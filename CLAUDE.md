# Contexto do projeto — pulso-blog

Este arquivo existe para dar contexto rápido ao Claude Code sobre este
repositório. Ele é lido automaticamente ao abrir uma sessão nesta pasta.

## O que é este projeto

Site simples em **Jekyll**, usando o tema padrão **minima**, com uma seção de
blog. Foi criado do zero (sem `jekyll new`) escrevendo os arquivos
manualmente, para manter a estrutura mínima e fácil de entender.

## Estrutura atual

```
.
├── _config.yml                       # título, descrição, tema minima, plugins de SEO
├── index.md                          # home (layout: home) — lista os posts automaticamente
├── robots.txt                        # aponta pro sitemap.xml gerado pelo jekyll-sitemap
├── _posts/
│   ├── 2026-08-04-bem-vindo-ao-blog.md
│   └── 2026-08-04-como-rodar-o-site-localmente.md
├── scripts/
│   ├── fetch_and_generate_post.py    # busca notícia + gera post via API da Claude
│   └── requirements.txt
├── data/
│   └── posted_urls.json              # controle de notícias já usadas (evita duplicar)
├── .github/workflows/weekly-post.yml # roda o script 1x/semana e faz commit/push
├── Gemfile                            # jekyll ~> 4.3, minima ~> 2.5, jekyll-feed,
│                                       # jekyll-seo-tag, jekyll-sitemap
├── .gitignore                         # ignora _site/, caches, Gemfile.lock, .env
└── README.md
```

## Decisões já tomadas

- Tema: **minima** (tema padrão do Jekyll), sem customizações de layout até
  agora.
- Dois posts de exemplo em `_posts/` só para a listagem da home não ficar
  vazia — podem ser removidos ou editados livremente.
- `url` em `_config.yml` já está apontado para
  `https://pbarbosa1999.github.io` (GitHub Pages). `baseurl` continua vazio
  por ser a raiz do domínio.
- **Automação de posts semanais sobre NR1**: um workflow do GitHub Actions
  (`weekly-post.yml`) roda toda segunda-feira às 08h (BRT), busca uma
  notícia recente sobre NR1 no Google News RSS, gera um artigo original
  (não uma cópia da notícia) via API da Claude, otimizado para SEO, e
  commita o novo post em `_posts/` automaticamente.
  - A escolha de reescrever em vez de republicar a notícia foi
    deliberada: republicar notícia de terceiros como está arrisca
    penalização por conteúdo duplicado/scraper no Google.
  - `data/posted_urls.json` guarda os links já usados para não repetir a
    mesma notícia em semanas seguintes.
  - **Pendente do usuário**: cadastrar o secret `ANTHROPIC_API_KEY` no
    GitHub (Settings → Secrets and variables → Actions) para o workflow
    funcionar. Sem isso, o job falha na etapa de geração do post.
- SEO técnico já configurado: `jekyll-seo-tag` (meta tags/Open Graph),
  `jekyll-sitemap` (sitemap.xml automático) e `robots.txt` na raiz.

## Git / GitHub

- Repositório local já inicializado (`git init`), branch renomeada para
  `main`, e primeiro commit feito.
- Remote `origin` já configurado apontando para:
  `https://github.com/pbarbosa1999/pbarbosa1999.github.io.git`
- **O push ainda não foi feito** — falta rodar `git push -u origin main`
  autenticado com as credenciais do usuário (não foi feito pelo Claude por
  não ter acesso à rede/credenciais do GitHub no ambiente em que o projeto
  foi criado).
- Como o nome do repositório é `pbarbosa1999.github.io`, o GitHub Pages vai
  publicar automaticamente em `https://pbarbosa1999.github.io/` assim que o
  push acontecer, sem configuração adicional.
- Se o repositório remoto já tiver conteúdo, pode ser necessário
  `git pull origin main --allow-unrelated-histories` antes do push, ou um
  `--force` caso o usuário queira substituir o conteúdo remoto.

## Próximos passos possíveis

- Fazer o push inicial para o GitHub (ver seção acima).
- Cadastrar o secret `ANTHROPIC_API_KEY` no GitHub para a automação
  semanal funcionar (ver seção acima).
- Ativar o GitHub Pages nas configurações do repositório, se não ativar
  sozinho.
- Rodar o workflow manualmente pela primeira vez (aba Actions → Run
  workflow) para validar antes de esperar a próxima segunda-feira.
- Personalizar `_config.yml` (nome do autor, redes sociais, título real).
- Revisar/ajustar `SEARCH_TERMS` em `scripts/fetch_and_generate_post.py`
  conforme os clusters de palavra-chave que performarem melhor no Google
  Search Console.
