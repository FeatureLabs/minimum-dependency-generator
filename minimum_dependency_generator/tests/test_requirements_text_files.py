import tempfile

from ..minimum_dependency_generator import generate_min_requirements


def test_with_requirements_texts(
    ploty_dep,
    dask_dep,
    pandas_dep,
    woodwork_dep,
    numpy_upper,
    numpy_lower,
    other_req_path,
    scipy_lower,
    scipy_even_higher,
):
    min_requirements = []
    requirements_core = "\n".join(
        [dask_dep, pandas_dep, woodwork_dep, numpy_upper, scipy_lower]
    )
    requirements_koalas = "\n".join(
        [ploty_dep, numpy_lower, other_req_path, scipy_even_higher]
    )
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", prefix="out_requirements"
    ) as _:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", prefix="core_requirements"
        ) as core_f:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", prefix="koalas_requirements"
            ) as koalas_f:
                core_f.writelines(requirements_core)
                core_f.flush()
                koalas_f.writelines(requirements_koalas)
                koalas_f.flush()
                paths = [core_f.name, koalas_f.name]
                paths = [" ".join(paths)]
                min_requirements = generate_min_requirements(paths=paths)
                assert isinstance(min_requirements, str)
    assert "-r" not in min_requirements
    assert ".txt" not in min_requirements
    assert "core-requirements.txt" not in min_requirements
    min_requirements = min_requirements.split("\n")
    assert min_requirements[-1] == ""
    min_requirements = min_requirements[:-1]
    expected_min_reqs = [
        "dask[dataframe]==2.30.0",
        "numpy==1.15.4",
        "pandas==0.24.1",
        "plotly==4.14.0",
        "woodwork==0.0.11",
        "scipy==1.5.0",
    ]
    expected_min_reqs = sorted(expected_min_reqs)
    assert len(min_requirements) == len(expected_min_reqs)
    for idx, min_req in enumerate(min_requirements):
        assert expected_min_reqs[idx] == min_req.strip()
