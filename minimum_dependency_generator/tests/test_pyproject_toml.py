import tempfile

from ..minimum_dependency_generator import generate_min_requirements
from .test_setup_cfg import verify_min_reqs_cfg_toml


def test_with_pyproject_toml(
    dask_dep, pandas_dep, woodwork_dep, numpy_lower, ploty_dep, numpy_upper, p_ytest_dep
):
    pyproject_str = f'''\
    [project]
    name = "example_package"
    requires-python = ">=3.7,<3.10"
    dependencies = [
        "{dask_dep}",
        "{pandas_dep}",
        "{woodwork_dep}",
        "{numpy_lower}",
    ]

    [project.optional-dependencies]
    test = [
        "{ploty_dep}",
        "{p_ytest_dep}",
    ]
    dev = [
        "{numpy_upper}",
    ]
    '''
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".toml", prefix="pyproject"
    ) as pyproject_file:
        pyproject_file.write(pyproject_str)
        pyproject_file.flush()

        paths = [pyproject_file.name]
        options = ['dependencies']
        extra_requires = ['test']
        min_requirements = generate_min_requirements(paths, options, extra_requires)
    verify_min_reqs_cfg_toml(min_requirements)
