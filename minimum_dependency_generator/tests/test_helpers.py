import sys

import pytest
from packaging.specifiers import Specifier

from ..minimum_dependency_generator import find_min_requirement


def test_lower_bound(ploty_dep):
    mininum_package = find_min_requirement(ploty_dep)
    verify_mininum(mininum_package, "plotly", "4.14.0")
    mininum_package = find_min_requirement("plotly>=4.14")
    verify_mininum(mininum_package, "plotly", "4.14")


def test_lower_upper_bound(dask_dep):
    mininum_package = find_min_requirement("xgboost>=0.82,<1.3.0")
    verify_mininum(mininum_package, "xgboost", "0.82")
    mininum_package = find_min_requirement(dask_dep)
    verify_mininum(mininum_package, "dask", "2.30.0", required_extra="dataframe")


def test_spacing():
    mininum_package = find_min_requirement("statsmodels >= 0.12.2")
    verify_mininum(mininum_package, "statsmodels", "0.12.2")


def test_marker():
    mininum_package = find_min_requirement('sktime>=0.5.3;python_version<"3.9"')
    verify_mininum(mininum_package, "sktime", "0.5.3")


def test_upper_bound():
    error_text = "Operator does not exist or is an invalid operator"
    with pytest.raises(ValueError, match=error_text):
        find_min_requirement("xgboost<1.3.0")
    with pytest.raises(ValueError, match=error_text):
        find_min_requirement("colorama")


def test_other_requirement(other_req_path):
    mininum_package = find_min_requirement(other_req_path)
    assert mininum_package is None


def test_bound(woodwork_dep):
    mininum_package = find_min_requirement(woodwork_dep)
    verify_mininum(mininum_package, "woodwork", "0.0.11")


def test_extra_require():
    mininum_package = find_min_requirement("dask>=2.30.0")
    verify_mininum(mininum_package, "dask", "2.30.0", required_extra=None)
    mininum_package = find_min_requirement("dask[dataframe]<2012.12.0,>=2.30.0")
    verify_mininum(mininum_package, "dask", "2.30.0", required_extra="dataframe")


def test_comments():
    mininum_package = find_min_requirement(
        "pyspark>=3.0.0 ; python_version!='3.9' # comment here"
    )
    verify_mininum(mininum_package, "pyspark", "3.0.0")


def test_complex_bound(pandas_dep):
    mininum_package = find_min_requirement(pandas_dep)
    verify_mininum(mininum_package, "pandas", "0.24.1")


def test_wrong_python_env():
    mininum_package = find_min_requirement("ipython==7.16.0; python_version=='3.4'")
    assert mininum_package is None
    python_version = str(sys.version_info.major) + "." + str(sys.version_info.minor)
    mininum_package = find_min_requirement(
        "ipython==7.16.0; python_version=='" + python_version + "'"
    )
    verify_mininum(mininum_package, "ipython", "7.16.0")


def verify_mininum(
    mininum_package,
    required_package_name,
    required_mininum_version,
    operator="==",
    required_extra=None,
):
    assert mininum_package.name == required_package_name
    assert mininum_package.specifier == Specifier(operator + required_mininum_version)
    if required_extra:
        assert mininum_package.extras == {required_extra}
    else:
        assert mininum_package.extras == set()
        extra_chars = ["[", "]"]
        not any([x in mininum_package.name for x in extra_chars])
        assert not any([x in required_package_name for x in extra_chars])
