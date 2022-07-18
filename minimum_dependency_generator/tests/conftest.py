import pytest


@pytest.fixture(scope="session", autouse=True)
def pandas_dep():
    return "pandas>=0.24.1,<2.0.0,!=1.1.0,!=1.1.1"


@pytest.fixture(scope="session", autouse=True)
def woodwork_dep():
    return "woodwork==0.0.11"


@pytest.fixture(scope="session", autouse=True)
def dask_dep():
    return "dask[dataframe]>=2.30.0,<2012.12.0"


@pytest.fixture(scope="session", autouse=True)
def ploty_dep():
    return "plotly>=4.14.0"


@pytest.fixture(scope="session", autouse=True)
def numpy_lower():
    return "numpy>=1.15.4"


@pytest.fixture(scope="session", autouse=True)
def numpy_upper():
    return "numpy<1.20.0"


@pytest.fixture(scope="session", autouse=True)
def other_req_path():
    return "-r core-requirements.txt"


@pytest.fixture(scope="session", autouse=True)
def setuptools():
    return "setuptools >= 47"


@pytest.fixture(scope="session", autouse=True)
def p_ytest_dep():
    return "pytest >= 5.2.0"


@pytest.fixture(scope="session", autouse=True)
def scipy_lower():
    return "scipy >= 1.3.3"


@pytest.fixture(scope="session", autouse=True)
def scipy_even_higher():
    return "scipy >= 1.5.0"


@pytest.fixture(scope="session", autouse=True)
def cfg_str(
    dask_dep, pandas_dep, woodwork_dep, numpy_lower, ploty_dep, numpy_upper, p_ytest_dep
):
    setup_cfg_str = f"""\
    [metadata]
    name = example_package

    [options]
    install_requires =
        {dask_dep}
        {pandas_dep}
        {woodwork_dep}
        {numpy_lower}

    [options.extras_require] =
    dev =
        {ploty_dep}
        {numpy_upper}
    test =
        {p_ytest_dep}
    """
    return setup_cfg_str


@pytest.fixture(scope="session", autouse=True)
def toml_cfg(
    pandas_dep, woodwork_dep, numpy_upper, ploty_dep, p_ytest_dep, dask_dep, numpy_lower
):
    pyproject_str = f"""\
    [project]
    name = "example_package"
    requires-python = ">=3.7,<3.10"
    dependencies = [
        "{pandas_dep}",
        "{woodwork_dep}",
        "{numpy_upper}",
    ]

    [project.optional-dependencies]
    test = [
        "{ploty_dep}",
        "{p_ytest_dep}",
    ]
    dev = [
        "{dask_dep}",
        "{numpy_lower}",
    ]
    """
    return pyproject_str
