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
- `styles.css` supplies the shared layout, system-based light/dark palettes, responsive behavior, and print styles.
- `Resume_Jackson-Pipe.pdf` remains the downloadable résumé. The separate Python résumé generator is not part of the website's runtime or publishing process.

Edit prose directly in `index.html` and the case-study `body.html` fragments; edit titles, summaries, technologies, years, and article metadata in `projects.json`, then run the generator. Page styles are shared, and the repeated navigation markup is rendered rather than copied by hand, so a title or slug only has to change in one place and the published files stay plain static HTML.

The diagrams are semantic HTML with CSS. Their labels and captions remain readable without styling. Investing Stats and Brawl Stats include local application screenshots on the homepage and their case studies, with dated captions and full-size links on the detail pages. Homepage previews crop the original images through CSS; the full-size images remain unchanged. The StarCraft illustration is a conceptual agent loop, not a recorded simulation.

The design uses warm ivory, charcoal, and rust, with a matching system dark theme and a 1,200px container. The homepage leads with Jackson's name, a factual introduction, and professional background. Its project directory is one reverse-chronological list of compact rows, each carrying a description, its technologies, and the year or year range it covers. Below 540px a row stacks, keeping the technologies and year on a shared second line. Shared case-study layouts have a desktop contents rail and wrapping mobile navigation. A dark contact panel closes the homepage.

Manrope (variable, weights 400–800) and Source Serif 4 (regular italic) are self-hosted Latin WOFF2 fonts in `assets/fonts/`, alongside their SIL Open Font License files. The main font is preloaded, both use `font-display: swap`, and system fallbacks keep text available when font loading fails. The homepage includes JSON-LD person metadata, but no executable JavaScript. All page resources are local; loading a page makes no third-party requests.

Keep the introduction factual and personal: roles, background, and specific activities. Avoid promotional slogans, generic claims, and availability badges. Project-directory entries need a preview, a short description, technologies, and a detail-page link; put ownership, implementation decisions, and evaluation evidence in the case studies. Use the shared color tokens, spacing rhythm, and restrained hover/focus treatments. Keep navigation, theme colors, metadata, and project links consistent across all pages.

To add a project, write its case study as `work/<slug>/body.html` — the hero figure, contents rail, and prose sections, using an existing fragment as the template — then add an entry to `projects.json` in date order and run `python build_site.py`. The generator produces the page chrome, the homepage row, the heading IDs and their `aria-labelledby` pairs, and the adjacent-project links. Retain dated screenshot captions in the fragment. Add only projects with reviewed source material, not placeholder cards.

## Editorial notes

Case studies describe implementation decisions, not inferred popularity or performance. Their initial source material was the corresponding projects' implementation, tests, and documentation:

- **Investing Stats:** ingestion and backfill orchestration, SQLite persistence, parsing/query tests, and deployment documentation.
- **Brawl Stats:** aggregation cache, composition model and recommendation path, synthetic model tests, and data-quality tests.
- **StarCraft:** SpecTactics architecture and distance-query correction, μSC2 action representation, and Augur's recorded September 8, 2026 experiment. Offline results are distinguished from full-game outcomes.

Before adding a metric, retain its measurement date, dataset or evaluation scope, and supporting result. Goals in project documents are not completed outcomes. Do not add inferred dates, audience sizes, ladder ranks, or performance figures.

The Investing Stats demo returned a public HTTP 200 during the September 9, 2026 review. Other project source/demo links were not confirmed publicly accessible and are omitted. Recheck external links before publication. Avoid copying private source, credentials, user records, or development-browser artifacts into this repository.

## Review before publishing

Check the homepage and each case study at mobile, tablet, and desktop widths, in both system color schemes. Test keyboard navigation, 200% zoom, printing, internal anchors, the PDF, and email links. The whole site should remain usable with JavaScript disabled and third-party requests blocked.

Run `python build_site.py --check` to confirm the committed HTML matches `projects.json` and the case-study fragments. Keep `CNAME` set to `jacksonpipe.dev`. Publish through the repository's existing GitHub Pages configuration. Domain certificates and HTTPS enforcement are managed in GitHub Pages settings, separately from the site files.

Local browser-review artifacts belong in the ignored `.preview/` directory.

## Contact

[jackbpipe@gmail.com](mailto:jackbpipe@gmail.com) · [GitHub](https://github.com/Waxter88) · [LinkedIn](https://www.linkedin.com/in/jackson-pipe/)
