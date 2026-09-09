# Jackson Pipe

Personal portfolio at [jacksonpipe.dev](https://jacksonpipe.dev/). Static HTML and CSS, published with GitHub Pages.

## Preview

From this directory, run:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000/>. There is no install or build step.

## Content

- `index.html` contains the personal introduction, professional background, categorized project directory, and contact information.
- `work/` contains the three standalone case studies. Each directory has an `index.html` so its URL works without a file extension.
- `styles.css` supplies the shared layout, system-based light/dark palettes, responsive behavior, and print styles.
- `Resume_Jackson-Pipe.pdf` remains the downloadable résumé. The separate Python résumé generator is not part of the website's runtime or publishing process.

Edit the HTML directly. When changing a project title or URL, update its homepage entry, case-study metadata, and the adjacent-project links. Page styles are shared; navigation markup is repeated deliberately to keep publishing independent of a build tool.

The diagrams are semantic HTML with CSS. Their labels and captions remain readable without styling. Investing Stats and Brawl Stats include local application screenshots on the homepage and their case studies, with dated captions and full-size links on the detail pages. Homepage previews crop the original images through CSS; the full-size images remain unchanged. The StarCraft illustration is a conceptual agent loop, not a recorded simulation.

The design uses warm ivory, charcoal, and rust, with a matching system dark theme and a 1,200px container. The homepage leads with Jackson's name, a factual introduction, and professional background. Its project directory groups compact entries under Web applications and Game AI, with native category jump links. Application cards use two columns on desktop and one on phones; the agent collection spans the desktop grid. Shared case-study layouts have a desktop contents rail and wrapping mobile navigation. A dark contact panel closes the homepage.

Manrope (variable, weights 400–800) and Source Serif 4 (regular italic) are self-hosted Latin WOFF2 fonts in `assets/fonts/`, alongside their SIL Open Font License files. The main font is preloaded, both use `font-display: swap`, and system fallbacks keep text available when font loading fails. The homepage includes JSON-LD person metadata, but no executable JavaScript. All page resources are local; loading a page makes no third-party requests.

Keep the introduction factual and personal: roles, background, and specific activities. Avoid promotional slogans, generic claims, and availability badges. Project-directory entries need a preview, a short description, technologies, and a detail-page link; put ownership, implementation decisions, and evaluation evidence in the case studies. Use the shared color tokens, spacing rhythm, and restrained hover/focus treatments. Keep navigation, theme colors, metadata, and project links consistent across all pages.

To add a project, create its case study under `work/<slug>/index.html` using an existing article as the template, then add a `.project` article to the appropriate `.project-grid` on the homepage. Give it a unique heading ID and matching `aria-labelledby`, retain dated screenshot captions, and update adjacent-project links. A new category needs a labeled `.project-category` section and a link in `.category-nav`; category links jump to sections and do not filter or hide content. Add only projects with reviewed source material, not placeholder cards.

## Editorial notes

Case studies describe implementation decisions, not inferred popularity or performance. Their initial source material was the corresponding projects' implementation, tests, and documentation:

- **Investing Stats:** ingestion and backfill orchestration, SQLite persistence, parsing/query tests, and deployment documentation.
- **Brawl Stats:** aggregation cache, composition model and recommendation path, synthetic model tests, and data-quality tests.
- **StarCraft:** SpecTactics architecture and distance-query correction, μSC2 action representation, and Augur's recorded September 8, 2026 experiment. Offline results are distinguished from full-game outcomes.

Before adding a metric, retain its measurement date, dataset or evaluation scope, and supporting result. Goals in project documents are not completed outcomes. Do not add inferred dates, audience sizes, ladder ranks, or performance figures.

The Investing Stats demo returned a public HTTP 200 during the September 9, 2026 review. Other project source/demo links were not confirmed publicly accessible and are omitted. Recheck external links before publication. Avoid copying private source, credentials, user records, or development-browser artifacts into this repository.

## Review before publishing

Check the homepage and each case study at mobile, tablet, and desktop widths, in both system color schemes. Test keyboard navigation, 200% zoom, printing, internal anchors, the PDF, and email links. The whole site should remain usable with JavaScript disabled and third-party requests blocked.

Keep `CNAME` set to `jacksonpipe.dev`. Publish through the repository's existing GitHub Pages configuration. Domain certificates and HTTPS enforcement are managed in GitHub Pages settings, separately from the site files.

Local browser-review artifacts belong in the ignored `.preview/` directory.

## Contact

[jackbpipe@gmail.com](mailto:jackbpipe@gmail.com) · [GitHub](https://github.com/Waxter88) · [LinkedIn](https://www.linkedin.com/in/jackson-pipe/)
