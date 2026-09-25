**English** · [Português (Brasil)](README.pt-BR.md)

# page-to-ai-markdown

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3](https://img.shields.io/badge/python-3-blue.svg)

`page-to-ai-markdown` is a free, open source command-line tool that fetches
a URL, strips the menu, footer, forms and other interface elements, and
shows what is left as clean markdown. It approximates what an AI search
crawler (GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot and similar) has
to read when the initial HTML is already rendered on the server, with no
JavaScript execution. The page is fetched with a single GET request and
processed locally.

## Contents

- [Background](#background)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
- [Limitations](#limitations)
- [Methodology](#methodology)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## Background

Many modern pages (SPAs, sites built with Lovable, Framer or React without
server-side rendering) look complete in the browser but deliver an almost
empty HTML to the crawler, because the content only appears after
JavaScript runs. An AI crawler that does not execute JavaScript sees the
empty shell, not the site you see. `page-to-ai-markdown` reads the page
the same way: it fetches the raw HTML, removes only the interface noise,
and shows what is really left.

## How it works

The tool fetches the URL, removes `script`, `style`, `nav`, `header`,
`footer`, `form` and `aside`, plus common noise blocks (menu, cookie
notice, sidebar, social sharing, testimonials), and converts the rest to
markdown. It **does not execute JavaScript** on purpose. That is the point
of the tool, not a flaw.

## Requirements

- Python 3
- The packages listed in `requirements.txt`:
  - `requests>=2.31`
  - `beautifulsoup4>=4.12`
  - `markdownify>=0.13`
  - `lxml>=5.0`

## Installation

```bash
git clone https://github.com/LucasFerrazSEO/page-to-ai-markdown.git
cd page-to-ai-markdown
pip install -r requirements.txt
```

## Usage

The tool prints its messages and writes the frontmatter keys in Brazilian
Portuguese.

**1. Point it at the URL you want to test.**

```bash
python page_to_ai_markdown.py https://exemplo.com/pagina/
```

By default, the tool saves a `.md` file named after the URL in the current
directory, with frontmatter (URL, title, meta description, fetch date,
word count).

**2. Or print straight to the terminal**, without saving a file:

```bash
python page_to_ai_markdown.py https://exemplo.com/pagina/ --stdout
```

**3. Read the remaining word count.** If a 1,200-word article turns into
40 words after cleanup, that is a strong sign the real content depends on
JavaScript and a crawler that does not run JS sees almost nothing:

```
pagina.md | Título da Página | 38 palavras restantes
```

**4. Choose the output file name and location**, if you want:

```bash
python page_to_ai_markdown.py https://exemplo.com/pagina/ --out diagnostico.md
```

**5. Use `--cache-bust`** on sites behind aggressive caching (LiteSpeed,
Cloudflare) that would serve old HTML for the exact URL without this
parameter. It appends `?v=<timestamp>` to the URL before fetching:

```bash
python page_to_ai_markdown.py https://exemplo.com/pagina/ --cache-bust
```

## FAQ

**Is page-to-ai-markdown really free?**
Yes. It is open source under the MIT license.

**Does this replace "Fetch as Google" in Search Console?**
It does not do the same job. The Search Console fetch uses Google's full
renderer (with JavaScript). `page-to-ai-markdown` deliberately shows the
version WITHOUT JavaScript, because that is the limitation many AI
crawlers still have. The two diagnostics complement each other.

**Does it work with any site?**
It works with any public URL reachable over HTTP. A site behind a login or
bot blocking will not respond to the request.

**Does the tool change the tested site?**
No. It only makes one GET request, like any visitor, and processes the
response locally.

## Limitations

Plain HTML, no JavaScript execution, on purpose. Noise removal is a
heuristic based on common interface classes and ids. On a page that does
not follow common patterns, some residual clutter may remain or real
content may be cut by mistake. Treat the result as a diagnostic, not as a
faithful copy of the editorial content.

## Methodology

A generalization of a lookup script used internally at
[lucasferrazseo.com](https://lucasferrazseo.com) to save tokens when
reading pages in AI sessions. Here it has no site-specific rules: the
noise patterns it removes are generic web interface patterns.

## Contributing

Bug reports and suggestions are welcome through [GitHub Issues](https://github.com/LucasFerrazSEO/page-to-ai-markdown/issues).

## Author

[Lucas Ferraz](https://lucasferraz.com) is an SEO, website development and Generative Engine Optimization specialist and the founder of [Lucas Ferraz SEO](https://lucasferrazseo.com).

## License

MIT. See [LICENSE](LICENSE).
