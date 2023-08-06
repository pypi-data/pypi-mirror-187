"""Lists out the inbuilt plugins in Eze"""
from eze.plugins.reporters.bom import BomReporter
from eze.plugins.reporters.console import ConsoleReporter
from eze.plugins.reporters.eze import EzeReporter
from eze.plugins.reporters.json import JsonReporter
from eze.plugins.reporters.sarif import SarifReporter
from eze.plugins.reporters.markdown import MarkdownReporter
from eze.plugins.reporters.html import HtmlReporter
from eze.plugins.tools.anchore_grype import GrypeTool
from eze.plugins.tools.anchore_syft import SyftTool
from eze.plugins.tools.container_trivy import TrivyTool
from eze.plugins.tools.java_cyclonedx import JavaCyclonedxTool
from eze.plugins.tools.node_cyclonedx import NodeCyclonedxTool
from eze.plugins.tools.node_npmaudit import NpmAuditTool
from eze.plugins.tools.node_npmoutdated import NpmOutdatedTool
from eze.plugins.tools.python_bandit import BanditTool
from eze.plugins.tools.python_cyclonedx import PythonCyclonedxTool
from eze.plugins.tools.python_outdated import PythonOutdatedTool
from eze.plugins.tools.raw import RawTool
from eze.plugins.tools.semgrep import SemGrepTool

from eze.plugins.tools.trufflehog import TruffleHogTool
from eze.plugins.tools.checkmarx_kics import KicsTool
from eze.plugins.tools.dotnet_cyclonedx import DotnetCyclonedxTool


def get_reporters() -> dict:
    """Return the default reporters engines that are installed"""
    return {
        "console": ConsoleReporter,
        "json": JsonReporter,
        "eze": EzeReporter,
        "bom": BomReporter,
        "sarif": SarifReporter,
        "markdown": MarkdownReporter,
        "html": HtmlReporter,
    }


def get_tools() -> dict:
    """Return the default tools that are installed"""
    return {
        # Generic Tools
        "anchore-grype": GrypeTool,
        "anchore-syft": SyftTool,
        "container-trivy": TrivyTool,
        # Dotnet / C# Tools
        "dotnet-cyclonedx": DotnetCyclonedxTool,
        # Container SAST Tool
        "kics": KicsTool,
        # Java Tools
        "java-cyclonedx": JavaCyclonedxTool,
        # Node Tools
        "node-npmaudit": NpmAuditTool,
        "node-npmoutdated": NpmOutdatedTool,
        "node-cyclonedx": NodeCyclonedxTool,
        # Python Tools
        "python-outdated": PythonOutdatedTool,
        "python-bandit": BanditTool,
        "python-cyclonedx": PythonCyclonedxTool,
        "raw": RawTool,
        # SAST Tool
        "semgrep": SemGrepTool,
        # Secrets Tool
        "trufflehog": TruffleHogTool,
    }
