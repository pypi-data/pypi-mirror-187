"""Helper functions for manipulating license data for SBOMs"""

import os
from pathlib import Path

import re

from pydash import py_

from eze.utils.vo.enums import LicenseScanType, SmellSeverityEnum
from eze.utils.vo.findings import LicenseRiskVO, SmellVO
from eze.utils.io.file import load_json
from eze.utils.log import log_error
from eze.utils.io.print import truncate
from eze.utils.vo.sboms import Component

LICENSE_TYPES = {
    "unrestricted": {
        "usageRestrictions": False,
        "shareDerivedSource": False,
        "shareLinkedSource": False,
        "attributionRequired": False,
    },
    "permissive": {
        "usageRestrictions": False,
        "shareDerivedSource": False,
        "shareLinkedSource": False,
        "attributionRequired": True,
    },
    "permissive-with-conditions": {
        "usageRestrictions": True,
        "shareDerivedSource": False,
        "shareLinkedSource": False,
        "attributionRequired": True,
    },
    "weak-copyleft": {
        "usageRestrictions": True,
        "shareLinkedSource": False,
        "shareDerivedSource": True,
        "attributionRequired": True,
    },
    "source-available": {
        "usageRestrictions": False,
        "shareLinkedSource": True,
        "shareDerivedSource": True,
        "attributionRequired": True,
    },
    "copyleft": {
        "usageRestrictions": True,
        "shareLinkedSource": True,
        "shareDerivedSource": True,
        "attributionRequired": True,
    },
    "noncommercial": {
        "usageRestrictions": True,
        "shareLinkedSource": False,
        "shareDerivedSource": False,
        "attributionRequired": True,
    },
    "proprietary": {
        "usageRestrictions": True,
        "shareLinkedSource": None,
        "shareDerivedSource": None,
        "attributionRequired": None,
    },
}

LICENSE_PROPRIETARY_POLICY = {
    "name": "proprietary",
    "types_error": ["proprietary", "source-available", "noncommercial", "copyleft"],
    "types_warn": ["permissive-with-conditions"],
    "licenses": {"error": [], "warn": ["unknown"]},
    "warn_non_opensource_licenses": False,
    "warn_unprofessional_licenses": True,
    "warn_deprecated_licenses": True,
    "reasons": {
        "proprietary": "Proprietary licenses should not be used in Proprietary projects without explicit permission",
        "source-available": "source-available licenses should not be used in Proprietary projects, unless you are sharing source",
        "noncommercial": "Noncommercial licenses should not be used in Proprietary projects without explicit permission",
        "copyleft": "Strong Copyleft licenses should not be used in Proprietary projects",
        "permissive-with-conditions": "Permissive licenses with conditions should be manually checked to ensure compliance",
    },
}

LICENSE_PERMISSIVE_POLICY = {
    "name": "permissive opensource",
    "types_error": ["proprietary", "copyleft"],
    "types_warn": ["permissive-with-conditions"],
    "licenses": {"error": [], "warn": ["unknown"]},
    "warn_non_opensource_licenses": False,
    "warn_unprofessional_licenses": True,
    "warn_deprecated_licenses": True,
    "reasons": {
        "proprietary": "Proprietary licenses should not be used in Opensource projects",
        "copyleft": "Strong Copyleft licenses should not be used in permissive opensource projects",
        "permissive-with-conditions": "Permissive licenses with conditions should be manually checked to ensure compliance",
    },
}

LICENSE_OPENSOURCE_POLICY = {
    "name": "copyleft opensource",
    "types_error": ["proprietary"],
    "types_warn": ["permissive-with-conditions"],
    "licenses": {"error": ["unknown"], "warn": []},
    "warn_non_opensource_licenses": True,
    "warn_unprofessional_licenses": True,
    "warn_deprecated_licenses": True,
    "reasons": {
        "proprietary": "Proprietary licenses should not be used in Opensource projects",
        "permissive-with-conditions": "Permissive licenses with conditions should be manually checked to ensure compliance",
    },
}

LICENSE_OFF_POLICY = {
    "name": "-",
    "types_error": [],
    "types_warn": [],
    "warn_non_opensource_licenses": False,
    "warn_unprofessional_licenses": False,
    "warn_deprecated_licenses": False,
}

GLOBAL_REASONS = {
    "license_type_unknown": "Components with unknown license types should be manually checked to ensure compliance",
    "license_unknown": "Components with unknown licenses should be manually checked to ensure compliance",
    "warn_non_opensource_licenses": "Unable to determine if license is fsf/osi opensource approved",
    "warn_unprofessional_licenses": "Components with unprofessional licenses should be avoided in Professional projects",
    "warn_deprecated_licenses": "Components with deprecated licenses should be avoided in Professional projects",
}


LICENSE_CHECK_CONFIG = {
    "type": str,
    "default": LicenseScanType.PROPRIETARY.value,
    "help_text": """available modes:
- PROPRIETARY : for commercial projects, check for non-commercial, strong-copyleft, and source-available licenses
- PERMISSIVE : for permissive open source projects (aka MIT, LGPL), check for strong-copyleft licenses
- OPENSOURCE : for copyleft open source projects (aka GPL), check for non-OSI or FsfLibre certified licenses
- OFF : no license checks
All modes will also warn on "unprofessional", "deprecated", and "permissive with conditions" licenses""",
    "help_example": "PROPRIETARY",
}

LICENSE_ALLOWLIST_CONFIG = {
    "type": list,
    "default": [],
    "help_text": """list of licenses to exempt from license checks""",
    "help_example": ["MIT-enna"],
}

LICENSE_DENYLIST_CONFIG = {
    "type": list,
    "default": [],
    "help_text": """list of licenses to always report usage as a error""",
    "help_example": ["MIT-enna"],
}


class Cache:
    """Cache class container"""


__c = Cache()
__c.licenses_data = None


def get_licenses_data() -> dict:
    """get license data from eze/data/license_data/spdx-license-list-data-supplement.json"""
    if not __c.licenses_data:
        file_dir = os.path.dirname(__file__)
        fixture_path = Path(file_dir) / ".." / "data" / "license_data" / "spdx-license-list-data-supplement.json"
        __c.licenses_data = load_json(fixture_path)
    return __c.licenses_data


def normalise_license_id(license_text: str) -> str:
    """normalise license id"""

    def _normalise_license_id(matches):
        return matches.group(1) + "-" + matches.group(2)

    return re.sub("^\\s*([a-zA-Z]+)[- _]+([0-9]+(?:[.][0-9.]+)?)\\s*$", _normalise_license_id, license_text)


def convert_pypi_to_spdx(pypi_license: str) -> str:
    """convert pypi license code aka "License :: OSI Approved :: BSD License" into spdx code "BSD" """
    licenses_data = get_licenses_data()
    pypi_lookup_table: dict = py_.get(licenses_data, "pypiToSpdxLookup", {})
    return pypi_lookup_table.get(pypi_license) or None


def get_bom_license(license_dict: dict) -> str:
    """Parse cyclonedx component object for normalised license"""
    license_text = py_.get(license_dict, "license.name")
    if not license_text:
        license_text = py_.get(license_dict, "license.id")
    if not license_text:
        license_text = py_.get(license_dict, "license.url")
    if license_text:
        # normalise upper and lower case unknown entries
        if license_text.lower() == "unknown":
            license_text = "unknown"
    return license_text


def get_license(license_text: str) -> dict:
    """get license data from eze/data/license_data/spdx-license-list-data-supplement.json"""
    licenses_data = get_licenses_data()

    # by spdx short code, aka "MIT"
    license_id = normalise_license_id(license_text)
    if license_id in licenses_data["licenses"]:
        return licenses_data["licenses"][license_id]
    # by pypi long code, aka "License :: OSI Approved :: MIT License"
    pypi_license_id = convert_pypi_to_spdx(license_text)
    if pypi_license_id:
        if pypi_license_id in licenses_data["licenses"]:
            return licenses_data["licenses"][pypi_license_id]
        if pypi_license_id in licenses_data["licensesPatterns"]:
            license_data = licenses_data["licensesPatterns"][pypi_license_id]
            created_license_data = license_data.copy()
            created_license_data["id"] = pypi_license_id
            created_license_data["isOsiApproved"] = ":: OSI Approved ::" in license_text
            created_license_data["isFsfLibre"] = None
            created_license_data["isDeprecated"] = None
            return created_license_data
    # by name, aka "MIT License"
    for key in licenses_data["licenses"]:
        license_data = licenses_data["licenses"][key]
        if license_text == license_data["name"]:
            return license_data
    # by url, aka microsoft's "http://go.microsoft.com/fwlink/?LinkId=329770"
    if license_text in licenses_data["licensesUrls"]:
        license_data = licenses_data["licensesUrls"][license_text]
        created_license_data = license_data.copy()
        created_license_data["isOsiApproved"] = None
        created_license_data["isFsfLibre"] = None
        created_license_data["isDeprecated"] = None
        return created_license_data
    # by pattern, aka "Apache-X.X lorem ipsum facto"
    for license_pattern in licenses_data["licensesPatterns"]:
        license_data = licenses_data["licensesPatterns"][license_pattern]
        if re.match(license_pattern, license_text):
            created_license_data = license_data.copy()
            created_license_data["id"] = license_text
            created_license_data["isOsiApproved"] = None
            created_license_data["isFsfLibre"] = None
            created_license_data["isDeprecated"] = None
            return created_license_data
    return None


def annotated_sbom_table(cyclonedx_bom: dict, print_transitive: bool = False) -> list:
    """annotated and sorted sboms table data"""
    sbom_components = annotate_licenses(cyclonedx_bom)
    sboms = []
    for sbom_component in sbom_components:
        if not print_transitive and sbom_component.is_transitive:
            continue
        sboms.append(
            {
                "type": sbom_component.type,
                "name": sbom_component.name,
                "version": sbom_component.version,
                "license": sbom_component.license,
                "license type": sbom_component.license_type,
                "description": truncate(sbom_component.description),
            }
        )
    sboms = sorted(sboms, key=lambda d: d["name"])
    return sboms


def annotate_licenses(sbom: dict) -> list:
    """return components list with annotations for transitive and licenses for violations of policies"""
    sbom_components = []
    for component in py_.get(sbom, "components", []):
        # manual parsing for name and id
        component_name = component["name"]
        component_group = component.get("group")
        if component_group:
            component_name = f"{component_group}.{component_name}"

        # manual parsing for license
        licenses = component.get("licenses", [])
        license_id = None
        if licenses and len(licenses) > 0:
            license_texts = []
            for license_obj in licenses:
                license_id = get_bom_license(license_obj)
                if license_id:
                    license_texts.append(license_id)
            if len(license_texts) > 1:
                log_error(
                    f"found multiple licenses for component '{component_name}', licenses: '{', '.join(license_texts)}', using '{license_id}'"
                )
        sbom_component = Component(
            {
                "type": component["type"],
                "name": component_name,
                "version": component["version"],
                "license": license_id,
                "description": component.get("description", ""),
                "is_transitive": py_.get(component, "properties.transitive", False),
            }
        )
        if not license_id:
            license_id = "unknown"
        license_data = get_license(license_id)
        if license_data:
            sbom_component.license = license_data["id"]
            sbom_component.license_type = license_data["type"]
            sbom_component.license_is_professional = license_data["isProfessional"]
            sbom_component.license_is_osi_approved = license_data["isOsiApproved"]
            sbom_component.license_is_fsf_libre = license_data["isFsfLibre"]
            sbom_component.license_is_deprecated = license_data["isDeprecated"]
        sbom_components.append(sbom_component)
    return sbom_components


def get_policy(license_policy: str) -> dict:
    """get description violation of policies"""
    # TODO: AB#943: auto detect project license from root LICENSE.md
    license_policy = license_policy.upper()
    if license_policy == LicenseScanType.PROPRIETARY.value:
        return LICENSE_PROPRIETARY_POLICY
    if license_policy == LicenseScanType.PERMISSIVE.value:
        return LICENSE_PERMISSIVE_POLICY
    if license_policy == LicenseScanType.OPENSOURCE.value:
        return LICENSE_OPENSOURCE_POLICY
    if license_policy == LicenseScanType.OFF.value:
        return LICENSE_OFF_POLICY
    # Default
    return LICENSE_PROPRIETARY_POLICY


def check_licenses(
    sbom: dict, license_policy: str, allowlist: list = None, denylist: list = None, project: str = "sbom"
) -> tuple:
    """check licenses for violations of policies"""
    allowlist = allowlist if allowlist else []
    denylist = denylist if denylist else []
    license_risks = []
    code_smells = []
    warnings = []
    policy = get_policy(license_policy)
    sbom_components = annotate_licenses(sbom)

    has_data: bool = False
    for sbom_component in sbom_components:
        sbom_component: Component = sbom_component
        if sbom_component.license and sbom_component.license != "unknown":
            has_data = True
            break

    if not has_data:
        warnings.append("unable to check licenses, no valid license information in sboms")
        return [license_risks, code_smells, warnings]

    for sbom_component in sbom_components:
        sbom_component: Component = sbom_component
        if sbom_component.license in allowlist:
            continue
        if sbom_component.license in denylist:
            license_risks.append(
                LicenseRiskVO(
                    {
                        "name": f"License {sbom_component.license}({sbom_component.name}), not allowed",
                        "overview": f"{sbom_component.license} in project license_denylist",
                        "file_location": {"path": project, "line": 1},
                    }
                )
            )
            continue
        if sbom_component.license_type in policy["types_error"]:
            license_risks.append(
                LicenseRiskVO(
                    {
                        "name": f"Invalid License {sbom_component.license}({sbom_component.name}), {sbom_component.license_type} license in {policy['name']} project",
                        "overview": policy["reasons"][sbom_component.license_type],
                        "file_location": {"path": project, "line": 1},
                    }
                )
            )
        if sbom_component.license_type in policy["types_warn"]:
            text: str = f"License '{sbom_component.license}'({sbom_component.name})[{project}], reason: {policy['reasons'][sbom_component.license_type]}"
            code_smells.append(
                SmellVO(
                    {
                        "name": text,
                        "overview": text,
                        "file_location": {"path": project, "line": 1},
                        "severity": SmellSeverityEnum.warning.name,
                    }
                )
            )
        if (
            policy["warn_non_opensource_licenses"]
            and not sbom_component.license_is_fsf_libre
            and not sbom_component.license_is_osi_approved
        ):
            text: str = f"License '{sbom_component.license}'({sbom_component.name})[{project}], reason: {GLOBAL_REASONS['warn_non_opensource_licenses']}"
            code_smells.append(
                SmellVO(
                    {
                        "name": text,
                        "overview": text,
                        "file_location": {"path": project, "line": 1},
                        "severity": SmellSeverityEnum.warning.name,
                    }
                )
            )
        if policy["warn_unprofessional_licenses"] and not sbom_component.license_is_professional:
            notes = py_.get(sbom_component, "notes", "")
            text: str = f"License '{sbom_component.license}'({sbom_component.name})[{project}], reason: {GLOBAL_REASONS['warn_unprofessional_licenses']}{notes}"
            code_smells.append(
                SmellVO(
                    {
                        "name": text,
                        "overview": text,
                        "file_location": {"path": project, "line": 1},
                        "severity": SmellSeverityEnum.warning.name,
                    }
                )
            )
        if policy["warn_deprecated_licenses"] and sbom_component.license_is_deprecated:
            text: str = f"License '{sbom_component.license}'({sbom_component.name})[{project}], reason: {GLOBAL_REASONS['warn_deprecated_licenses']}"
            code_smells.append(
                SmellVO(
                    {
                        "name": text,
                        "overview": text,
                        "file_location": {"path": project, "line": 1},
                        "severity": SmellSeverityEnum.warning.name,
                    }
                )
            )
    return (license_risks, code_smells, warnings)
