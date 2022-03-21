import configparser
import os
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


def find_min_requirement(requirement, python_version="3.7", major_python_version="py3"):
    if is_requirement_path(requirement):
        # skip requirement paths
        # ex '-r core_requirements.txt'
        return
    requirement = remove_comment(requirement)
    if not verify_python_environment(requirement):
        return
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
            "Operator does not exist or is an invalid operator (such as '<'). Please specify the mininum version ('>=', '==')."
        )
    name = determine_package_name(package)
    min_requirement = Requirement(name + str(mininum))
    return min_requirement


def clean_list_length_one(item):
    if isinstance(item, list) and len(item) == 1 and ' ' in item[0]:
        item = item[0].split(' ')
    if item == ['']:
        return None
    return item


def parse_requirements_text_file(paths):
    requirements = []
    paths = clean_list_length_one(paths)

    for path in paths:
        with open(path) as f:
            requirements.extend(f.readlines())
    return requirements


def parse_setup_cfg(paths, options, extras_require):
    config = configparser.ConfigParser()
    config.read(paths[0])

    requirements = []
    options = clean_list_length_one(options)
    extras_require = clean_list_length_one(extras_require)
    if options and len(options) > 0:
        for option in options:
            requirements += clean_cfg_section(config['options'][option])
    if extras_require and len(extras_require) > 0:
        for extra in extras_require:
            requirements += clean_cfg_section(config['options.extras_require'][extra])
    return requirements


def generate_min_requirements(paths, options=None, extras_require=None, output_filepath=None):
    requirements_to_specifier = defaultdict(list)
    min_requirements = []

    if len(paths) == 1 and paths[0].endswith('.cfg') and os.path.basename(paths[0]).startswith('setup'):
        requirements = parse_setup_cfg(paths, options, extras_require)
    else:
        requirements = parse_requirements_text_file(paths)

    for req in requirements:
        if is_requirement_path(req):
            # skip requirement paths
            # ex '-r core_requirements.txt'
            continue
        package = Requirement(remove_comment(req))
        name = determine_package_name(package)
        if name in requirements_to_specifier:
            prev_req = Requirement(requirements_to_specifier[name])
            new_req = prev_req.specifier & package.specifier
            requirements_to_specifier[name] = name + str(new_req)
        else:
            requirements_to_specifier[name] = name + str(package.specifier)

    for req in list(sorted(requirements_to_specifier.values())):
        min_package = find_min_requirement(req)
        min_requirements.append(str(min_package))
    min_requirements = '\n'.join(min_requirements) + '\n'
    if output_filepath:
        write_file(min_requirements, output_filepath)
    return min_requirements


def write_file(data, filepath):
    try:
        with open(filepath, 'w') as f:
            f.write(data)
    except OSError:
        print("Error writing file")
        exit(1)
