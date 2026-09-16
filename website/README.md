# Website preview

Run from the parent `astra-build` directory:

```bash
python3 -m http.server 8765
```

Open `http://127.0.0.1:8765/website/`.

The site has no framework/build dependency. `app.js` loads
`../release/metrics.json` when served over HTTP and falls back to the static metric
values embedded in the HTML if fetch is unavailable.

Large videos and D41 review renders are referenced by relative path so this draft
does not duplicate or alter the historical presentation/experiment media.

