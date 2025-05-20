---
layout: default
title: Welcome to Slate
description: A Jekyll theme for GitHub Pages
---

# Welcome to Slate

Slate is a Jekyll theme for GitHub Pages. You can preview the theme to see what it looks like, or even use it today.

## Usage

To use the Slate theme:

1. Add the following to your site's `_config.yml`:
```yaml
remote_theme: pages-themes/slate@v0.2.0
plugins:
  - jekyll-remote-theme
```

2. Optionally, if you'd like to preview your site on your computer, add the following to your site's `Gemfile`:
```ruby
gem "github-pages", group: :jekyll_plugins
```

## Customizing

### Configuration variables

Slate will respect the following variables, if set in your site's `_config.yml`:

```yaml
title: [The title of your site]
description: [A short description of your site's purpose]
```

Additionally, you may choose to set the following optional variables:

```yaml
show_downloads: ["true" or "false" (unquoted) to indicate whether to provide a download URL]
google_analytics: [Your Google Analytics tracking ID]
```

### Stylesheet

If you'd like to add your own custom styles:

1. Create a file called `/assets/css/style.scss` in your site
2. Add the following content to the top of the file, exactly as shown:
```scss
@import "{{ site.theme }}";
```
3. Add any custom CSS (or Sass, including imports) you'd like immediately after the `@import` line

### Layouts

If you'd like to change the theme's HTML layout:

1. For some changes such as a custom favicon, you can add custom files in your local `_includes` folder. The files provided with the theme provide a starting point and are included by the original layout template.
2. For more extensive changes, copy the original template from the theme's repository
3. Create a file called `/_layouts/default.html` in your site
4. Paste the default layout content copied in the first step
5. Customize the layout as you'd like

## Contributing

Interested in contributing to Slate? We'd love your help. Slate is an open source project, built one contribution at a time by users like you. See the [CONTRIBUTING](CONTRIBUTING.md) file for instructions on how to contribute.

## Previewing the theme locally

If you'd like to preview the theme locally (for example, in the process of proposing a change):

1. Clone down the theme's repository (`git clone https://github.com/pages-themes/slate`)
2. `cd` into the theme's directory
3. Run `script/bootstrap` to install the necessary dependencies
4. Run `bundle exec jekyll serve` to start the preview server
5. Visit `localhost:4000` in your browser to preview the theme

## Running tests

The theme contains a minimal test suite, to ensure a site with the theme would build successfully. To run the tests, simply run `script/cibuild`. You'll need to run `script/bootstrap` once before the test script will work. 