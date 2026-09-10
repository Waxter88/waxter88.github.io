# Jackson Pipe

Personal portfolio at [jacksonpipe.dev](https://jacksonpipe.dev/). Static HTML and CSS, published with GitHub Pages.

## Preview

From this directory, run:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000/>. Serving the files needs no install step, and the generated pages are committed, so a fresh checkout previews without running anything. `python build_site.py` regenerates them after a change to `projects.json` or a case-study fragment; it uses the standard library only.

## Content

- `index.html` contains the personal introduction, professional background, project directory, and contact information. Everything between the `build:projects` markers is generated; the rest is hand-written.
- `work/` contains the three standalone case studies. Each directory has an `index.html` so its URL works without a file extension, generated around the hand-written prose in its `body.html`.
- `projects.json` holds the fields the generated chrome needs — titles, summaries, technologies, years, article metadata, and search descriptions — ordered newest first. That order sets both the homepage directory and the adjacent-project links.
- `build_site.py` renders both from that data. `python build_site.py --check` reports whether the committed output is current and writes nothing.
- `sitemap.xml` and `robots.txt` are generated from the same project order and committed with the pages. The sitemap carries no `lastmod`: an invented date would be worse than none.
- `assets/og/card.html` is the source for `assets/og-card.png`, the 1200×630 social card every page points at with `og:image`. It is rendered once and committed, so a published page still loads nothing but its own files. Re-render it only when the card's own text changes: serve the site, open the card at a 1200×630 viewport, and capture that viewport as PNG.
- `styles.css` supplies the shared layout, system-based light/dark palettes, responsive behavior, and print styles.
- `Resume_Jackson-Pipe.pdf` remains the downloadable résumé. The separate Python résumé generator is not part of the website's runtime or publishing process.

Edit prose directly in `index.html` and the case-study `body.html` fragments; edit titles, summaries, technologies, years, and article metadata in `projects.json`, then run the generator. Page styles are shared, and the repeated navigation markup is rendered rather than copied by hand, so a title or slug only has to change in one place and the published files stay plain static HTML.

The diagrams are semantic HTML with CSS. Their labels and captions remain readable without styling, and the print stylesheet redraws the dark agent diagram on white so it does not print as a solid block. Investing Stats and Brawl Stats include local application screenshots on their case studies, with dated captions and full-size links. The homepage carries no images. The StarCraft illustration is a conceptual agent loop, not a recorded simulation.

The design uses warm ivory, charcoal, and rust, with a matching system dark theme, a 1,080px homepage container and a 1,200px container elsewhere. Spacing and type are drawn from the `--s-*` and `--t-*` scales declared at the top of `styles.css`; reach for a scale step rather than a new literal value, and keep the responsive blocks' optically tuned offsets as they are. The type ladder runs 72 / 31 / 20 / 17px so the project directory outranks the background list rather than matching it. The homepage leads with Jackson's name, a factual introduction, and a professional background split into Work and Education & certification, each list carrying its own heading and date gutter. Its project directory is one reverse-chronological list of compact rows, each carrying a description, its technologies, and the year or year range it covers, with a `--wash` ground on hover. Below 540px a row stacks, keeping the technologies and year on a shared second line. Shared case-study layouts have a desktop contents rail and wrapping mobile navigation, and set prose to roughly 69 characters a line.

Manrope (variable, weights 400–800) and Source Serif 4 (regular italic) are self-hosted Latin WOFF2 fonts in `assets/fonts/`, alongside their SIL Open Font License files. The main font is preloaded, both use `font-display: swap`, and system fallbacks keep text available when font loading fails. The homepage includes JSON-LD person metadata, but no executable JavaScript. All page resources are local; loading a page makes no third-party requests.

Keep the introduction factual and personal: roles, background, and specific activities. Avoid promotional slogans, generic claims, and availability badges. Project-directory entries need a short description, technologies, and a detail-page link; put ownership, implementation decisions, and evaluation evidence in the case studies. Use the shared color tokens, spacing rhythm, and restrained hover/focus treatments. Keep navigation, theme colors, metadata, and project links consistent across all pages.

To add a project, write its case study as `work/<slug>/body.html` — the hero figure, contents rail, and prose sections, using an existing fragment as the template — then add an entry to `projects.json` in date order and run `python build_site.py`. The generator produces the page chrome, the homepage row, the heading IDs and their `aria-labelledby` pairs, and the adjacent-project links. Retain dated screenshot captions in the fragment. Add only projects with reviewed source material, not placeholder cards.

## Editorial notes

Case studies describe implementation decisions, not inferred popularity or performance. Their initial source material was the corresponding projects' implementation, tests, and documentation:

- **Investing Stats:** ingestion and backfill orchestration, SQLite persistence, parsing/query tests, and deployment documentation.
- **Brawl Stats:** aggregation cache, composition model and recommendation path, synthetic model tests, and data-quality tests.
- **StarCraft:** SpecTactics architecture and distance-query correction, μSC2 action representation, and Augur's recorded September 8, 2026 experiment. Offline results are distinguished from full-game outcomes.

Before adding a metric, retain its measurement date, dataset or evaluation scope, and supporting result. Goals in project documents are not completed outcomes. Do not add inferred dates, audience sizes, ladder ranks, or performance figures.

The Investing Stats and Brawl Stats demos both returned a public HTTP 200 during the September 9, 2026 review. Both are Fly.dev deployments that suspend when idle, so a first request can hang for a minute or more while the machine wakes; check headers with a generous timeout rather than concluding the app is down. The StarCraft projects have no confirmed public link and none is listed. Recheck external links before publication. Avoid copying private source, credentials, user records, or development-browser artifacts into this repository.

## Review before publishing

Check the homepage and each case study at mobile, tablet, and desktop widths, in both system color schemes. Test keyboard navigation, 200% zoom, printing, internal anchors, the PDF, and email links. The whole site should remain usable with JavaScript disabled and third-party requests blocked.

Confirm `og:image` resolves once the change is live, and that `sitemap.xml` parses and lists every page.

Run `python build_site.py --check` to confirm the committed output matches `projects.json` and the case-study fragments. Keep `CNAME` set to `jacksonpipe.dev`. Publish through the repository's existing GitHub Pages configuration. Domain certificates and HTTPS enforcement are managed in GitHub Pages settings, separately from the site files.

Local browser-review artifacts belong in the ignored `.preview/` directory.

## Resume

The previous resume PDF and generator are preserved locally in `_archive/resume/2026-09-09-before-redesign/`, which is ignored by Git. They also remain recoverable from commit `17d7079af8e2c707b2a40c7729bfdee1740f46f7`. The portfolio's existing links use the current `Resume_Jackson-Pipe.pdf` at the repository root.

`build_resume.py` contains the resume content and generates `Resume_Jackson-Pipe.pdf`. Edit the summary, skills, training and experience entries in the script, then rebuild:

```sh
python -m pip install reportlab==5.0.1
python build_resume.py
```

The resume follows the portfolio's Manrope typography and rust-and-charcoal palette. It uses short paragraphs and a narrow section-label rail. Relevant experience leads with the Niagara academic client work; qualifications share the same visual treatment. Contact details and web links sit in two aligned rows, with the portfolio link accented and underlined. Personal project case studies stay on the portfolio. The one-page PDF has embedded fonts and clickable contact, portfolio, and credential links. The generator checks the page count before replacing the existing PDF. Review the rendered page and extracted text after changing the content. Resume edits do not require running the site generator.

`assets/fonts/manrope-regular.ttf` and `manrope-semibold.ttf` are static 400/600 instances of the existing `manrope.woff2`, generated with FontTools for PDF embedding. They retain the accompanying `Manrope-OFL.txt` licence. Rebuilding the resume only needs ReportLab; FontTools is needed only if regenerating those font instances.

The cybersecurity training description combines Jackson's confirmed tabletop exercise and attack-response simulations with [Mohawk's 2025 program of studies](https://myssb.mohawkcollege.ca/mcprod/psecrsdes.P_POSGet?pos_prg=557&prg_ver=25-A) and [official program overview](https://www.mohawkcollege.ca/programs/graduate-studies/cyber-security-analytics-557), reviewed September 9, 2026. Program descriptions support training topics; they do not establish specific tools used, employment, or project outcomes. Personal dates follow the portfolio's background section and the corrected Niagara project dates.

The Azure and Niagara diploma blurbs describe broad credential topics, checked against [Microsoft's Azure Fundamentals overview](https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/) and [Niagara's Computer Programming overview](https://www.niagaracollege.ca/media/program/programming/). They do not imply professional Azure administration experience or completion of courses introduced after graduation.

## Contact

[jackbpipe@gmail.com](mailto:jackbpipe@gmail.com) · [GitHub](https://github.com/Waxter88) · [LinkedIn](https://www.linkedin.com/in/jackson-pipe/)
