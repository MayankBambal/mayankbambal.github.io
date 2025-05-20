---
layout: default
title: Home
permalink: /
---

# Welcome to My Portfolio

I’m **Mayank Bambal**, an MS candidate in Business Analytics & Information Management at Purdue University (graduating August 2025). With a B.Tech in Mechanical Engineering from IIT Indore (2019), I design and implement data-driven solutions that drive business impact across industries.

- 🔍 **Background & Achievements**: Learn about my journey, skills, and key accomplishments on the [About](/about/) page.
- 📂 **Projects & Code**: Explore detailed case studies, open-source projects, and portfolio highlights on the [Projects](/projects/) page.
- ✉️ **Connect with Me**: Reach out for collaborations, questions, or coffee chats on the [Contact](/contact/) page.

---

## Table of Contents

1. [Overview](#overview)
2. [Site Structure](#site-structure)
3. [Local Development](#local-development)
4. [Deployment](#deployment)
5. [Technologies](#technologies)
6. [Customization](#customization)
7. [License & Credits](#license--credits)
8. [Contact](#contact)

---

## Overview

This static portfolio is built with [Jekyll](https://jekyllrb.com/) and hosted on [GitHub Pages](https://pages.github.com/). It provides a clean, responsive showcase of my education, experience, and projects.

## Site Structure

```
/
├── _config.yml       # Jekyll configuration and site settings
├── _layouts
│   └── default.html  # Base HTML template for all pages
├── about.md          # About page content and bio
├── projects.md       # Projects portfolio
├── contact.md        # Contact information and links
├── README.md         # Homepage Markdown (this file)
├── styles.css        # Custom styling rules
└── assets/           # Images, scripts, and additional CSS
```

## Local Development

To run and preview the site locally:

```bash
# Install dependencies (first time only)
bundle install

# Start Jekyll server with live reload
bundle exec jekyll serve
```

Open your browser to `http://localhost:4000/`. The site will auto-rebuild when you edit content or styles.

## Deployment

Changes pushed to the `main` branch are automatically deployed via GitHub Pages:

1. Commit and push updates to `main`.
2. GitHub Pages builds using `_config.yml` and publishes to `https://mayankbambal.github.io/`.

## Technologies

- **Static Site Generator**: Jekyll (Ruby)
- **Hosting**: GitHub Pages (HTTPS enabled by default)
- **Languages & Formats**: HTML, Markdown, CSS
- **Plugins**:
  - jekyll-feed (RSS feed)
  - jekyll-seo-tag (SEO metadata)
  - jekyll-sitemap (XML sitemap)

## Customization

- **Themes**: Change the `theme` in `_config.yml` or override layouts under `_layouts/`.
- **Navigation**: Edit the `nav` array in `_config.yml` to reorganize or add new pages.
- **Styles**: Update `styles.css` (or add files under `assets/`) for custom visual tweaks.

## License & Credits

This portfolio template is open-source under the [MIT License](LICENSE).

- Built on the [Minimal Jekyll Theme](https://github.com/pages-themes/minimal).
- Powered by GitHub Pages and the Jekyll community.

## Contact

- 📧 Email: [mbambal@purdue.edu](mailto:mbambal@purdue.edu)
- 🔗 LinkedIn: [linkedin.com/in/mayankbambal](https://linkedin.com/in/mayankbambal/)
- 🐙 GitHub: [github.com/MayankBambal](https://github.com/MayankBambal/)

Feel free to connect for collaborations, feedback, or opportunities!
