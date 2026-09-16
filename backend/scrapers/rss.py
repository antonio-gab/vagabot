"""Leitura pequena de feeds RSS/Atom sem dependência externa."""

from xml.etree import ElementTree


def _texto(elemento, *nomes: str) -> str:
    for nome in nomes:
        encontrado = elemento.find(nome)
        if encontrado is not None and encontrado.text:
            return encontrado.text.strip()
    return ""


def parse_feed(conteudo: bytes) -> list[dict]:
    """Extrai os campos comuns de feeds RSS 2.0 e Atom."""
    raiz = ElementTree.fromstring(conteudo)
    entradas = raiz.findall("./channel/item")
    if not entradas:
        entradas = raiz.findall("{http://www.w3.org/2005/Atom}entry")

    resultado = []
    for entrada in entradas:
        atom = entrada.tag.startswith("{")
        prefixo = "{http://www.w3.org/2005/Atom}" if atom else ""
        link = _texto(entrada, "link")
        if atom:
            link_elemento = entrada.find(f"{prefixo}link[@rel='alternate']")
            if link_elemento is None:
                link_elemento = entrada.find(f"{prefixo}link")
            link = link_elemento.get("href", "") if link_elemento is not None else ""
        resultado.append({
            "title": _texto(entrada, f"{prefixo}title", "title"),
            "link": link,
            "summary": _texto(entrada, f"{prefixo}summary", f"{prefixo}content", "description"),
            "published": _texto(entrada, f"{prefixo}published", f"{prefixo}updated", "pubDate"),
            "author": _texto(entrada, "author", f"{prefixo}author"),
        })
    return resultado
