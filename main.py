from argparse import ArgumentParser
import os

from minimum_dependency_generator import generate_min_requirements

def main():
    parser = ArgumentParser(description="reads a requirements file and outputs the minimized requirements")
    parser.add_argument('--requirements_paths', nargs='+',
                        help='path for requirements to minimize', required=True)
    args = parser.parse_args()
    requirements = generate_min_requirements(args.requirements_paths)
    print(requirements)
    requirements = sanitize_string(requirements)
    print(requirements)
    # DO NOT remove, the GH action needs to output
    os.environ['MIN_REQS'] = requirements
    print("::set-output name=content::{}".format(requirements))
    return

def sanitize_string(s):
    return s.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")

if __name__ == '__main__':
    main()