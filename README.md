# Yue Ding · Academic homepage

A bilingual, responsive academic homepage for Yue Ding (丁悦), Shanghai Mental Health Center. Built with static HTML, CSS and JavaScript; no build service, framework, external fonts, analytics or cookies are required.

- English: `index.html`
- 中文: `zh.html`
- Public research content: `profile.json`
- Page generator and student lists: `build.py`
- Styling: `styles.css`
- Publication search and filters: `app.js`

## Update content

Edit the public facts and publication records in `profile.json`, or the student lists in `build.py`, then regenerate both pages:

```sh
python3 build.py
```

Preview:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765/ in a browser. All publications remain readable when JavaScript is disabled. The print stylesheet includes the complete publication list.

## GitHub Pages

The intended repository is `FreyaTing/FreyaTing.github.io`. In **Settings → Pages**, publish from branch **main**, folder **/(root)**. The public URL is https://freyating.github.io/ once deployment completes. `.nojekyll` disables unnecessary Jekyll processing. Commit the generated HTML after editing the source data.

## Content sources

The supplied 2026 biography and August 2026 CV are the basis for the public profile. The portrait comes from the supplied 2025 biography. Student groupings and alumni destinations were supplied directly by the site owner on 24 November 2026. Original documents, personal telephone numbers and birth dates are not included.

Selected records were reconciled against primary sources on 24 November 2026:

- [Institutional profile](https://www.smhc.org.cn/njkyjy/info/4633/3362.htm)
- [Closed-loop tACS, Molecular Psychiatry](https://doi.org/10.1038/s41380-026-03846-3)
- [Schizophrenia subtyping, General Psychiatry](https://doi.org/10.1002/gps3.70047)
- [LARA-Gen v3, arXiv](https://arxiv.org/abs/2510.05875v3)

Google Scholar is linked, but direct access was unavailable during preparation. Citation metrics are therefore not displayed. The two 2026 bioRxiv/medRxiv records retain the preprint status documented in the CV. Education dates follow the supplied updated CV.
