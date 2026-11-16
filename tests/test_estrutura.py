import importlib

import pytest


@pytest.mark.parametrize("modulo", ["coletor", "parser", "pipeline"])
def test_pacotes_importam(modulo: str) -> None:
    assert importlib.import_module(modulo).__doc__
