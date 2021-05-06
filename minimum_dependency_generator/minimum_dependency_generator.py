from collections import defaultdict

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


def find_min_requirement(requirement, python_version="3.7", major_python_version="py3"):
    requirement = remove_comment(requirement)
    if not verify_python_environment(requirement):
        return None
    if ">=" in requirement:
        # mininum version specified (ex - 'package >= 0.0.4')
        package = Requirement(requirement)
        version = find_operator_version(package, ">=")
        mininum = create_strict_min(version)
    elif "==" in requirement:
        # version strictly specified
        package = Requirement(requirement)
        version = find_operator_version(package, "==")
        mininum = create_strict_min(version)
    else:
        # mininum version not specified (ex - 'package < 0.0.4')
        # version not specified (ex - 'package')
        raise ValueError(
            "Operator does not exist or is an invalid operator. Please specify the mininum version."
        )
    name = determine_package_name(package)
    min_requirement = Requirement(name + str(mininum))
    return min_requirement


def generate_min_requirements(requirements_paths):
    requirements_to_specifier = defaultdict(list)
    min_requirements = []

    print(requirements_paths)

    if isinstance(requirements_paths, str):
        requirements_paths = requirements_paths.split(' ')
    print(requirements_paths)

    for path in requirements_paths:
        requirements = []
        with open(path) as f:
            requirements.extend(f.readlines())
        for req in requirements:
            package = Requirement(remove_comment(req))
            name = determine_package_name(package)
            if name in requirements_to_specifier:
                prev_req = Requirement(requirements_to_specifier[name])
                new_req = prev_req.specifier & package.specifier
                requirements_to_specifier[name] = name + str(new_req)
            else:
                requirements_to_specifier[name] = name + str(package.specifier)

    for req in list(requirements_to_specifier.values()):
        min_package = find_min_requirement(req)
        min_requirements.append(str(min_package))
    min_requirements = '\n'.join(min_requirements)
    return min_requirements

    # with open(output_filepath, "w") as f:
    #     f.writelines(min_requirements)
