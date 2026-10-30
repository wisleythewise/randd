# randd

Servo7's static research library: engineering references, interactive explainers,
podcasts, RFCs, and reports. Serve this directory with `python -m http.server 8000`
and open `http://localhost:8000` to preview it locally.

The library and engineering mechanics reader share `randd.css`, using the colors,
typography, borders, and spacing of the Jarvis portal. Existing interactive
explainers keep their individual layouts.

`Engineering_Mechanics_Visual_Cheat_Sheet.pdf` is the original 21-page downloaded
reference. It is linked from the library and has a reader at
`engineering-mechanics.html`, with section links and open/download fallbacks.

To display the library inside Jarvis, point its embedded app at the hosted
`index.html`. `randd-shell.js` automatically hides the standalone brand bar and
footer inside an iframe while keeping the page title and section navigation.
Use `?embed=1` to preview that presentation without a frame. Section deep links
such as `index.html?embed=1#reports` work too. Embedding does not bypass the
existing library password check or introduce shared authentication.

The downloaded 247TailorSteel CAD/design guide and Harmonic Drive SHA58A swivel
evaluation also have PDF readers at `247tailorsteel-design-guide.html` and
`harmonic-drive-sha58a.html`. The original PDFs are preserved without editing.

The **Cheatsheets** tab groups the 247TailorSteel guide and Engineering Mechanics
reference; both also remain searchable under Pages. Document lists use one column
and are ordered newest first by their library-added date (not their source's
publication date). Each card stores that date in `data-added` and displays it in a
`time` element. When adding a document, insert its card in descending date order.

Cards use small, static previews in `assets/previews/`: the first page for PDFs,
and a browser capture for HTML documents. Regenerate them with:

```sh
uv run --with playwright python scripts/generate-library-previews.py
```

This requires Playwright Chromium (`uv run --with playwright playwright install
chromium`) and `pdftoppm`. Add new PDF readers to the script's `PDFS` mapping.
Original documents are not modified; previews load lazily in the library.
