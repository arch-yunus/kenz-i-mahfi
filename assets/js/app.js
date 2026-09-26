// Kenz-i Mahfî Külliyatı - Web Viewer Application

let corpusData = [];
let currentDocId = "README.md";

document.addEventListener("DOMContentLoaded", async () => {
  initMermaid();
  await loadCorpus();
  setupEvents();
  renderNav();
  loadDocument(currentDocId);
});

function initMermaid() {
  if (window.mermaid) {
    mermaid.initialize({
      startOnLoad: false,
      theme: 'dark',
      themeVariables: {
        darkMode: true,
        background: '#070b12',
        primaryColor: '#d4af37',
        primaryTextColor: '#fff',
        lineColor: '#388bfd'
      }
    });
  }
}

async function loadCorpus() {
  try {
    const res = await fetch('data/corpus.json');
    if (!res.ok) throw new Error("Veri yüklenemedi");
    corpusData = await res.json();
  } catch (err) {
    console.error("Corpus yükleme hatası:", err);
    document.getElementById("docViewer").innerHTML = `
      <div style="text-align: center; padding: 40px;">
        <h2>⚠️ Veritabanı Yüklenemedi</h2>
        <p>Lütfen 'python scripts/build_site.py' komutunu çalıştırınız.</p>
      </div>
    `;
  }
}

function setupEvents() {
  const searchInput = document.getElementById("searchInput");
  searchInput.addEventListener("input", (e) => {
    filterNav(e.target.value.trim().toLowerCase());
  });

  const menuToggle = document.getElementById("menuToggle");
  const sidebar = document.getElementById("sidebar");
  menuToggle.addEventListener("click", () => {
    sidebar.classList.toggle("open");
  });

  const themeToggle = document.getElementById("themeToggle");
  themeToggle.addEventListener("click", () => {
    const currentTheme = document.body.getAttribute("data-theme");
    const newTheme = currentTheme === "light" ? "dark" : "light";
    document.body.setAttribute("data-theme", newTheme);
  });
}

function renderNav() {
  const navTree = document.getElementById("navTree");
  navTree.innerHTML = "";

  // Group documents by category
  const categories = {};
  corpusData.forEach(doc => {
    if (!categories[doc.category]) {
      categories[doc.category] = [];
    }
    categories[doc.category].push(doc);
  });

  for (const [catName, docs] of Object.entries(categories)) {
    const groupEl = document.createElement("div");
    groupEl.className = "nav-group";

    const titleEl = document.createElement("div");
    titleEl.className = "nav-group-title";
    titleEl.textContent = catName;
    groupEl.appendChild(titleEl);

    docs.forEach(doc => {
      const itemEl = document.createElement("a");
      itemEl.className = `nav-item ${doc.id === currentDocId ? 'active' : ''}`;
      itemEl.textContent = doc.title;
      itemEl.title = doc.title;
      itemEl.onclick = () => {
        loadDocument(doc.id);
        if (window.innerWidth <= 768) {
          document.getElementById("sidebar").classList.remove("open");
        }
      };
      groupEl.appendChild(itemEl);
    });

    navTree.appendChild(groupEl);
  }
}

function filterNav(query) {
  const navItems = document.querySelectorAll(".nav-item");
  navItems.forEach(item => {
    const text = item.textContent.toLowerCase();
    if (text.includes(query)) {
      item.style.display = "block";
    } else {
      item.style.display = "none";
    }
  });
}

async function loadDocument(docId) {
  currentDocId = docId;
  const doc = corpusData.find(d => d.id === docId);
  const docViewer = document.getElementById("docViewer");
  const currentCrumb = document.getElementById("currentCrumb");

  if (!doc) {
    docViewer.innerHTML = `<p>Belge bulunamadı: ${docId}</p>`;
    return;
  }

  currentCrumb.textContent = `${doc.category} > ${doc.title}`;

  // Update active item in sidebar
  document.querySelectorAll(".nav-item").forEach(el => {
    el.classList.toggle("active", el.title === doc.title);
  });

  // Render Markdown
  const renderedHtml = marked.parse(doc.content);
  docViewer.innerHTML = renderedHtml;
  docViewer.scrollTop = 0;

  // Render Mermaid diagrams if present
  if (window.mermaid) {
    setTimeout(() => {
      const mermaidCodeBlocks = docViewer.querySelectorAll('pre code.language-mermaid');
      mermaidCodeBlocks.forEach((block, idx) => {
        const parent = block.parentElement;
        const code = block.textContent;
        const mermaidDiv = document.createElement('div');
        mermaidDiv.className = 'mermaid';
        mermaidDiv.textContent = code;
        parent.replaceWith(mermaidDiv);
      });
      mermaid.run();
    }, 50);
  }
}
