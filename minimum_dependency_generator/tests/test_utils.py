from tempfile import NamedTemporaryFile

from ..minimum_dependency_generator import write_file


def test_write_text_file():
    reqs = ["scipy==0.8.0", "pandas==1.2.0"]
    reqs = "\n".join(reqs) + "\n"
    with NamedTemporaryFile() as temp:
        write_file(reqs, temp.name)
        with open(temp.name) as written:
            min_reqs = written.readlines()
            assert len(min_reqs) == 2
            assert "scipy==0.8.0" == min_reqs[0].strip()
            assert "pandas==1.2.0" == min_reqs[1].strip()
