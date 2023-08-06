"""Bandit Python tool class"""
import json
import re
import shlex

from eze.utils.log import log_debug

from eze.utils.io.file_scanner import cache_production_workspace_into_tmp
from eze.utils.vo.findings import SmellVO
from eze.utils.vo.enums import ToolType, SourceType, SmellSeverityEnum
from eze.core.tool import (
    ToolMeta,
)
from eze.utils.vo.findings import ScanVO
from eze.utils.cli.run import run_async_cli_command, CompletedProcess
from eze.utils.io.file import load_json
from eze.utils.cli.exe import exe_variable_interpolation_single


class BanditTool(ToolMeta):
    """Bandit Python tool class"""

    TOOL_NAME: str = "python-bandit"
    TOOL_URL: str = "https://bandit.readthedocs.io/en/latest/"
    TOOL_TYPE: ToolType = ToolType.SAST
    SOURCE_SUPPORT: list = [SourceType.PYTHON]
    SHORT_DESCRIPTION: str = "Opensource python SAST scanner"
    INSTALL_HELP: str = """In most cases all that is required to install bandit is python and pip install
pip install bandit
bandit --version"""
    MORE_INFO: str = """https://pypi.org/project/bandit/
https://bandit.readthedocs.io/en/latest/

Tips and Tricks
===============================
- exclude tests file as these use non-production functions like assert
  this will avoid lots of False positives
- use IGNORED_FILES to ignore false positives
"""
    # https://github.com/PyCQA/bandit/blob/master/LICENSE
    LICENSE: str = """Apache-2.0"""
    EZE_CONFIG: dict = {
        "SOURCE": {
            "type": str,
            "default": ".",
            "help_text": """bandit source folder to scan for python files""",
        },
        "EXCLUDE": {
            "type": list,
            "default": [],
            "help_text": """Array of list of paths (glob patterns supported) to exclude from scan (note that these are in addition to 
the excluded paths provided in the config file)
(default: .svn,CVS,.bzr,.hg,.git,__pycache__,.tox,.eggs,*.egg)""",
            "help_example": ["PATH-TO-EXCLUDED-FOLDER/.*", "PATH-TO-EXCLUDED-FILE.js"],
        },
        "INI_PATH": {
            "type": str,
            "default": "",
            "help_text": """.bandit config file to use
path to a .bandit file that supplies command line arguments
maps to "--ini INI_PATH""",
            "help_example": "XXX-XXX/.bandit",
        },
        "CONFIG_FILE": {
            "type": str,
            "default": "",
            "help_text": """Optional config file to use for selecting plugins and overriding defaults
maps to -c CONFIG_FILE""",
        },
        "INCLUDE_FULL_REASON": {
            "type": bool,
            "default": False,
            "help_text": """Optional inclusion the full reason in report
Warning: on production might want to set this to False to prevent found Secrets appearing in reports""",
        },
    }

    VERSION_CHECK: dict = {
        "FROM_EXE": "bandit --version",
        "FROM_DOCKER": {"DOCKER_COMMAND": {"IMAGE_NAME": "cytopia/bandit:1", "BASE_COMMAND": "--version"}},
    }
    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            "BASE_COMMAND": shlex.split("bandit -f json "),
            "DOCKER_COMMAND": {"FOLDER_NAME": "/data", "IMAGE_NAME": "cytopia/bandit:1", "BASE_COMMAND": "-f json"},
            # eze config fields -> flags
            "FLAGS": {
                "REPORT_FILE": "-o ",
                #
                "SOURCE": "-r ",
                "CONFIG_FILE": "-c ",
                "INI_PATH": "--ini ",
                "EXCLUDE": "-x ",
            },
        }
    }

    async def run_scan(self) -> ScanVO:
        """
        Run scan using tool

        typical steps
        1) setup config
        2) run tool
        3) parse tool report & normalise into common format

        :raises EzeError
        """
        self.config["REPORT_FILE"] = "__EZE_CONFIG_FOLDER__/raw/_bandit-report.json"
        scan_config = self.config.copy()
        cwd: str = cache_production_workspace_into_tmp()
        completed_process: CompletedProcess = await run_async_cli_command(
            self.TOOL_CLI_CONFIG["CMD_CONFIG"], scan_config, self.TOOL_NAME, cwd=cwd
        )

        report_local_filepath: str = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        parsed_json = load_json(report_local_filepath)
        report: ScanVO = self.parse_report(parsed_json)
        return report

    def parse_report(self, parsed_json: dict) -> ScanVO:
        """convert report json into ScanVO"""
        report_results = parsed_json["results"]
        smells_list: list[SmellVO] = []

        for report_result in report_results:
            path: str = report_result["filename"]

            # WORKAROUND: clean up docker path, remove './' prefix
            path = re.sub("^./", "", path)
            reason: str = report_result["issue_text"]

            line: str = report_result["line_number"]

            raw_code: str = report_result["code"]

            name: str = reason
            summary: str = f"'{reason}', in {path}"
            recommendation: str = f"Investigate '{path}' Line {line} for '{reason}' strings"

            # only include full reason if include_full_reason true
            if self.config["INCLUDE_FULL_REASON"]:
                recommendation += " Full Match: " + raw_code

            smells_list.append(
                SmellVO(
                    {
                        "name": name,
                        "overview": summary,
                        "recommendation": recommendation,
                        "language": "python",
                        "severity": convert_bandit_to_smell_severity(
                            report_result["issue_severity"],
                            report_result["issue_confidence"],
                        ),
                        "identifiers": {"bandit-code": f"{report_result['test_id']}:{report_result['test_name']}"},
                        "metadata": None,
                        "file_location": {"path": path, "line": line},
                    }
                )
            )

        errors = list(map(json.dumps, parsed_json["errors"]))
        report: ScanVO = ScanVO(
            {
                "tool": self.TOOL_NAME,
                "smells": smells_list,
                "warnings": errors,
            }
        )
        return report

    def _parse_config(self, eze_config: dict) -> dict:
        """take raw config dict and normalise values"""
        parsed_config = super()._parse_config(eze_config)

        # ADDITION PARSING: EXCLUDE
        # convert to space separated, clean os specific regex
        if len(parsed_config["EXCLUDE"]) > 0:
            parsed_config["EXCLUDE"] = ",".join(parsed_config["EXCLUDE"])
        else:
            parsed_config["EXCLUDE"] = ""

        return parsed_config


def convert_bandit_to_smell_severity(bandit_severity: str, bandit_confidence: str) -> str:
    if bandit_severity == "HIGH":
        if bandit_confidence == "LOW":
            return SmellSeverityEnum.warning.name
        else:
            return SmellSeverityEnum.error.name
    elif bandit_severity == "MEDIUM":
        if bandit_confidence == "HIGH":
            return SmellSeverityEnum.error.name
        else:
            return SmellSeverityEnum.warning.name
    elif bandit_severity == "LOW":
        return SmellSeverityEnum.note.name
    elif bandit_severity == "UNDEFINED":
        return SmellSeverityEnum.note.name
    log_debug(f"Unknown kics severity: {bandit_severity}")
    return SmellSeverityEnum.warning.name
