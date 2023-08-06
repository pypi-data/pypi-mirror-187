"""html reporter class implementation"""

from eze.utils.markdown_print import scan_results_as_markdown

from eze.core.reporter import ReporterMeta
from eze.utils.io.file import write_text
from eze.utils.log import log
import markdown

from eze.utils.cli.exe import exe_variable_interpolation_single


class HtmlReporter(ReporterMeta):
    """Python report class for echoing output into a html report"""

    REPORTER_NAME: str = "html"
    SHORT_DESCRIPTION: str = "HTML output file formatter"
    INSTALL_HELP: str = """inbuilt"""
    MORE_INFO: str = """inbuilt"""
    LICENSE: str = """inbuilt"""
    VERSION_CHECK: dict = {"FROM_EZE": True}
    EZE_CONFIG: dict = {
        "REPORT_FILE": {
            "type": str,
            "default": ".eze/eze_report.html",
            "help_text": """Report file location
By default set to eze_report.html""",
        },
        "PRINT_TRANSITIVE_PACKAGES": {
            "type": bool,
            "default": False,
            "environment_variable": "PRINT_TRANSITIVE_PACKAGES",
            "help_text": """Print out non top level packages""",
        },
    }

    async def run_report(self, scan_results: list):
        """Method for taking scans and turning then into report output for html format"""

        report_str = scan_results_as_markdown(scan_results, self.config["PRINT_TRANSITIVE_PACKAGES"])
        html_content = markdown.markdown(report_str, output_format="html", extensions=["tables", "attr_list"])
        html = (
            """
<!DOCTYPE html>
<html lang="en">
<head>
<style>
table {
    border: 1px solid #ddd;
    border-collapse: collapse;
    border-spacing: 0;
    margin-bottom: 20px;
}
thead th {
    border-bottom: 1px solid #000;
    border-left: 1px solid #000;
}
tbody tr>:first-child {
    border-left: 1px solid #000;
}
tbody>tr:nth-of-type(odd) {
    background-color: #f2f2f2;
}
tbody tr td {
    border: 1px solid #bbb;
}
td, th {
    line-height: 1.1;
    padding: 8px;
    vertical-align: top;
}
</style>
<title>Eze Scanning report</title>
</head>

<body>
<div class="container">
"""
            + html_content
            + """
</div>
</body>
</html>
"""
        )
        report_local_filepath = exe_variable_interpolation_single(self.config["REPORT_FILE"])
        file_location = write_text(report_local_filepath, html)
        log(f"Written html report : {file_location}")
