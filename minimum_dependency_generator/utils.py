from packaging.requirements import Requirement
from packaging.specifiers import Specifier


def create_strict_min(package_version):
    return Specifier("==" + package_version)


def verify_python_environment(requirement):
    package = Requirement(requirement)
    if not package.marker:
        # no python version specified in requirement
        return True
    elif package.marker and package.marker.evaluate():
        # evaluate --> evaluating the given marker against the current Python process environment
        return True
    return False


def remove_comment(requirement):
    if "#" in requirement:
        # remove everything after comment character
        requirement = requirement.split("#")[0]
    return requirement


def is_requirement_path(requirement):
    if '.txt' in requirement and '-r' in requirement:
        return True
    return False


def find_operator_version(package, operator):
    version = None
    for x in package.specifier:
        if x.operator == operator:
            version = x.version
            break
    return version


def determine_package_name(package):
    name = package.name
    if len(package.extras) > 0:
        name = package.name + "[" + package.extras.pop() + "]"
    return name


def clean_cfg_section(section):
    section = section.split('\n')
    section = [x for x in section if len(x) > 1]
    return section


def verify_list(item):
    if not isinstance(item, list):
        item = list(item)
    return item
