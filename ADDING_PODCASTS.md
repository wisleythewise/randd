# Adding New Podcasts

Episodes live in `~/workspace/knowledge/docs/podcast/` on the laptop. Each episode has two parts:
- an `.m4a` audio file under `mp4/`
- a `.md` blueprint doc

## Copy files from laptop

```bash
# Copy a new audio file (replace <filename> with actual name)
scp laptop:~/workspace/knowledge/docs/podcast/mp4/<filename>.m4a ~/workspace/randd/mp4/

# Copy the blueprint doc
scp laptop:~/workspace/knowledge/docs/podcast/<date>.md ~/workspace/randd/
```

If you rsync the whole batch at once:

```bash
# Sync all new audio files
rsync -av --ignore-existing laptop:~/workspace/knowledge/docs/podcast/mp4/ ~/workspace/randd/mp4/

# Sync all new blueprint docs
rsync -av --ignore-existing --include="*.md" --exclude="*" laptop:~/workspace/knowledge/docs/podcast/ ~/workspace/randd/
```

## Add the episode to index.html

Open `index.html` and add a new `<tr>` inside `#pod-tbody`. Copy an existing row and update:

| Field | What to change |
|---|---|
| `data-search` | EP number + title words + topics (lowercase, no punctuation) |
| `ep-num` | `EP XX` |
| `ep-date-cell` | `Mon DD, YYYY` |
| `ep-title-cell` | Full episode title |
| `ep-chip` spans | Topic tags |
| `ep-listen-btn href` | `mp4/<filename>.m4a` |
| `ep-blueprint-btn href` | `<date>.md` (omit the `<a>` entirely if no blueprint) |

Insert the new row **at the top** of `<tbody>` so episodes stay newest-first.

Also update the episode count in the `<h2>` heading:
```html
<h2>Podcasts — XX episodes</h2>
```

## Run the build script (if password changed)

```bash
node build.js
```

## Push

```bash
git add mp4/<filename>.m4a <date>.md index.html
git commit -m "Add EP XX: <title>"
git push
```
