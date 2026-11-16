# Personal website of Mads Henrik Højgaard

Live at https://madshenrikhoejgaard.github.io, from the repository `madshenrikhoejgaard.github.io`.

This folder is the source of the website. Quarto turns these files into web pages, and GitHub builds and publishes the site automatically every time you save (commit) a change. You never need to build anything yourself.

## What the files do

| File or folder | What it is | Will you edit it? |
|---|---|---|
| `_quarto.yml` | Site settings: name, address, menu, footer | Rarely |
| `_variables.yml` | Your email and LinkedIn address | Once |
| `index.qmd` | Home page, with the blue band and the figures | Sometimes |
| `projects.qmd` | The Projects page: series and the map (builds itself) | Rarely |
| `projects/` | One page per series, and the Double Economy chart data | Sometimes |
| `_data/series.yml` | The series: names, pages and one-line summaries | When you start a series |
| `_data/places.yml` | The places on the map | When you write about a new place |
| `_data/greece-map.json` | The outline of Greece for the map | No |
| `_scripts/` | Small Python helper that counts, groups and maps the writing | No |
| `images/` | The chalk drawing in the home page band | No |
| `about.qmd` | About page | Sometimes |
| `writing.qmd` | The Writing page (builds itself from your posts) | No |
| `external.yml` | List of pieces published on other websites | Often |
| `posts/` | One folder per post written for this site | Often |
| `references.bib` | Your reference library for citations | Often |
| `theme-light.scss`, `theme-dark.scss` | Colours for light and dark mode | Rarely |
| `styles.css` | Layout and typography | Rarely |
| `house.mplstyle` | Chart style | Rarely |
| `fonts/` | The two typefaces and their licences | No |
| `_listing/`, `_includes/` | Small technical parts of the layout | No |
| `requirements.txt` | Python packages GitHub installs to draw charts | No |
| `.github/workflows/publish.yml` | Instructions GitHub follows to build and publish | No |

Files ending in `.qmd` are ordinary text written in Markdown: `*italic*`, `**bold**`, `## Heading`, `[link text](https://address)`.

## Add a piece published elsewhere

1. On GitHub, open `external.yml` and click the pencil icon (Edit this file).
2. Copy one whole entry, from its dash down to the blank line after it, and paste it at the top of the list.
3. Change the title, outlet, link (`path`), date (year-month-day), description and topics. Keep the spaces at the start of each line exactly as they are.
   - If the piece belongs to a series, keep or change its `series:` line, for example `series: [double-economy]`. If not, delete the line.
   - If the piece is set in a place on the map, keep or change its `place:` line, for example `place: symi`. If not, delete the line.
4. Click **Commit changes**. The piece appears on the site in about two minutes.

Write the description in your own words. Do not paste text from the original article.

## Write a new post

1. On GitHub, click **Add file**, then **Create new file**.
2. In the name box, type the folder and file name, for example `posts/2026-12-01-housing-strategy/index.qmd`. Typing the slashes creates the folders.
3. Paste this header at the top and write the post below it:

```
---
title: "Your title"
description: "One sentence on what the post argues."
date: 2026-12-01
categories: [Housing]
draft: true
---

Your text starts here.
```

4. Click **Commit changes**. While `draft: true` is in the header, the post stays off the live site. Delete that line and commit again to publish.

Note that the repository is public. Anything stored in it, drafts included, can be read by anyone who opens the repository on GitHub, even when it is not on the site. Keep sensitive or embargoed drafts elsewhere until they are ready.

The sample post in `posts/2026-11-09-sample-post/` shows citations, a margin note and a chart. It is marked as a draft and is never published; keep it as a reference.

### Images

Open the post's folder on GitHub, click **Add file**, then **Upload files**, and add the image. In the post, write `![Caption, with the source of the image](photo.jpg)`.

### Citations

Paste a BibTeX entry into `references.bib` (Zotero can export BibTeX, and most journal pages offer it under "Cite"). Then cite it in a post with its key in square brackets, such as `[@ostrom1990governing]`. The reference list is built automatically.

### Charts from data

Put a data file such as `data.csv` in the post's folder and copy the chart code from the sample post. The code is hidden from readers. Always name the dataset and release in the caption.

## Series and the Projects page

The Projects page groups the writing into series and builds itself. A piece joins a series through the `series:` line of its entry in `external.yml` (or in the header of a post). The series ids are `double-economy`, `cafe-neon`, `accountability`, `memory`, `islands` and `portraits`. A piece can belong to more than one: `series: [memory, islands]`.

To start a new series:

1. Open `_data/series.yml`, copy one entry and give it a new `id` (short, no spaces), title, page and summary.
2. Open one of the small series pages in `projects/`, such as `projects/portraits.qmd`, copy its contents, and create a new file in `projects/` named after the id, for example `projects/elections.qmd`. Change the title, the text and the id in the line `series: "portraits"`.
3. Add `series: [elections]` to the pieces that belong to it.

## The map of the writing

The map at the end of the Projects page shows the places listed in `_data/places.yml`, with the pieces whose entry has a matching `place:` line. To add a place, copy one entry in `_data/places.yml`, give it an id, a name and its latitude and longitude (right-click the spot in Google Maps or OpenStreetMap to see them), then use the id in `place:` lines. If two names overlap on the map, change `label:` to `left`, `right`, `above` or `below`.

The outline of Greece comes from Natural Earth (public domain) and is stored in the site, so the map loads nothing from other websites.

## The Double Economy page

`projects/double-economy.qmd` has the framework text, the diagram of the four channels and the chart. The chart reads `projects/data/housing-overburden.csv`: one row per year and area, taken from Eurostat's dataset ilc_lvho07a (housing cost overburden rate). In the `flag` column, `e` means Eurostat marks the value as an estimate. When Eurostat publishes a new year, add two rows (Greece and EU) and check the year range and the date in the chart caption in `double-economy.qmd`.

## Figures on the home page

The number of articles under the blue band is counted automatically every time the site is built. The other three figures are written in `index.qmd`, in the block that starts with `print(sitedata.tally_html(`. Change the number or the words between the quotation marks.

## Check that a change worked

Open the **Actions** tab of the repository. Each change starts a run called "Publish site".

A green tick means the site is published. A red cross means something stopped the build, usually a typing mistake in a header or in `external.yml`, and the live site keeps its previous version. Open the failed run, copy the red error lines, and ask Claude to read them.

## The publishing instructions file

Folders whose names start with a dot are hidden on most computers, so `.github` may not come along when you drag the project files into GitHub. If the repository has no `.github` folder after uploading, create the file by hand: click **Add file**, then **Create new file**, name it `.github/workflows/publish.yml`, and paste in its contents.

## Later, if you want: working on your own computer

Everything can be done on GitHub's website. If you later want to preview drafts before they go online, install Quarto from quarto.org and an editor such as Positron or VS Code, open this folder, and run `quarto preview`. GitHub Desktop keeps your computer and GitHub in step without the command line.

## Licences

The typefaces are GFS Didot (Greek Font Society) and Literata (The Literata Project Authors), both under the SIL Open Font License. The licence texts are in the `fonts/` folder.
