"""NpmAudit tool class"""
import shlex

from eze.utils.cli.exe import exe_variable_interpolation_single

from eze.utils.log import log_debug
from pydash import py_

from eze.utils.vo.findings import VulnerabilityVO
from eze.utils.vo.enums import VulnerabilitySeverityEnum, ToolType, SourceType
from eze.core.tool import (
    ToolMeta,
)
from eze.utils.vo.findings import ScanVO
from eze.utils.cli.run import run_async_cli_command, CompletedProcess
from eze.utils.io.file import write_text, parse_json
from eze.utils.language.node import install_npm_in_path, get_npm_projects, NPM_DOCKER_IMAGE
from pathlib import Path


class NpmAuditTool(ToolMeta):
    """NpmAudit Node tool class"""

    TOOL_NAME: str = "node-npmaudit"
    TOOL_URL: str = "https://docs.npmjs.com/cli/v6/commands/npm-audit"
    TOOL_TYPE: ToolType = ToolType.SCA
    SOURCE_SUPPORT: list = [SourceType.NODE]
    SHORT_DESCRIPTION: str = "Opensource node SCA scanner"
    INSTALL_HELP: str = """In most cases all that is required to install node and npm (version 6+)
npm --version"""
    MORE_INFO: str = """https://docs.npmjs.com/cli/v6/commands/npm-audit
https://docs.npmjs.com/downloading-and-installing-node-js-and-npm
"""
    EZE_CONFIG: dict = {
        "INCLUDE_DEV": {
            "type": bool,
            "default": False,
            "help_text": "Include development dependencies from the SCA, if false adds '--only=prod' flag to ignore devDependencies",
        },
    }
    # https://github.com/npm/cli/blob/latest/LICENSE
    LICENSE: str = """NPM"""
    # TODO: improve with FROM_NPM ? ps docker run node:19.3.0-slim npm --version
    VERSION_CHECK: dict = {
        "FROM_EXE": "npm --version",
        "FROM_DOCKER": {"DOCKER_COMMAND": {"IMAGE_NAME": NPM_DOCKER_IMAGE, "BASE_COMMAND": "npm --version"}},
        "CONDITION": ">=9",
    }
    DEFAULT_SEVERITY = VulnerabilitySeverityEnum.high.name
    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            "BASE_COMMAND": shlex.split("npm audit --json"),
            "DOCKER_COMMAND": {
                "FOLDER_NAME": "/src",
                "WORKING_FOLDER": "/src",
                "IMAGE_NAME": NPM_DOCKER_IMAGE,
                "BASE_COMMAND": "npm audit --json",
                "ENV_VARS": {"NPM_CONFIG_UPDATE_NOTIFIER": "false"},
            },
            # eze config fields -> flags
            "SHORT_FLAGS": {"_ONLY_PROD": "--omit=dev"},
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
        self.config["REPORT_FILE"] = "__EZE_CONFIG_FOLDER__/raw/_npmaudit-report.json"
        vulnerabilities_list: list = []
        npm_package_jsons = get_npm_projects()
        for npm_package in npm_package_jsons:
            log_debug(f"run 'npm audit' on {npm_package}")
            npm_project = Path(npm_package).parent
            npm_project_fullpath = Path.joinpath(Path.cwd(), npm_project)
            await install_npm_in_path(npm_project)
            self.config["__THROW_ERROR_ON_STDERR"] = True
            completed_process: CompletedProcess = await run_async_cli_command(
                self.TOOL_CLI_CONFIG["CMD_CONFIG"], self.config, self.TOOL_NAME, cwd=npm_project_fullpath
            )
            report_text = completed_process.stdout
            report_local_filepath: str = exe_variable_interpolation_single(self.config["REPORT_FILE"])
            write_text(report_local_filepath, report_text)
            parsed_json = parse_json(report_text)
            vulnerabilities = self.parse_report(parsed_json, npm_package)
            vulnerabilities_list.extend(vulnerabilities)

        report: ScanVO = ScanVO(
            {
                "tool": self.TOOL_NAME,
                "vulnerabilities": vulnerabilities_list,
                "warnings": [],
            }
        )

        return report

    def parse_report(self, parsed_json: dict, npm_package: str = None) -> list:
        """convert report json into ScanVO"""
        # v7+ npm audit
        # https://blog.npmjs.org/post/626173315965468672/npm-v7-series-beta-release-and-semver-major
        return self.parse_npm_v7_report(parsed_json, npm_package)

    def create_recommendation_v7(self, vulnerability: dict):
        """convert vulnerability dict into recommendation"""
        fix_available = vulnerability["fixAvailable"]
        if not fix_available:
            return "no fix available"

        recommendation = "fix available via `npm audit fix --force`"
        if fix_available is True:
            return recommendation

        recommendation += f"\nWill install {fix_available['name']}@{fix_available['version']}"

        if fix_available["isSemVerMajor"] is True:
            recommendation += ", which is a breaking change"

        return recommendation

    def create_path_v7(self, vulnerability: dict) -> str:
        """extract the path from the vulnerability"""
        # detected module from vulnerability details
        module_name = py_.get(vulnerability, "via[0].name", False) or py_.get(vulnerability, "name")

        # create path
        module_path = ""
        for parent_module in vulnerability["effects"]:
            module_path += f"{parent_module}>"

        # pull it all together
        path = f"{module_path}{module_name}"

        return path

    def create_version_v7(self, vulnerability: dict) -> str:
        """extract the version from the vulnerability"""
        module_version = py_.get(vulnerability, "via[0].range", False) or py_.get(vulnerability, "range")

        return module_version

    def create_description_v7(self, vulnerability: dict):
        """extract the description from the vulnerability"""
        # detected module from vulnerability details
        module_version = self.create_version_v7(vulnerability)

        # create path
        module_path = self.create_path_v7(vulnerability)

        # if advisory not present, it's a insecure dependency issue
        advisory_title = py_.get(vulnerability, "via[0].title", "")
        if not advisory_title:
            advisory_title = "has insecure dependency "
            advisory_title += ">".join(reversed(vulnerability["via"]))

        # pull it all together
        path = f"{module_path}({module_version})"

        if advisory_title:
            path += f": {advisory_title}"

        return path

    def parse_npm_v7_report(self, parsed_json: dict, npm_package: str) -> list:
        """Parses newer v7 npm audit format"""
        # WARNING: npm v7 report format doesn't look complete
        #
        # wouldn't be surprised if there are future breaking changes to the format,
        # at a glance the v2 reports looks less mature to v1 reports
        # and looks like there are some quality and accuracy issues
        # ("via" array doesn't always seem correct for complex dependency trees)
        #
        # Excellent commentary : https://uko.codes/dealing-with-npm-v7-audit-changes
        vulnerabilities = py_.get(parsed_json, "vulnerabilities", None)
        vulnerabilities_list: list = []

        if vulnerabilities:
            for vulnerability_key in vulnerabilities:
                vulnerability = vulnerabilities[vulnerability_key]

                name: str = self.create_path_v7(vulnerability)
                version: str = self.create_version_v7(vulnerability)
                description: str = self.create_description_v7(vulnerability)
                recommendation: str = self.create_recommendation_v7(vulnerability)

                references = []
                npm_reference = py_.get(vulnerability, "via[0].url", False)
                if npm_reference:
                    references.append(npm_reference)

                vulnerability_vo = {
                    "name": name,
                    "version": version,
                    "overview": description,
                    "recommendation": recommendation,
                    "severity": vulnerability["severity"],
                    "identifiers": {},
                    "references": references,
                    "metadata": None,
                    "file_location": {"path": npm_package, "line": 1},
                }

                # WARNING: AB-524: limitation, for now just showing first advisory
                advisory_source = py_.get(vulnerability, "via[0].source", False)
                if advisory_source:
                    vulnerability_vo["identifiers"]["npm"] = advisory_source

                vulnerabilities_list.append(VulnerabilityVO(vulnerability_vo))

        return vulnerabilities_list

    def _parse_config(self, eze_config: dict) -> dict:
        """take raw config dict and normalise values"""
        parsed_config = super()._parse_config(eze_config)

        # ADDITION PARSING: invert INCLUDE_DEV into _ONLY_PROD(--only-prod) flag
        parsed_config["_ONLY_PROD"] = not parsed_config["INCLUDE_DEV"]

        return parsed_config
