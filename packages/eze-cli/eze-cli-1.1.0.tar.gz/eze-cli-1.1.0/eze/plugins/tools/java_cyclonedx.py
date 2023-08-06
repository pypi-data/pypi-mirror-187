"""cyclonedx SBOM tool class"""
import shlex
from pathlib import Path

from eze.core.license import LICENSE_CHECK_CONFIG, LICENSE_ALLOWLIST_CONFIG, LICENSE_DENYLIST_CONFIG
from eze.utils.vo.enums import ToolType, SourceType
from eze.utils.vo.findings import ScanVO
from eze.core.tool import ToolMeta
from eze.utils.cli.run import run_async_cli_command, CompletedProcess
from eze.utils.log import log_debug
from eze.utils.io.file import load_json, write_json
from eze.utils.scan_result import convert_multi_sbom_into_scan_result
from eze.utils.language.java import ignore_groovy_errors, get_maven_projects, MAVEN_DOCKER_IMAGE
from eze.utils.data.osv import osv_sca_sboms
from eze.utils.cli.exe import exe_variable_interpolation_single


class JavaCyclonedxTool(ToolMeta):
    """cyclonedx java bill of materials generator & vulnerability detection tool (SBOM/SCA) tool class"""

    TOOL_NAME: str = "java-cyclonedx"
    TOOL_URL: str = "https://owasp.org/www-project-cyclonedx/"
    TOOL_TYPE: ToolType = ToolType.SBOM
    SOURCE_SUPPORT: list = [SourceType.JAVA]
    SHORT_DESCRIPTION: str = "Opensource java bill of materials generator & open-source vulnerability detection tool"
    INSTALL_HELP: str = """In most cases all that is required is java and mvn installed

https://maven.apache.org/download.cgi

test with

mvn --version
"""
    MORE_INFO: str = """
https://github.com/CycloneDX/cyclonedx-maven-plugin
https://owasp.org/www-project-cyclonedx/
https://cyclonedx.org/

Tips and Tricks
===========================
You can add org.cyclonedx:cyclonedx-maven-plugin to customise your SBOM output

<plugin>
  <groupId>org.cyclonedx</groupId>
  <artifactId>cyclonedx-maven-plugin</artifactId>
  <version>X.X.X</version>
</plugin>
"""
    # https://github.com/CycloneDX/cyclonedx-maven-plugin/blob/master/LICENSE
    LICENSE: str = """Apache-2.0"""
    EZE_CONFIG: dict = {
        "MVN_REPORT_FILE": {
            "type": str,
            "default": "target/bom.json",
            "help_text": "Maven output bom.json location, relative to pom.xml folder, will be loaded, parsed and copied to <REPORT_FILE>",
        },
        "SCA_ENABLED": {
            "type": bool,
            "default": True,
            "help_text": "use osv data feeds to detect Maven vulnerabilities",
        },
        "LICENSE_CHECK": LICENSE_CHECK_CONFIG.copy(),
        "LICENSE_ALLOWLIST": LICENSE_ALLOWLIST_CONFIG.copy(),
        "LICENSE_DENYLIST": LICENSE_DENYLIST_CONFIG.copy(),
    }
    VERSION_CHECK: dict = {
        "FROM_MAVEN": "org.cyclonedx:cyclonedx-maven-plugin",
    }
    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            # tool command prefix
            "BASE_COMMAND": shlex.split(
                "mvn -B -Dmaven.javadoc.skip=true -Dmaven.test.skip=true install org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom"
            ),
            "DOCKER_COMMAND": {
                "FOLDERS": {"/root/.m2": "__ABSOLUTE_CWD__.eze/.m2"},
                "FOLDER_NAME": "/src",
                "WORKING_FOLDER": "/src",
                "IMAGE_NAME": MAVEN_DOCKER_IMAGE,
                "BASE_COMMAND": "mvn -B -Dmaven.javadoc.skip=true -Dmaven.test.skip=true install org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom",
            },
        }
    }

    async def run_scan(self) -> ScanVO:
        """
        Run scan using tool

        typical steps
        1) find all the manifests aka "package.json"s
        2) setup config
        3) run tool against
        4) parse tool report & normalise into common format
        5) repeat

        :raises EzeError
        """
        self.config["REPORT_FILE"] = "__EZE_CONFIG_FOLDER__/raw/_java-cyclonedx-bom.json"
        warnings_list: list = []
        sboms: dict = {}
        pom_files: list = get_maven_projects()

        for pom_file in pom_files:
            log_debug(f"run 'java cyclonedx' on {pom_file}")
            maven_project = Path(pom_file).parent
            maven_project_fullpath = Path.joinpath(Path.cwd(), maven_project)

            self.config["__THROW_ERROR_ON_STDERR"] = True
            completed_process: CompletedProcess = await run_async_cli_command(
                self.TOOL_CLI_CONFIG["CMD_CONFIG"], self.config, self.TOOL_NAME, cwd=maven_project_fullpath
            )
            # TODO: AB#1047: add option to SCA test dependencies: INCLUDE_TEST -DincludeTestScope=true
            # TODO: AB#1048: EZE CLI: mark java-cyclonedx transitive packages
            # "properties"."transitive" not "dependency" as too complex to calculate
            # mvn dependency:tree -DoutputType=dot  -Dverbose
            # https://maven.apache.org/plugins/maven-dependency-plugin/tree-mojo.html
            bom_fullpath = Path.joinpath(maven_project_fullpath, self.config["MVN_REPORT_FILE"])
            cyclonedx_bom = load_json(str(bom_fullpath))

            report_local_filepath: str = exe_variable_interpolation_single(self.config["REPORT_FILE"])
            write_json(report_local_filepath, cyclonedx_bom)
            sboms[pom_file] = cyclonedx_bom
            if completed_process.stderr:
                tool_warnings = ignore_groovy_errors(completed_process.stderr)
                for tool_warning in tool_warnings:
                    warnings_list.append(tool_warning)

        report: ScanVO = self.parse_report(sboms)
        # add all warnings
        report.warnings.extend(warnings_list)

        return report

    def parse_report(self, cyclonedx_boms: dict) -> ScanVO:
        """convert report json into ScanVO"""
        is_sca_enabled = self.config.get("SCA_ENABLED", False)
        scan_result: ScanVO = convert_multi_sbom_into_scan_result(self, cyclonedx_boms)
        if not is_sca_enabled:
            return scan_result
        # When SCA_ENABLED get SCA vulnerabilities/warnings directly from PYPI
        [osv_vulnerabilities, osv_warnings] = osv_sca_sboms(cyclonedx_boms)
        scan_result.vulnerabilities.extend(osv_vulnerabilities)
        scan_result.warnings.extend(osv_warnings)

        return scan_result
