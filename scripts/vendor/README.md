# Bundled Markdown renderer

Mistune **3.2.0** is bundled here so the Python static build remains self-contained on the current host. Source: https://github.com/lepture/mistune . License: BSD-3-Clause, retained under `mistune-3.2.0.dist-info/licenses/LICENSE`.

Installed from the pinned PyPI wheel with `python3 -m pip install --target scripts/vendor --no-compile mistune==3.2.0`. Review upstream updates deliberately and rerun the CMS/content checks when updating. Raw HTML is escaped and unsafe Markdown link schemes are blocked by the renderer.
