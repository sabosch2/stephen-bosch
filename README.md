# stephen-bosch.com

My personal portfolio site — a standalone static site, separate from the
[In Transit](https://2intransit.com) travel blog.

## Files

- `index.html` — the whole site (nav, hero, about, skills, projects, contact).
- `style.css` — all the styling. Change the colours/fonts at the top under
  `:root` to re-theme the site.

Both files sit at the repo root so the site can be deployed as-is.

## Editing

Everything is plain HTML/CSS with comments explaining each part. To add a
project, copy one of the `<article class="card">` blocks in the Projects
section and edit the text. Placeholder text is written in `[brackets]` or as
comments — search for those to find what to fill in.

## Hosting

Deployed on Netlify from this GitHub repo. Every push to `main` publishes
automatically. Custom domain: **stephen-bosch.com**.
