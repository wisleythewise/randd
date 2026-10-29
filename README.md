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
