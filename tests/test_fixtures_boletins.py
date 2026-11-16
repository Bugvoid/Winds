"""Integridade das fixtures reais da B3 em parser/fixtures/."""

import json
import re
from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parent.parent / "parser" / "fixtures"
BOLETINS = sorted((FIXTURES / "boletins").glob("Proventos-*.txt"))
NOME = re.compile(r"Proventos-(\d{4})-(\d{2})-(\d{2})-(\d+)\.txt")
MANCHETE = 'PROVENTOS DOS EMISSORES DEPOSITADOS NA FORMA "EX": {d}/{m}/{a}'


def test_ha_boletins_reais() -> None:
    assert len(BOLETINS) >= 20


@pytest.mark.parametrize("arquivo", BOLETINS, ids=lambda p: p.name)
def test_boletim_bem_formado(arquivo: Path) -> None:
    nome = NOME.fullmatch(arquivo.name)
    assert nome, arquivo.name
    a, m, d, _ = nome.groups()
    bruto = arquivo.read_bytes()
    assert b"\r" not in bruto
    texto = bruto.decode("utf-8")
    linhas = texto.split("\n")
    assert linhas[0].strip() == MANCHETE.format(d=d, m=m, a=a)
    assert any(linha.startswith("EMPRESA:") for linha in linhas)
    assert max(len(linha) for linha in linhas) <= 80
    assert not re.search(r"&(?:[a-z]+|#\d+);", texto), "entidade HTML não decodificada"


def test_listagem_cobre_os_boletins() -> None:
    listagem = json.loads(
        (FIXTURES / "listagem-2026-10-17_2026-11-16.json").read_text(encoding="utf-8")
    )
    ids = {item["NwsMsg"]["id"] for item in listagem}
    assert {int(NOME.fullmatch(p.name).group(4)) for p in BOLETINS} <= ids
