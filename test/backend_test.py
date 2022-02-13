import sys

sys.path.append('..')
from src.base_dataclass import prateleira, estantes


def test_prateleira():
    for index, estante in enumerate(estantes.split()):
        assert prateleira[estante] == index
