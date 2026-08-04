#!/usr/bin/env python3
"""
Busca notícias recentes sobre a NR1 (Google News RSS), escolhe uma que ainda
não foi usada, e gera um post original em Markdown (pensado para SEO) usando
a API da Claude. O post é salvo em _posts/ no formato que o Jekyll espera.

Variáveis de ambiente necessárias:
  ANTHROPIC_API_KEY   -> chave da API da Claude (obrigatória)

Uso:
  python scripts/fetch_and_generate_post.py
"""

import datetime
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote

import feedparser
import requests

# --------------------------------------------------------------------------
# Configuração
# --------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT_DIR / "_posts"
POSTED_LOG = ROOT_DIR / "data" / "posted_urls.json"

# Termos de busca no Google News (pt-BR). Pode ajustar/adicionar conforme os
# clusters de conteúdo que quiser cobrir.
SEARCH_TERMS = [
    "NR1 riscos psicossociais",
    "NR1 fiscalização trabalho",
    "NR1 comitê de prevenção",
]

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")

SITE_NAME = "Pulso"
SITE_TOPIC_CONTEXT = (
    "O Pulso é um portal para o setor de RH das empresas se adequarem à NR1: "
    "treinamentos, canal anônimo de denúncias, pesquisa de clima, avaliações, "
    "comitê de prevenção e certificados, tudo em um só lugar."
)


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text).strip("-")
    return text[:70].rstrip("-")


def load_posted_urls() -> set:
    if POSTED_LOG.exists():
        return set(json.loads(POSTED_LOG.read_text(encoding="utf-8")))
    return set()


def save_posted_url(url: str) -> None:
    urls = load_posted_urls()
    urls.add(url)
    POSTED_LOG.parent.mkdir(parents=True, exist_ok=True)
    POSTED_LOG.write_text(
        json.dumps(sorted(urls), ensure_ascii=False, indent=2), encoding="utf-8"
    )


# --------------------------------------------------------------------------
# 1. Buscar notícias
# --------------------------------------------------------------------------

def fetch_candidate_articles() -> list[dict]:
    posted = load_posted_urls()
    candidates = []

    for term in SEARCH_TERMS:
        url = GOOGLE_NEWS_RSS.format(query=quote(term))
        feed = feedparser.parse(url)
        for entry in feed.entries[:8]:
            link = entry.get("link", "")
            if not link or link in posted:
                continue
            candidates.append(
                {
                    "title": entry.get("title", "").strip(),
                    "link": link,
                    "published": entry.get("published", ""),
                    "summary": re.sub("<[^<]+?>", "", entry.get("summary", "")).strip(),
                    "source": entry.get("source", {}).get("title", "")
                    if isinstance(entry.get("source"), dict)
                    else "",
                }
            )

    # remove duplicados por título muito parecido (mesmo assunto em fontes diferentes)
    seen_titles = set()
    unique = []
    for c in candidates:
        key = slugify(c["title"])[:40]
        if key in seen_titles:
            continue
        seen_titles.add(key)
        unique.append(c)

    return unique


# --------------------------------------------------------------------------
# 2. Gerar o post com a API da Claude
# --------------------------------------------------------------------------

POST_GENERATION_PROMPT = """\
Você é um redator especialista em SEO e em legislação trabalhista brasileira,
escrevendo para o blog do {site_name}.

Contexto do produto: {site_context}

Abaixo está uma notícia recente sobre a NR1 (norma regulamentadora que trata
da gestão de riscos, incluindo riscos psicossociais, no ambiente de trabalho).
Use-a apenas como PONTO DE PARTIDA factual — não copie nem parafraseie de
perto o texto da notícia. Escreva um artigo ORIGINAL e aprofundado para o
blog, pensado para ranquear bem no Google.

Notícia de referência:
Título: {title}
Fonte: {source}
Resumo: {summary}
Link original: {link}

Escreva um post seguindo estas diretrizes de SEO:
- Foque em UMA palavra-chave principal relacionada à NR1 (ex: "NR1 riscos
  psicossociais", "prazo NR1", "comitê de prevenção NR1" etc. — escolha a
  mais adequada ao tema da notícia).
- Título (H1) deve conter a palavra-chave principal, ter até 60 caracteres
  e ser atrativo.
- Escreva uma meta description de até 155 caracteres, resumindo o artigo
  de forma persuasiva e contendo a palavra-chave principal.
- Estruture o corpo com subtítulos H2/H3 usando ## e ###.
- Primeiro parágrafo deve resumir o tema e responder a intenção de busca
  logo de cara (resposta direta antes de aprofundar).
- Inclua contexto prático para profissionais de RH: o que muda, prazos,
  riscos de não conformidade, e como se preparar.
- Feche o artigo com uma seção curta conectando o tema ao Pulso, sem soar
  como propaganda agressiva — foco em ajudar o leitor.
- Português do Brasil, tom profissional e direto.
- Tamanho: 500 a 800 palavras no corpo.
- NÃO invente números, multas ou leis específicas que você não tenha
  certeza; prefira linguagem geral quando o dado exato for incerto.

Responda ESTRITAMENTE em JSON válido, sem markdown ao redor, no formato:
{{
  "title": "...",
  "meta_description": "...",
  "keyword": "...",
  "categories": ["nr1", "..."],
  "body_markdown": "## Subtítulo\\n\\nConteúdo em markdown..."
}}
"""


def generate_post(article: dict) -> dict:
    if not ANTHROPIC_API_KEY:
        raise RuntimeError(
            "ANTHROPIC_API_KEY não definida. Configure essa variável de "
            "ambiente (ou secret do GitHub Actions) antes de rodar o script."
        )

    prompt = POST_GENERATION_PROMPT.format(
        site_name=SITE_NAME,
        site_context=SITE_TOPIC_CONTEXT,
        title=article["title"],
        source=article["source"] or "não informado",
        summary=article["summary"] or "não disponível",
        link=article["link"],
    )

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": ANTHROPIC_MODEL,
            "max_tokens": 3000,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    text_blocks = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
    raw_text = "\n".join(text_blocks).strip()

    # remove eventuais cercas de código, caso o modelo as inclua
    raw_text = re.sub(r"^```(json)?", "", raw_text.strip())
    raw_text = re.sub(r"```$", "", raw_text.strip())

    return json.loads(raw_text)


# --------------------------------------------------------------------------
# 3. Salvar o post em _posts/
# --------------------------------------------------------------------------

def save_post(post: dict, source_article: dict) -> Path:
    today = datetime.date.today()
    slug = slugify(post["title"])
    filename = f"{today.isoformat()}-{slug}.md"
    filepath = POSTS_DIR / filename

    categories = post.get("categories") or ["nr1"]
    categories_yaml = " ".join(categories)

    front_matter = (
        "---\n"
        "layout: post\n"
        f"title: \"{post['title'].replace(chr(34), chr(39))}\"\n"
        f"date: {today.isoformat()} 08:00:00 -0300\n"
        f"categories: {categories_yaml}\n"
        f"description: \"{post['meta_description'].replace(chr(34), chr(39))}\"\n"
        f"keyword: \"{post.get('keyword', '')}\"\n"
        "---\n\n"
    )

    footer = (
        f"\n\n---\n*Fonte de referência: [{source_article['source'] or 'notícia relacionada'}]"
        f"({source_article['link']})*\n"
    )

    filepath.write_text(front_matter + post["body_markdown"] + footer, encoding="utf-8")
    return filepath


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> None:
    print("Buscando notícias sobre NR1...")
    candidates = fetch_candidate_articles()

    if not candidates:
        print("Nenhuma notícia nova encontrada. Encerrando sem criar post.")
        sys.exit(0)

    article = candidates[0]
    print(f"Notícia escolhida: {article['title']} ({article['link']})")

    print("Gerando post com a API da Claude...")
    post = generate_post(article)

    filepath = save_post(post, article)
    save_posted_url(article["link"])

    print(f"Post criado em: {filepath.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
