from argparse import ArgumentParser

from minimum_dependency_generator import generate_min_requirements

def main():
    parser = ArgumentParser(description="reads a requirements file and outputs the minimized requirements")
    parser.add_argument('--requirements_paths', nargs='+',
                        help='path for requirements to minimize', required=True)
    args = parser.parse_args()
    requirements = generate_min_requirements(args.requirements_paths)
    return

if __name__ == '__main__':
    main()