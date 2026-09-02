# heydarsoudani.github.io

Personal academic homepage. Static HTML, no dependencies, served by GitHub Pages.

## Layout

| Path             | Role                                                        |
| ---------------- | ----------------------------------------------------------- |
| `sections/`      | Page content — one file per section. **Edit these.**         |
| `_template.html` | Page shell: `<head>`, and the order sections appear in.      |
| `build.py`       | Inlines `sections/` into `_template.html` → `index.html`.    |
| `index.html`     | **Generated. Do not edit** — your changes will be overwritten. |
| `styles.css`     | All styling.                                                 |
| `main.js`        | Theme toggle, mobile nav, scroll fade-in.                    |

## Editing

```sh
# 1. edit a file in sections/ (or _template.html)
# 2. rebuild
./build.py
# 3. commit the section file AND the regenerated index.html
```

`index.html` is committed because GitHub Pages serves it directly — there is no
build step on their side.

To confirm you didn't forget step 2:

```sh
./build.py --check   # exits 1 if index.html is out of date
```

### Adding a section

1. Create `sections/<name>.html` containing a single `<section id="<name>">`.
2. Add `<div data-include="sections/<name>.html"></div>` to `_template.html`
   where you want it to appear.
3. Add a nav link in `sections/nav.html`.
4. Run `./build.py`.

`sections/service.html` and `sections/press.html` are scaffolded but commented
out — uncomment the block and its nav entry once there are real entries.

## Preview

Because `index.html` is fully assembled, opening it directly in a browser works.
To serve it as GitHub Pages does:

```sh
python3 -m http.server 8000   # → http://localhost:8000
```

## Credit

Design adapted with permission from [Zahra Moti](https://zahramoti.com)'s
personal site.
