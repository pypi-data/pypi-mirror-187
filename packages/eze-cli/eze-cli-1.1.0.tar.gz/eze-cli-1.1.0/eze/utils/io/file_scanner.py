"""Basic file finder utility
"""
import os
import re
import shutil
from distutils.file_util import copy_file
from pathlib import Path

from eze.utils.log import log_debug

from eze.utils.io.file import create_tempfile_folder

from eze.utils.error import EzeError


class Cache:
    """Cache class container"""


__c = Cache()
__c.discovered_folders = None
__c.ignored_folders = None
__c.discovered_files = None
__c.discovered_production_files = None
__c.discovered_filenames = None
__c.discovered_types = None
__c.cached_workspace = False
__c.cached_production_workspace = False

IGNORED_FOLDERS: list = [
    # IDEs and Configs
    ".gradle",
    ".aws",
    ".idea",
    ".git",
    ".eze",
    ".coverage",
    "~",
    # TERRAFORM
    ".terraform",
    # NODE
    "node_modules",
    "build",
    "target",
    "vendor",
    # PYTHON
    ".pytest_cache",
    "__pycache__",
    ".env",
    ".venv",
    ".tox",
    "venv",
    "dist",
    "sdist",
]
IGNORED_FILES: list = [
    # IDEs and Configs
    # TERRAFORM
    ".terraform.lock.hcl",
    # NODE
    "package-lock.json",
    # PYTHON
]

TEST_FOLDER_NAMES: list = [
    # IDEs and Configs
    "test",
    "tests",
    "__tests__",
]

TEST_FILE_PATTERNS: list = [
    # IDEs and Configs
    # NODE
    "\\.test\\.[a-z]+$",
    # PYTHON
    "^test_",
    # JAVA
    "Test\\.[a-z]+$",
]


def _is_test_file(filename: str, file_path: str) -> bool:
    """test files tester"""
    if file_path:
        linux_paths: list[str] = file_path.split("/")
        if len(linux_paths) > 1 and any(item in TEST_FOLDER_NAMES for item in linux_paths):
            return True
        windows_and_single_paths: list[str] = file_path.split("\\")
        if any(item in TEST_FOLDER_NAMES for item in windows_and_single_paths):
            return True
    if any(re.search(pattern, filename) for pattern in TEST_FILE_PATTERNS):
        return True
    return False


def populate_file_cache(
    *,
    discovered_folders: list,
    ignored_folders: list,
    discovered_files: list,
    discovered_production_files: list,
    discovered_filenames: list,
    discovered_types: dict,
) -> None:
    """delete file caching"""
    __c.discovered_folders = discovered_folders
    __c.ignored_folders = ignored_folders
    __c.discovered_files = discovered_files
    __c.discovered_production_files = discovered_production_files
    __c.discovered_filenames = discovered_filenames
    __c.discovered_types = discovered_types


def initialise_cache():
    """sets up cache of files for project"""
    if not __c.discovered_folders:
        [
            discovered_folders,
            ignored_folders,
            discovered_files,
            discovered_production_files,
            discovered_filenames,
            discovered_types,
        ] = _build_file_list()
        populate_file_cache(
            discovered_folders=discovered_folders,
            ignored_folders=ignored_folders,
            discovered_files=discovered_files,
            discovered_production_files=discovered_production_files,
            discovered_filenames=discovered_filenames,
            discovered_types=discovered_types,
        )


def delete_file_cache() -> None:
    """delete file caching"""
    __c.discovered_folders = None
    __c.ignored_folders = None
    __c.discovered_files = None
    __c.discovered_production_files = None
    __c.discovered_filenames = None
    __c.discovered_types = None
    __c.cached_workspace = False


def _build_file_list(root_path: str = None) -> list:
    """build a list of folder and file names"""
    if not root_path:
        root_path = Path.cwd()
    walk_dir: str = os.path.abspath(root_path)

    root_prefix = len(str(Path(root_path))) + 1

    ignored_folders: list[str] = []
    discovered_files: list[str] = []
    discovered_production_files: list[str] = []
    discovered_folders: list[str] = []
    discovered_filenames: list[str] = []
    discovered_filetypes: dict = {}

    for root, subdirs, files in os.walk(walk_dir):
        # Ignore Some directories
        for ignored_directory in IGNORED_FOLDERS:
            if ignored_directory in subdirs:
                ignored_folder_path: str = os.path.join(root, ignored_directory)[root_prefix:]
                ignored_folders.append(ignored_folder_path)
                subdirs.remove(ignored_directory)

        for subdir in subdirs:
            folder_path: str = os.path.join(root, subdir)[root_prefix:]
            discovered_folders.append(folder_path)

        for filename in files:
            file_path: str = os.path.join(root, filename)[root_prefix:]
            folder_path: str = os.path.join(root)[root_prefix:]
            discovered_files.append(file_path)
            if not _is_test_file(filename, folder_path):
                discovered_production_files.append(file_path)
            discovered_filenames.append(filename)
            filename_without_extension, extension = os.path.splitext(filename)
            if not extension:
                extension = filename_without_extension
            if extension not in discovered_filetypes:
                discovered_filetypes[extension] = 0
            discovered_filetypes[extension] += 1

    return [
        discovered_folders,
        ignored_folders,
        discovered_files,
        discovered_production_files,
        discovered_filenames,
        discovered_filetypes,
    ]


def has_filetype(filetype: str) -> int:
    """will return count of given file type aka '.py'"""
    initialise_cache()
    if filetype not in __c.discovered_types:
        return 0
    return __c.discovered_types[filetype]


def find_files_by_path(regex_str: str) -> list:
    """find list of matching files by full path aka 'backend\\function\\ezemcdbcrud\\src\\package.json'"""
    list_of_files: list = get_file_list()
    try:
        regex = re.compile(regex_str)
    except re.error as error:
        raise EzeError(f"unable to parse regex '{regex_str}' due to {error.msg}")
    return list(filter(regex.match, list_of_files))


def find_files_by_name(regex_str: str) -> list:
    """find list of matching files by name aka 'package.json'"""
    list_of_files: list = get_file_list()
    list_of_filenames: list = get_filename_list()
    try:
        regex = re.compile(regex_str)
    except re.error as error:
        raise EzeError(f"unable to parse regex '{regex_str}' due to {error.msg}")
    counter = 0
    files_by_name = []
    for filename in list_of_filenames:
        if regex.match(filename):
            files_by_name.append(list_of_files[counter])
        counter += 1
    return files_by_name


def get_filename_list() -> list:
    """get list of files aka package.json"""
    initialise_cache()
    return __c.discovered_filenames


def get_file_list() -> list:
    """
    get list of filepathsincludes src and tests, but excludes dependencies
    aka backend\\function\\ezemcdbcrud\\src\\package.json
    """
    initialise_cache()
    return __c.discovered_files


def get_production_file_list() -> list:
    """
    get list of filepathsincludes src, but excludes dependencies and tests
    aka backend\\function\\ezemcdbcrud\\src\\package.json
    """
    initialise_cache()
    return __c.discovered_production_files


def get_ignored_folder_list() -> list:
    """get list of folders aka backend\\function\\ezemcdbcrud\\src\\"""
    initialise_cache()
    return __c.ignored_folders


def get_folder_list() -> list:
    """get list of folders aka backend\\function\\ezemcdbcrud\\src\\"""
    initialise_cache()
    return __c.discovered_folders


def cache_workspace_into_tmp() -> str:
    """
    create cached folder includes src and tests, but excludes dependencies stored in temp

    used by SAST, secrets SAST tools, that needs src and test assets,
    but not dependencies (aka saves scanning dependencies for secrets / SAST)
    """
    workspace_folder: str = create_tempfile_folder("cached-workspace")
    if __c.cached_workspace:
        return workspace_folder
    log_debug(f"clearing and copying all prod and test files to {workspace_folder}")
    shutil.rmtree(workspace_folder)
    files = get_file_list()
    for file in files:
        dest_file = os.path.join(workspace_folder, file)
        log_debug(f"copying to '{dest_file}'")
        os.makedirs(Path(dest_file).parent, exist_ok=True)
        copy_file(file, dest_file)
    __c.cached_workspace = True
    return workspace_folder


def cache_production_workspace_into_tmp() -> str:
    """
    create cached folder includes src, but excludes dependencies and tests stored in temp

    used by SAST that needs src assets, but not dependencies or test
    (aka saves scanning dependencies for SAST and false positive issues)
    """
    production_workspace_folder: str = create_tempfile_folder("cached-production-workspace")
    if __c.cached_production_workspace:
        return production_workspace_folder
    log_debug(f"clearing and copying prod files to {production_workspace_folder} (excluding test files)")
    shutil.rmtree(production_workspace_folder)
    production_files = get_production_file_list()
    for file in production_files:
        dest_file = os.path.join(production_workspace_folder, file)
        log_debug(f"copying to '{dest_file}'")
        os.makedirs(Path(dest_file).parent, exist_ok=True)
        copy_file(file, dest_file)
    __c.cached_production_workspace = True
    return production_workspace_folder
