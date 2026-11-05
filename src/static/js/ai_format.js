
(function () {
  "use strict";

  function escapeHTML(text) {
    return text.replace(/[&<>"']/g, function (c) {
      return {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
      }[c];
    });
  }

  function inlineFormat(text) {
    return escapeHTML(text)
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/(?<!\*)\*([^*\n]+)\*(?!\*)/g, "<em>$1</em>");
  }

  function renderMarkdown(text) {
    const lines = String(text || "").split(/\r?\n/);
    let html = "";
    let list = null;

    function closeList() {
      if (list) {
        html += "</" + list + ">";
        list = null;
      }
    }

    for (const line of lines) {
      const s = line.trim();

      if (!s) {
        closeList();
        continue;
      }

      if (/^#{1,3}\s/.test(s)) {
        closeList();
        const level = s.match(/^#+/)[0].length;
        html += "<h" + level + ">" +
          inlineFormat(s.replace(/^#{1,3}\s+/, "")) +
          "</h" + level + ">";
      } else if (/^[-*]\s+/.test(s)) {
        if (list !== "ul") {
          closeList();
          html += "<ul>";
          list = "ul";
        }
        html += "<li>" + inlineFormat(s.slice(2)) + "</li>";
      } else if (/^\d+\.\s+/.test(s)) {
        if (list !== "ol") {
          closeList();
          html += "<ol>";
          list = "ol";
        }
        html += "<li>" +
          inlineFormat(s.replace(/^\d+\.\s+/, "")) +
          "</li>";
      } else if (/^---+$/.test(s)) {
        closeList();
        html += "<hr>";
      } else {
        closeList();
        html += "<p>" + inlineFormat(s) + "</p>";
      }
    }

    closeList();
    return html;
  }

  function formatResults() {
    const candidates = document.querySelectorAll(
      "#ai-result, #aiResult, #ai-output, #aiOutput, " +
      "#analysis-result, #analysisResult, #analysis-output"
    );

    candidates.forEach(function (el) {
      if (el.dataset.dgFormatted === "yes") return;

      const text = el.textContent || "";

      if (!text.trim()) return;

      el.innerHTML = renderMarkdown(text);
      el.classList.add("dg-ai-formatted");
      el.dataset.dgFormatted = "yes";
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    formatResults();

    const observer = new MutationObserver(function () {
      formatResults();
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true
    });
  });
})();
