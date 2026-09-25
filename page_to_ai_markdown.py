#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
page-to-ai-markdown — extrai o que sobra de uma página depois de remover
menu, rodapé, formulário e outros elementos de interface, e mostra o
resultado em markdown limpo: uma aproximação do que um crawler de busca com
IA (GPTBot, ClaudeBot, PerplexityBot e afins) tem para ler quando o HTML
inicial já vem renderizado no servidor.

O QUE FAZ
    Busca uma URL, remove script/style/nav/header/footer/form/aside e blocos
    comuns de ruído (menu, cookie, sidebar, redes sociais, depoimento), e
    converte o que sobra em markdown. Salva em arquivo com frontmatter
    (título, meta description, contagem de palavras) ou imprime no terminal.

    Não executa JavaScript. Se a página depende de renderização client-side
    (SPA sem SSR), o resultado mostra exatamente esse problema: pouco ou
    nenhum texto restante — o mesmo vazio que um crawler que não roda JS
    também veria.

MÉTODO
    Generalização de um script de consulta usado internamente em
    lucasferrazseo.com para poupar tokens ao ler páginas (o conteúdo vai
    para arquivo, não para o contexto de uma sessão de IA). Aqui, sem
    nenhuma regra específica de site: as classes/ids removidos são padrões
    genéricos de interface (menu, cookie, sidebar, compartilhamento).

USO
    python page_to_ai_markdown.py https://exemplo.com/pagina/
    python page_to_ai_markdown.py https://exemplo.com/pagina/ --out pagina.md
    python page_to_ai_markdown.py https://exemplo.com/pagina/ --stdout
    python page_to_ai_markdown.py https://exemplo.com/pagina/ --cache-bust

LIMITAÇÕES
    HTML puro, sem execução de JavaScript — de propósito, é o ponto da
    ferramenta. Remoção de ruído é heurística (classes/ids comuns); página
    fora do padrão pode sobrar lixo ou cortar conteúdo real.

Autor: Lucas Ferraz (lucasferraz.com).
Dependências: requests, beautifulsoup4, markdownify (ver requirements.txt).
Licença: MIT.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    from markdownify import markdownify as to_markdown
except ImportError:
    print(
        "Dependência faltando. Instale com:\n"
        "    pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(2)

UA = {"User-Agent": "page-to-ai-markdown/1.0 (+https://github.com/lucasferrazseo/page-to-ai-markdown)"}

TAGS_DESCARTADAS = ["script", "style", "noscript", "header", "footer", "nav", "form", "aside"]
CLASSES_RUIDO = re.compile(
    r"(menu|breadcrumb|cookie|offcanvas|sidebar|widget|site-header|"
    r"site-footer|related|cta|whatsapp|social|share|depoiment|review|"
    r"testimonial|avaliac|estrela)",
    re.I,
)


def escolhe_parser() -> str:
    for parser in ("lxml", "html.parser"):
        try:
            BeautifulSoup("<i></i>", parser)
            return parser
        except Exception:  # noqa: BLE001
            continue
    return "html.parser"


def com_cache_bust(url: str, ativo: bool) -> str:
    if not ativo:
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}v={int(time.time())}"


def slugifica(texto: str) -> str:
    texto = texto.strip().lower()
    trocas = [("á", "a"), ("à", "a"), ("â", "a"), ("ã", "a"), ("é", "e"),
              ("ê", "e"), ("í", "i"), ("ó", "o"), ("ô", "o"), ("õ", "o"),
              ("ú", "u"), ("ç", "c")]
    for a, b in trocas:
        texto = texto.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", texto).strip("-") or "pagina"


def nome_arquivo(url: str) -> str:
    partes = urlparse(url)
    segmentos = [s for s in partes.path.split("/") if s]
    base = segmentos[-1] if segmentos else partes.netloc.replace(".", "-")
    return slugifica(base) + ".md"


def limpa(soup: "BeautifulSoup") -> "BeautifulSoup":
    for tag in soup(TAGS_DESCARTADAS):
        tag.decompose()
    for el in soup.find_all(attrs={"class": CLASSES_RUIDO}):
        el.decompose()
    for el in soup.find_all(attrs={"id": CLASSES_RUIDO}):
        el.decompose()
    return soup.body or soup


def meta(soup: "BeautifulSoup", *seletores: dict) -> str:
    for sel in seletores:
        tag = soup.find("meta", attrs=sel)
        if tag and tag.get("content"):
            return tag["content"].strip()
    return ""


def extrai(url: str, cache_bust: bool) -> tuple[str, str, str, int]:
    resposta = requests.get(com_cache_bust(url, cache_bust), headers=UA, timeout=30)
    resposta.raise_for_status()
    soup = BeautifulSoup(resposta.text, escolhe_parser())
    titulo = (soup.title.string if soup.title else "").strip()
    descricao = meta(soup, {"name": "description"}, {"property": "og:description"})
    corpo = limpa(soup)
    md = to_markdown(str(corpo), heading_style="ATX")
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    palavras = len(md.split())
    return md, titulo, descricao, palavras


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Extrai o que sobra de uma página depois de remover interface, em markdown limpo."
    )
    ap.add_argument("url", help="URL da página")
    ap.add_argument("--out", default="", help="arquivo de saída (padrão: nome derivado da URL)")
    ap.add_argument("--stdout", action="store_true", help="imprime o markdown no terminal em vez de salvar")
    ap.add_argument("--cache-bust", action="store_true", help="adiciona ?v=timestamp na URL antes de buscar")
    args = ap.parse_args()

    try:
        md, titulo, descricao, palavras = extrai(args.url, args.cache_bust)
    except requests.RequestException as exc:
        print(f"Falha ao buscar {args.url}: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.stdout:
        print(md)
        print(f"\n--- {palavras} palavra(s) restante(s) ---", file=sys.stderr)
        return

    caminho = args.out or nome_arquivo(args.url)
    frontmatter = (
        "---\n"
        f"url: {args.url}\n"
        f"titulo: {titulo!r}\n"
        f"meta_description: {descricao!r}\n"
        f"consultado_em: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n"
        f"palavras: {palavras}\n"
        "---\n\n"
    )
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(frontmatter + md)
    print(f"{caminho} | {titulo} | {palavras} palavras restantes")


if __name__ == "__main__":
    main()
