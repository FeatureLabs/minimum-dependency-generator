from argparse import ArgumentParser

from minimum_dependency_generator import generate_min_requirements


def main():
    parser = ArgumentParser(description="reads a requirements file and outputs the minimized requirements")

    parser.add_argument('--paths', nargs='+',
                        help='path for requirements to minimize', required=True)

    parser.add_argument('--options', nargs='+', default=None,
                        help='path for requirements to minimize')

    parser.add_argument('--extras_require', nargs='+', default=None,
                        help='path for requirements to minimize')

    parser.add_argument('--output_filepath', default=None,
                        help='path to output minimum dependencies (optional)')

    args = parser.parse_args()
    requirements = generate_min_requirements(args.paths, args.options, args.extras_require, args.output_filepath)
    requirements = sanitize_string(requirements)
    # DO NOT remove, the GH action needs to output
    print("::set-output name=min_reqs::{}".format(requirements))


def sanitize_string(s):
    return s.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


if __name__ == '__main__':
    main()
