"""Print helpers
"""
import json
import re


def escape_markdown_text(text: str) -> str:
    """
    escape special markdown characters

    @see hhttps://www.markdownguide.org/basic-syntax/#escaping-characters
    """
    if not text:
        return ""
    return re.sub("([\\\\`*_{}\[\]<>()+.!|-])", r"\\\1", str(text))


def non_escape_text(text: str) -> str:
    """
    identity function for string

    @see hhttps://www.markdownguide.org/basic-syntax/#escaping-characters
    """
    return str(text)


def generate_markdown_header(title: str, headerLevel=1) -> str:
    """
    turn a str into a header

    @see https://www.markdownguide.org/basic-syntax/
    """
    return f"\n{'#'*headerLevel} {title}"


def generate_markdown_list(items: list) -> str:
    """
    turn a list of strs into a markdown list

    @see https://www.markdownguide.org/basic-syntax/
    """
    strip_and_add_list_indent: callable = (
        lambda line: "* " + line[1].strip() if line[0] == 0 else "  " + line[1].strip()
    )
    is_empty: callable = lambda i: i.strip() != ""
    return "\n".join(
        map(
            lambda item: "\n".join(map(strip_and_add_list_indent, enumerate(filter(is_empty, item.split("\n"))))), items
        )
    )


def generate_markdown_table(table: list, has_nothing_message: bool = True) -> str:
    """
    given kv create markdown string of table

    @see https://www.markdownguide.org/basic-syntax/
    """
    # WARNING: special print functions
    if len(table) == 0:
        if has_nothing_message:
            return "Nothing to display"
        return ""

    markdown_str: str = ""

    sample_entry = table[0]
    column_sizes = {}
    for column in sample_entry:
        column_sizes[column] = 0
        column_name_size = len(column)
        if column_name_size > column_sizes[column]:
            column_sizes[column] = column_name_size

    for table_row in table:
        for column in table_row:
            column_size = len(table_row[column])
            if column_size > column_sizes[column]:
                column_sizes[column] = column_size

    markdown_str += "|"
    for column_name in column_sizes:
        column_size = column_sizes[column_name]
        markdown_str += " " + column_name.ljust(column_size) + " |"

    markdown_str += "\n|"
    for column_name in column_sizes:
        column_size = column_sizes[column_name]
        markdown_str += " " + ("-" * column_size) + " " + "|"

    for table_row in table:
        markdown_str += "\n|"
        for column_name in column_sizes:
            column_size = column_sizes[column_name]
            column_value = table_row[column_name]
            markdown_str += " " + column_value.ljust(column_size) + " |"
        markdown_str += ""
    return markdown_str


def pretty_print_table(table: list, has_nothing_message: bool = True) -> None:
    """given kv print it as a pretty printed table
    output is compatible with markdown"""
    markdown_table = generate_markdown_table(table, has_nothing_message)
    print(markdown_table)


def pretty_print_json(obj) -> str:
    """Helper, takes generic python class/object and convert into pretty json str"""
    return json.dumps(obj, default=vars, indent=2, sort_keys=True)


def truncate(value: str, limit: int = 80, ellipsis: str = "…") -> str:
    """
    Helper, truncates string to character limit
    """
    value = value.strip().split("\n")[0].strip()
    if len(value) > limit - 1:
        return value[: limit - 1].strip() + ellipsis
    return value
