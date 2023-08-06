"""helper functions for dealing with dotnet"""

import re
import shlex

from pydash import py_

from eze.utils.data.osv import get_osv_id_data

from eze.utils.vo.findings import VulnerabilityVO
from eze.utils.vo.enums import VulnerabilitySeverityEnum
from eze.utils.cli.run import run_async_cmd, has_missing_exe_output, CompletedProcess
from eze.utils.io.file_scanner import find_files_by_name
from eze.utils.io.file import create_absolute_path

from eze.utils.error import EzeExecutableNotFoundError
from typing import Tuple

# TODO: handle multiple sdk versions

DOTNET_DOCKER_IMAGE = "mcr.microsoft.com/dotnet/sdk:7.0"


class DeprecatedPackage:
    def __init__(self, vo: list):
        self.package = vo[0]
        self.request_version = vo[1]
        self.installed_version = vo[2]
        self.reason = vo[3]
        self.alternative = vo[4]


class VulnerablePackage:
    def __init__(self, vo: list):
        self.package = vo[0]
        self.request_version = vo[1]
        self.installed_version = vo[2]
        self.severity = vo[3]
        self.advisory_url = vo[4]
        advisory_id_matches = re.compile(r".*[/](.*)$", re.ASCII).match(self.advisory_url)
        self.advisory_id = advisory_id_matches.group(1) if advisory_id_matches else None


class DotnetPackage:
    def __init__(self, vo: list, is_transitive: bool):
        self.is_transitive = is_transitive
        self.package = vo[0]
        if len(vo) == 2:
            self.installed_version = vo[1]
        if len(vo) == 4:
            self.request_version = vo[1]
            self.installed_version = vo[3]


def get_dotnet_projects() -> []:
    """give a list of dotnet_projects"""
    dotnet_projects = find_files_by_name(".*[.]csproj$")
    return dotnet_projects


def get_dotnet_solutions() -> []:
    """give a list of dotnet_solutions"""
    dotnet_solutions = find_files_by_name(".*[.]sln$")
    return dotnet_solutions


def extract_deprecated_packages(stdout: str) -> list:
    """
    extract deprecated packages from dotnet output
    TODO: upgrade to --json dotnet once available
    """
    deprecated_package_re = re.compile(r"^[ ]+>[ ]+([^ ]+)[ ]+([^ ]+)[ ]+([^ ]+)[ ]+([^ ]+)[ ]+(.+)", re.ASCII)
    stdout_lines = stdout.split("\n")
    deprecated_packages: list = []
    for stdout_line in stdout_lines:
        matches = deprecated_package_re.match(stdout_line)
        if not matches:
            continue
        deprecated_packages.append(DeprecatedPackage(matches.groups()))
    return deprecated_packages


async def get_deprecated_packages(project_folder: str, dotnet_project_file: str) -> list:
    """
    use dotnet to get list of deprecated packages
    @see https://www.nuget.org/packages?q=deprecated
    """
    (completed_process, used_docker_dotnet) = await run_dotnet_command(
        "dotnet list package --deprecated", project_folder
    )
    return list(
        map(
            lambda deprecated_package: VulnerabilityVO(
                {
                    "name": deprecated_package.package,
                    "version": deprecated_package.installed_version,
                    "overview": f"'{deprecated_package.package}' is deprecated",
                    "recommendation": f"recommended migrate to {deprecated_package.alternative}"
                    if deprecated_package.alternative
                    else None,
                    "severity": VulnerabilitySeverityEnum.medium.name,
                    "file_location": {"path": dotnet_project_file, "line": 1},
                }
            ),
            extract_deprecated_packages(completed_process.stdout),
        )
    )


def extract_vulnerable_packages(stdout: str) -> list:
    """
    extract vulnerable packages from dotnet output
    TODO: upgrade to --json dotnet once available
    """
    deprecated_package_re = re.compile(r"^[ ]+>[ ]+([^ ]+)[ ]+([^ ]+)[ ]+([^ ]+)[ ]+([^ ]+)[ ]+(.+)", re.ASCII)
    stdout_lines = stdout.split("\n")
    deprecated_packages: list = []
    for stdout_line in stdout_lines:
        matches = deprecated_package_re.match(stdout_line)
        if not matches:
            continue
        deprecated_packages.append(VulnerablePackage(matches.groups()))
    return deprecated_packages


async def get_vulnerable_packages(project_folder: str, dotnet_project_file: str) -> list:
    """
    use dotnet to get list of vulnerable packages
    @see https://www.nuget.org/packages
    """
    (completed_process, used_docker_dotnet) = await run_dotnet_command(
        "dotnet list package --vulnerable", project_folder
    )
    vulnerable_packages = extract_vulnerable_packages(completed_process.stdout)
    vp: VulnerablePackage
    vulnerabilities = []
    for vp in vulnerable_packages:
        if vp.advisory_id:
            osv_vuln = get_osv_id_data(vp.advisory_id, vp.package, vp.installed_version, dotnet_project_file)
            if osv_vuln.severity == "" or osv_vuln.severity == VulnerabilitySeverityEnum.na.name:
                osv_vuln.severity = vp.severity.lower()
            vulnerabilities.append(osv_vuln)
        else:
            vulnerabilities.append(
                VulnerabilityVO(
                    {
                        "name": vp.package,
                        "version": vp.installed_version,
                        "overview": f"'{vp.package}' has {vp.severity.lower()} vulnerability {vp.advisory_url}",
                        "recommendation": None,
                        "severity": vp.severity.lower(),
                        "file_location": {"path": dotnet_project_file, "line": 1},
                    }
                )
            )
    return vulnerabilities


def _extract_transitive_packages(stdout: str, is_transitive: bool) -> dict:
    """
    extract packages from dotnet output, as indexed
    TODO: upgrade to --json dotnet once available
    """
    package_re = re.compile(r"^[ ]+>[ ]+([^ ]+)[ ]+([^ ]+)([ ]+([^ ]+))?", re.ASCII)
    stdout_lines = stdout.split("\n")
    packages: dict = {}
    for stdout_line in stdout_lines:
        matches = package_re.match(stdout_line)
        if not matches:
            continue
        package = DotnetPackage(matches.groups(), is_transitive)
        packages[package.package] = package
    return packages


def extract_transitive_packages(stdout: str) -> dict:
    """
    extract top level abd transitive packages from dotnet output, as indexed
    TODO: upgrade to --json dotnet once available
    """
    stdouts: list = stdout.split("Transitive Package")
    top_level_stdout: str = py_.get(stdouts, "[0]", "")
    transitive_stdout: str = py_.get(stdouts, "[1]", "")
    return {
        "top_level": _extract_transitive_packages(top_level_stdout, False),
        "transitive": _extract_transitive_packages(transitive_stdout, True),
    }


async def annotate_transitive_licenses(sbom: dict, project_folder: str) -> dict:
    """adding annotations to licenses which are not top-level"""
    (completed_process, used_docker_dotnet) = await run_dotnet_command(
        "dotnet list package --include-transitive", project_folder
    )
    packages = extract_transitive_packages(completed_process.stdout)
    for component in py_.get(sbom, "components", []):
        component_name = component["name"]
        is_not_transitive = component_name in packages["top_level"]
        is_transitive = component_name in packages["transitive"]
        if is_transitive:
            py_.set(component, "properties.transitive", True)
        elif is_not_transitive:
            py_.set(component, "properties.transitive", False)
    return packages


async def run_dotnet_command(dotnet_command: str, cwd: str) -> Tuple[CompletedProcess, bool]:
    """run dotnet local command with docker fallback"""
    absolute_cwd: str = str(create_absolute_path(cwd))
    try:
        completed_process: CompletedProcess = await run_async_cmd(shlex.split(dotnet_command), True, cwd=absolute_cwd)
        output = completed_process.stdout
        if has_missing_exe_output(output):
            raise EzeExecutableNotFoundError("failed local dotnet try docker")
        return completed_process, False
    except EzeExecutableNotFoundError as error:
        return (
            await run_async_cmd(
                shlex.split(
                    f"docker run --rm -v {absolute_cwd}:/src -w /src --rm {DOTNET_DOCKER_IMAGE} {dotnet_command}"
                ),
                True,
                cwd=absolute_cwd,
            ),
            True,
        )
