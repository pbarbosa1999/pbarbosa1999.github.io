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
