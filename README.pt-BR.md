[English](README.md) · **Português (Brasil)**

# page-to-ai-markdown

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3](https://img.shields.io/badge/python-3-blue.svg)

`page-to-ai-markdown` é uma ferramenta de linha de comando gratuita e de
código aberto que busca uma URL, remove menu, rodapé, formulário e outros
elementos de interface, e mostra o que sobra em markdown limpo. É uma
aproximação do que um crawler de busca com IA (GPTBot, ClaudeBot,
PerplexityBot, OAI-SearchBot e afins) tem para ler quando o HTML inicial
já vem renderizado no servidor, sem execução de JavaScript. A página é
buscada com uma única requisição GET e processada localmente.

## Sumário

- [Contexto](#contexto)
- [Como funciona](#como-funciona)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Perguntas frequentes](#perguntas-frequentes)
- [Limitações](#limitações)
- [Método e origem](#método-e-origem)
- [Como contribuir](#como-contribuir)
- [Autor](#autor)
- [Licença](#licença)

## Contexto

Muita página moderna (SPA, site montado em Lovable, Framer ou React sem
server-side rendering) parece completa no navegador, mas entrega ao
crawler um HTML quase vazio, porque o conteúdo só aparece depois que o
JavaScript roda. Um crawler de IA que não executa JavaScript vê a casca
vazia, não o site que você vê. `page-to-ai-markdown` lê a página do mesmo
jeito: busca o HTML cru, tira só o ruído de interface, e mostra o que
sobra de verdade.

## Como funciona

A ferramenta busca a URL, remove `script`, `style`, `nav`, `header`,
`footer`, `form` e `aside`, além de blocos comuns de ruído (menu, aviso de
cookie, barra lateral, compartilhamento social, depoimento), e converte o
que sobra em markdown. De propósito, **não executa JavaScript**. É o
ponto da ferramenta, não uma falha dela.

## Requisitos

- Python 3
- Os pacotes listados em `requirements.txt`:
  - `requests>=2.31`
  - `beautifulsoup4>=4.12`
  - `markdownify>=0.13`
  - `lxml>=5.0`

## Instalação

```bash
git clone https://github.com/LucasFerrazSEO/page-to-ai-markdown.git
cd page-to-ai-markdown
pip install -r requirements.txt
```

## Uso

**1. Aponte para a URL que você quer testar.**

```bash
python page_to_ai_markdown.py https://exemplo.com/pagina/
```

Por padrão, a ferramenta salva um arquivo `.md` com o nome derivado da
URL, no diretório atual, com frontmatter (URL, título, meta description,
data da consulta, contagem de palavras).

**2. Ou peça para imprimir direto no terminal**, sem salvar arquivo:

```bash
python page_to_ai_markdown.py https://exemplo.com/pagina/ --stdout
```

**3. Leia a contagem de palavras restantes.** Se um artigo de 1.200
palavras vira 40 palavras depois da limpeza, é sinal forte de que o
conteúdo real depende de JavaScript e um crawler sem execução de JS não
está vendo quase nada:

```
pagina.md | Título da Página | 38 palavras restantes
```

**4. Escolha o nome e o local do arquivo de saída**, se quiser:

```bash
python page_to_ai_markdown.py https://exemplo.com/pagina/ --out diagnostico.md
```

**5. Use `--cache-bust`** em sites atrás de cache agressivo (LiteSpeed,
Cloudflare), que serviriam HTML antigo para a URL exata sem esse
parâmetro. Ele acrescenta `?v=<timestamp>` à URL antes de buscar:

```bash
python page_to_ai_markdown.py https://exemplo.com/pagina/ --cache-bust
```

## Perguntas frequentes

**page-to-ai-markdown é realmente grátis?**
Sim, código aberto sob licença MIT.

**Isso substitui o "Fetch como Google" do Search Console?**
Não faz o mesmo trabalho. O Fetch do Search Console usa o renderizador
completo do Google (com JavaScript). `page-to-ai-markdown` mostra
deliberadamente a versão SEM JavaScript, porque é essa a limitação que
muitos crawlers de IA ainda têm. Os dois diagnósticos se complementam.

**Funciona com qualquer site?**
Funciona com qualquer URL pública acessível por HTTP. Site atrás de login
ou bloqueio de bot não vai responder à requisição.

**A ferramenta modifica o site testado?**
Não. Só faz uma requisição GET, como qualquer visitante, e processa a
resposta localmente.

## Limitações

HTML puro, sem execução de JavaScript, de propósito. Remoção de ruído é
heurística baseada em classes e ids comuns de interface. Em página fora do
padrão pode sobrar lixo residual ou ser cortado conteúdo real por engano.
Trate o resultado como diagnóstico, não como cópia fiel do conteúdo
editorial.

## Método e origem

Generalização de um script de consulta usado internamente em
[lucasferrazseo.com](https://lucasferrazseo.com) para poupar tokens ao ler
páginas em sessões de IA. Aqui, sem nenhuma regra específica de site: os
padrões de ruído removidos são genéricos de interface web.

## Como contribuir

Relatos de erro e sugestões são bem-vindos pelas [Issues do GitHub](https://github.com/LucasFerrazSEO/page-to-ai-markdown/issues).

## Autor

[Lucas Ferraz](https://lucasferraz.com) é especialista em SEO, criação de sites e Generative Engine Optimization e fundador da [Lucas Ferraz SEO](https://lucasferrazseo.com).

## Licença

MIT. Veja o arquivo [LICENSE](LICENSE).
