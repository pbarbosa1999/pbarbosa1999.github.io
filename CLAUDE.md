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
├── _config.yml       # título, descrição, tema minima, plugin jekyll-feed
├── index.md          # home (layout: home) — lista os posts automaticamente
├── _posts/
│   ├── 2026-08-04-bem-vindo-ao-blog.md
│   └── 2026-08-04-como-rodar-o-site-localmente.md
├── Gemfile            # jekyll ~> 4.3, minima ~> 2.5, jekyll-feed
├── .gitignore          # ignora _site/, caches, Gemfile.lock
└── README.md
```

## Decisões já tomadas

- Tema: **minima** (tema padrão do Jekyll), sem customizações de layout até
  agora.
- Dois posts de exemplo em `_posts/` só para a listagem da home não ficar
  vazia — podem ser removidos ou editados livremente.
- `baseurl` e `url` em `_config.yml` estão vazios de propósito, pensando em
  publicar na raiz de um domínio/GitHub Pages (`usuario.github.io`).

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
- Ativar o GitHub Pages nas configurações do repositório, se não ativar
  sozinho.
- Personalizar `_config.yml` (nome do autor, redes sociais, título real).
- Adicionar mais posts ou páginas (ex: `about.md`).
