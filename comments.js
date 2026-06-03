/* RFC comments widget.
 * Drop-in: include `<script src="/comments.js" defer></script>` before </body>.
 * It derives the page slug from the URL, fetches existing comments from
 * /api/comments, renders a thread + a post form, and persists via POST.
 * Styling mirrors the RFC pages' dark theme (var(--accent) etc., with fallbacks).
 */
(function () {
  "use strict";

  var PAGE = location.pathname.split("/").pop() || "index.html";
  var API = "/api/comments";
  var NAME_KEY = "rfc-comment-author";

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "text") node.textContent = attrs[k];
        else node.setAttribute(k, attrs[k]);
      });
    }
    (children || []).forEach(function (c) {
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  function fmtTime(ms) {
    try {
      return new Date(ms).toLocaleString(undefined, {
        year: "numeric", month: "short", day: "numeric",
        hour: "2-digit", minute: "2-digit",
      });
    } catch (e) {
      return "";
    }
  }

  function injectStyles() {
    if (document.getElementById("rfc-comments-style")) return;
    var css =
      "#rfc-comments{max-width:860px;margin:48px auto 80px;padding:0 16px;" +
      "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;}" +
      "#rfc-comments h2{font-size:18px;letter-spacing:.04em;text-transform:uppercase;" +
      "color:var(--accent,#4ea1ff);border-bottom:1px solid var(--line,#262b36);padding-bottom:10px;margin-bottom:8px;}" +
      "#rfc-comments .rfc-c-count{color:var(--muted,#8b93a7);font-size:13px;margin:0 0 20px;}" +
      "#rfc-comments .rfc-c-list{display:flex;flex-direction:column;gap:14px;margin-bottom:28px;}" +
      "#rfc-comments .rfc-c{background:var(--panel,#161a22);border:1px solid var(--line,#262b36);" +
      "border-left:3px solid var(--accent,#4ea1ff);border-radius:8px;padding:12px 16px;}" +
      "#rfc-comments .rfc-c-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:6px;}" +
      "#rfc-comments .rfc-c-author{font-weight:600;color:var(--text,#e6e9ef);font-size:14px;}" +
      "#rfc-comments .rfc-c-ts{color:var(--muted,#8b93a7);font-size:12px;white-space:nowrap;}" +
      "#rfc-comments .rfc-c-body{color:var(--text,#e6e9ef);font-size:14px;line-height:1.55;white-space:pre-wrap;word-wrap:break-word;}" +
      "#rfc-comments .rfc-c-empty{color:var(--muted,#8b93a7);font-size:14px;font-style:italic;}" +
      "#rfc-comments form{background:var(--panel,#161a22);border:1px solid var(--line,#262b36);" +
      "border-radius:10px;padding:16px;display:flex;flex-direction:column;gap:10px;}" +
      "#rfc-comments input,#rfc-comments textarea{background:var(--bg,#0f1115);color:var(--text,#e6e9ef);" +
      "border:1px solid var(--line,#262b36);border-radius:6px;padding:9px 11px;font-size:14px;font-family:inherit;width:100%;box-sizing:border-box;}" +
      "#rfc-comments input:focus,#rfc-comments textarea:focus{outline:none;border-color:var(--accent,#4ea1ff);}" +
      "#rfc-comments textarea{min-height:84px;resize:vertical;line-height:1.5;}" +
      "#rfc-comments .rfc-c-bar{display:flex;justify-content:space-between;align-items:center;gap:12px;}" +
      "#rfc-comments button{background:var(--accent,#4ea1ff);color:#0a0c11;border:none;border-radius:6px;" +
      "padding:9px 18px;font-size:14px;font-weight:600;cursor:pointer;font-family:inherit;}" +
      "#rfc-comments button:disabled{opacity:.5;cursor:default;}" +
      "#rfc-comments .rfc-c-msg{font-size:13px;color:var(--muted,#8b93a7);}" +
      "#rfc-comments .rfc-c-msg.err{color:#ff6b6b;}";
    var style = el("style", { id: "rfc-comments-style" });
    style.textContent = css;
    document.head.appendChild(style);
  }

  function render(root, comments) {
    var list = root.querySelector(".rfc-c-list");
    var count = root.querySelector(".rfc-c-count");
    list.textContent = "";
    count.textContent = comments.length === 1 ? "1 comment" : comments.length + " comments";
    if (!comments.length) {
      list.appendChild(el("div", { class: "rfc-c-empty", text: "No comments yet — be the first." }));
      return;
    }
    comments.forEach(function (c) {
      list.appendChild(
        el("div", { class: "rfc-c" }, [
          el("div", { class: "rfc-c-head" }, [
            el("span", { class: "rfc-c-author", text: c.author || "Anonymous" }),
            el("span", { class: "rfc-c-ts", text: c.ts ? fmtTime(c.ts) : "" }),
          ]),
          el("div", { class: "rfc-c-body", text: c.body || "" }),
        ])
      );
    });
  }

  function setMsg(root, text, isErr) {
    var msg = root.querySelector(".rfc-c-msg");
    msg.textContent = text || "";
    msg.className = "rfc-c-msg" + (isErr ? " err" : "");
  }

  function load(root) {
    fetch(API + "?page=" + encodeURIComponent(PAGE))
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        if (!res.ok) throw new Error(res.j.error || "failed to load comments");
        render(root, res.j.comments || []);
      })
      .catch(function (e) {
        setMsg(root, "Could not load comments: " + e.message, true);
      });
  }

  function submit(root, e) {
    e.preventDefault();
    var authorEl = root.querySelector("input[name=author]");
    var bodyEl = root.querySelector("textarea[name=body]");
    var btn = root.querySelector("button");
    var author = authorEl.value.trim();
    var body = bodyEl.value.trim();
    if (!body) { setMsg(root, "Write something first.", true); return; }
    if (author) localStorage.setItem(NAME_KEY, author);

    btn.disabled = true;
    setMsg(root, "Posting…", false);
    fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ page: PAGE, author: author, body: body }),
    })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        if (!res.ok) throw new Error(res.j.error || "failed to post");
        bodyEl.value = "";
        setMsg(root, "", false);
        load(root);
      })
      .catch(function (err) {
        setMsg(root, "Could not post: " + err.message, true);
      })
      .finally(function () { btn.disabled = false; });
  }

  function mount() {
    injectStyles();
    var root = el("section", { id: "rfc-comments" });
    root.appendChild(el("h2", { text: "Comments" }));
    root.appendChild(el("p", { class: "rfc-c-count", text: "Loading…" }));
    root.appendChild(el("div", { class: "rfc-c-list" }));

    var form = el("form");
    form.appendChild(el("input", {
      type: "text", name: "author", placeholder: "Your name",
      value: localStorage.getItem(NAME_KEY) || "", maxlength: "80",
    }));
    form.appendChild(el("textarea", {
      name: "body", placeholder: "Add a comment…", maxlength: "5000",
    }));
    var bar = el("div", { class: "rfc-c-bar" }, [
      el("span", { class: "rfc-c-msg" }),
      el("button", { type: "submit", text: "Post comment" }),
    ]);
    form.appendChild(bar);
    form.addEventListener("submit", function (e) { submit(root, e); });
    root.appendChild(form);

    document.body.appendChild(root);
    load(root);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
