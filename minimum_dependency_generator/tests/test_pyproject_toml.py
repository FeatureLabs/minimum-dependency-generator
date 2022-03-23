import tempfile

import pytest

from ..minimum_dependency_generator import generate_min_requirements

@pytest.mark.parametrize(
    "file_prefix,file_extension,options",
    [('setup', 'cfg', 'install_requires' ), ('pyproject', 'toml', 'dependencies')],
)
def test_with_toml_cfg(
    file_prefix, file_extension, options, cfg_str, toml_cfg
):
    file_str = toml_cfg
    if file_prefix == 'setup':
        file_str = cfg_str
    with tempfile.NamedTemporaryFile(
        mode="w", suffix="." + file_extension, prefix=file_prefix
    ) as pyproject_file:
        pyproject_file.write(file_str)
        pyproject_file.flush()

        paths = [pyproject_file.name]
        options = [options]
        extra_requires = ['test dev']
        min_requirements = generate_min_requirements(paths, options, extra_requires)
    verify_min_reqs_cfg_toml(min_requirements)

def verify_min_reqs_cfg_toml(min_requirements):
    assert '-r' not in min_requirements
    assert '.txt' not in min_requirements
    assert 'core-requirements.txt' not in min_requirements
    min_requirements = min_requirements.split('\n')
    assert min_requirements[-1] == ''
    min_requirements = min_requirements[:-1]
    expected_min_reqs = [
        "dask[dataframe]==2.30.0",
        "numpy==1.15.4",
        "pandas==0.24.1",
        "plotly==4.14.0",
        "pytest==5.2.0",
        "woodwork==0.0.11",
    ]
    expected_min_reqs = sorted(expected_min_reqs)
    assert len(min_requirements) == len(expected_min_reqs)
    for idx, min_req in enumerate(min_requirements):
        assert expected_min_reqs[idx] == min_req.strip()
