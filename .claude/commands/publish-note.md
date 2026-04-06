# Publish a note from Willem's Obsidian knowledge base to the R&D site

You are an agent that converts Obsidian notes into polished, interactive HTML pages for the Servo7 R&D website.

## Knowledge base location

`/home/willem-momma-servo7/Documents/Willem/Knowledge Base/`

## Step 1: Pick a note

If the user provided a note name as an argument (`$ARGUMENTS`), use that. Otherwise:

1. List all `.md` files in the Knowledge Base directory.
2. Read `index.html` in the repo root and extract all existing page filenames (the `href` values in `.page-link` elements).
3. Show the user which notes are **not yet published** and let them pick one.
4. If a note is already published, warn the user and ask if they want to update it.

## Step 2: Read and understand the note

Read the full Obsidian note. Pay attention to:
- Frontmatter tags (if any)
- Section structure (headings, subheadings)
- Code blocks, equations, diagrams
- Obsidian wiki-links (`[[...]]`) — resolve or remove them
- The depth and nature of the content (tutorial? reference? essay?)

## Step 3: Decide on the format

Based on the content, choose the **best interactive format**. The site already has several patterns you can reference:

| Content type | Format | Reference file |
|---|---|---|
| Step-by-step walkthrough | Paginated steps with progress dots, collapsible code | `gpt-walkthrough.html` |
| Deep explainer with math | Scrollable sections with KaTeX, interactive diagrams | `vae-elbo-explainer.html`, `sac_guide.html` |
| Tutorial with exercises | Sections + quiz/exercise blocks with reveal answers | `rl_study_quiz.html` |
| Reference / cheat sheet | Collapsible sections, search, copy buttons | `active-set-tutorial.html` |
| Interactive visualization | Canvas/WebGL + explanatory text | `gripper_viewer.html`, `lqr-tutorial.html` |

**Always prefer interactive elements** when they aid understanding:
- Collapsible sections for long content
- Toggle-to-reveal for answers/proofs
- Interactive diagrams (Canvas 2D) for algorithms or architectures
- Animated transitions between concepts
- Progress indicators for long reads
- Embedded quizzes to test understanding

## Step 4: Generate the HTML page

Create a **single, self-contained HTML file** in the repo root. Requirements:

### Filename
- Use kebab-case: `topic-name.html` (e.g., `dagger-imitation-learning.html`)

### Styling — match the site's dark theme
- Background: `#0a0a0f` or similar very dark
- Text: light gray (`#c8c5d0` to `#f0f0f0`)
- Accent color: pick one that fits the topic (existing pages use neon yellow `#e8ff47`, gold `#e8b430`, purple `#6a4a8a`, coral `#ff6b4a`)
- Fonts: Use Google Fonts — `IBM Plex Mono` or `JetBrains Mono` for code, `Crimson Pro` for body text, `Syne` or `Instrument Sans` for headings
- Responsive: must work on mobile
- All CSS inline in `<style>` — no external stylesheets (fonts via Google Fonts link are OK)

### Content quality
- **Expand and enrich** the Obsidian note — don't just convert markdown to HTML. Add:
  - Better explanations where the note is terse
  - Visual metaphors or diagrams
  - Practical examples
  - "Why does this matter?" context
- Preserve all technical accuracy from the original note
- Use KaTeX (`<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex/dist/katex.min.css">` + script) for any math
- Use syntax highlighting for code blocks (inline highlight or a lightweight lib)

### Interactive elements (pick what fits)
- **Collapsible code blocks** with toggle buttons
- **Step-through animations** for algorithms
- **Canvas diagrams** for architecture/flow
- **Quiz questions** with hidden answers
- **Tabbed views** for comparing approaches
- **Progress bar** for long reads
- **Smooth scroll navigation** with section dots

### Page structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Page Title]</title>
  <!-- Google Fonts -->
  <!-- KaTeX if needed -->
  <style>/* All styles inline */</style>
</head>
<body>
  <!-- Header with back link to index -->
  <!-- Hero/title section -->
  <!-- Main content with interactive elements -->
  <!-- Footer -->
  <script>/* All JS inline */</script>
</body>
</html>
```

## Step 5: Register in index.html

Add a new `<a class="page-link">` entry in the `#pages` div of `index.html`, **at the end** (before the closing `</div>` of `#pages`). Use this exact format:

```html
<a class="page-link" href="FILENAME.html" data-search="KEYWORDS lowercase no punctuation willem">
  <div>
    <div class="page-title">PAGE TITLE</div>
    <div class="page-meta">
      <span class="page-path">FILENAME.html</span>
      <span class="tag tag-willem">Willem</span>
    </div>
  </div>
  <span class="arrow">-></span>
</a>
```

**Important**: Use the tag `tag-willem` with text "Willem" (not "Jasper") since these are Willem's notes.

Check if a `.tag-willem` CSS rule exists in `index.html`. If not, add one near the other tag styles:
```css
.tag-willem { background: #1a3a2a; color: #4ade80; }
```

Also make sure the `data-search` attribute contains relevant lowercase keywords from the content for the search feature.

## Step 6: Show the user

After creating the page:
1. Tell the user the filename and a brief summary of what you created
2. Mention which interactive elements you added and why
3. Ask if they want you to commit the changes
4. Suggest they can preview it by opening the HTML file in a browser

## Notes
- Each page must be fully self-contained (no external JS/CSS dependencies except Google Fonts and KaTeX CDN)
- Never include the site's password protection in individual pages — that's only on index.html
- If the Obsidian note references other notes via wiki-links, mention what those are but don't try to convert them too
- Aim for pages that are genuinely useful for learning — not just formatted text dumps
