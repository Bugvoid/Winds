"""Sonda descartável: registra o código HTTP da fonte B3 a partir de onde roda.

Faz poucas requisições, uma por vez, com um User-Agent que identifica o projeto.
Não tenta contornar bloqueio: só registra o que cada chamada devolve.
"""
import base64
import json
import re
import time
import urllib.error
import urllib.request

UA = "winds-coletor/0.1 (+https://github.com/Bugvoid/Winds)"
PLANTAO = "https://sistemasweb.b3.com.br/PlantaoNoticias/Noticias"
LISTADOS = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall"


def b64(obj):
    return base64.b64encode(json.dumps(obj).encode()).decode()


def get(nome, url, ua=UA):
    headers = {"User-Agent": ua} if ua else {}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            status, corpo = r.status, r.read()
    except urllib.error.HTTPError as e:
        status, corpo = e.code, e.read()
    except Exception as e:  # noqa: BLE001
        print(f"{nome}: ERRO {type(e).__name__}: {e}")
        return None, b""
    texto = corpo.decode("utf-8", "replace")
    tem_pre = bool(re.search(r'<pre[^>]*id="conteudoDetalhe"', texto))
    cf = "Cloudflare" in texto[:2000]
    print(f"{nome}: HTTP {status}, {len(corpo)} bytes, pre={tem_pre}, pagina_cloudflare={cf}")
    time.sleep(2)
    return status, corpo


def main():
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=20) as r:
            print("IP de saida:", r.read().decode())
    except Exception as e:  # noqa: BLE001
        print("IP de saida: indisponivel", e)

    _, corpo = get(
        "listagem",
        f"{PLANTAO}/ListarTitulosNoticias?agencia=18&palavra=Proventos"
        "&dataInicial=2026-11-10&dataFinal=2026-11-16",
    )
    detalhe = (
        f"{PLANTAO}/Detail?idNoticia=3556774&agencia=18"
        "&dataNoticia=2026-11-16%2008%3A43%3A01"
    )
    try:
        item = json.loads(corpo)[0]["NwsMsg"]
        print("primeira manchete:", item["headline"])
    except Exception as e:  # noqa: BLE001
        print("listagem nao e JSON:", e)
    for i in range(1, 4):
        get(f"detalhe (UA identificado), tentativa {i}", detalhe)
        time.sleep(5)
    get("detalhe (UA padrao do urllib)", detalhe, ua=None)
    get("indice (UA identificado)", f"{PLANTAO}/Index")

    _, corpo = get(
        "listados: proventos em dinheiro CURY",
        f"{LISTADOS}/GetListedCashDividends/"
        + b64({"language": "pt-br", "pageNumber": 1, "pageSize": 20, "tradingName": "CURY"}),
    )
    print("  amostra:", corpo[:400].decode("utf-8", "replace"))
    _, corpo = get(
        "listados: suplemento CURY",
        f"{LISTADOS}/GetListedSupplementCompany/"
        + b64({"issuingCompany": "CURY", "language": "pt-br"}),
    )
    print("  amostra:", corpo[:400].decode("utf-8", "replace"))


if __name__ == "__main__":
    main()
