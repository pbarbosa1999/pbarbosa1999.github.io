# Meu Site Jekyll

Site simples criado com [Jekyll](https://jekyllrb.com/) e o tema padrão
**minima**, incluindo uma seção de blog.

## Estrutura

```
.
├── _config.yml      # configurações do site
├── _posts/          # posts do blog (Markdown)
├── index.md         # página inicial (lista os posts)
├── Gemfile          # dependências Ruby (Jekyll + minima)
└── .gitignore
```

## Como rodar localmente

```bash
bundle install
bundle exec jekyll serve
```

Depois acesse [http://localhost:4000](http://localhost:4000).

## Como criar um novo post

Adicione um arquivo em `_posts/` no formato:

```
AAAA-MM-DD-titulo-do-post.md
```

com o seguinte cabeçalho no topo:

```yaml
---
layout: post
title: "Título do post"
date: AAAA-MM-DD HH:MM:SS -0300
categories: geral
---
```

## Post semanal automático sobre a NR1

Este repositório inclui uma automação que, uma vez por semana, busca uma
notícia recente sobre a NR1, gera um artigo original (pensado para SEO)
usando a API da Claude, e publica em `_posts/` automaticamente via GitHub
Actions.

### Configuração (uma vez só)

1. Crie uma chave de API em [console.anthropic.com](https://console.anthropic.com/).
2. No GitHub, vá em **Settings → Secrets and variables → Actions** do
   repositório e crie um secret chamado `ANTHROPIC_API_KEY` com essa chave.
3. Pronto — o workflow em `.github/workflows/weekly-post.yml` já está
   configurado para rodar toda segunda-feira às 08h (horário de Brasília).

Você também pode disparar manualmente pela aba **Actions → Post semanal
automático (NR1) → Run workflow**, sem esperar a próxima segunda.

### Rodar localmente (opcional, para testar)

```bash
export ANTHROPIC_API_KEY="sua-chave-aqui"
pip install -r scripts/requirements.txt
python scripts/fetch_and_generate_post.py
```

Isso cria um novo arquivo em `_posts/` (não faz commit/push sozinho quando
rodado localmente — isso só acontece dentro do GitHub Actions).

### Como funciona por baixo dos panos

- `scripts/fetch_and_generate_post.py` busca notícias no Google News RSS
  para alguns termos relacionados à NR1, evita repetir links já usados
  (controlados em `data/posted_urls.json`), e manda a notícia mais recente
  para a API da Claude gerar um artigo original — nunca republica a
  notícia como está, o que evitaria penalização de conteúdo duplicado no
  Google.
- O SEO técnico do site já está configurado via `jekyll-seo-tag` (meta
  tags, Open Graph) e `jekyll-sitemap` (sitemap.xml automático), além de
  um `robots.txt` na raiz.
