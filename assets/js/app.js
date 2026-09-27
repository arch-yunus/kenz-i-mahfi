// Kenz-i Mahfî Külliyatı - Gelişmiş Web Viewer & İrfan Kütüphanesi

let corpusData = [];
let glossaryData = [];
let currentDocId = "README.md";
let activeTag = "all";
let currentFontSize = 16;

const WISDOM_QUOTES = [
  {
    quote: "كُنْتُ كَنْزاً مَخْفِيّاً فَأَحْبَبْتُ أَنْ أُعْرَفَ فَخَلَقْتُ الْخَلْقَ لِيَعْرِفُونِي",
    meaning: "Ben gizli bir hazine idim; bilinmeyi istedim/sevdim ve bilinmek için mahlûkatı yarattım.",
    author: "Kenz-i Mahfî Hadis-i Kudsîsi"
  },
  {
    quote: "Gözsüz beni görsün deyu, dilsiz beni sorsun deyu / İki cihanı halk eden bir gizli gence aşk olsun.",
    meaning: "İlahi muhabbet, Gayb hazinesini aşikâr kılan ezelî sırdır.",
    author: "Niyâzî-i Mısrî"
  },
  {
    quote: "Mahlûkat Hakk'ın isimlerinin aynalarıdır. Sen o aynaya baktığında sadece Hakk'ın zâtını ve tecellisini görürsün.",
    meaning: "Varlıkta Hakk'tan gayrı hakiki vücûd yoktur; kesret bir tecelli cümbüşüdür.",
    author: "Muhyiddin İbnü'l-Arabî, Fütûhât"
  },
  {
    quote: "Daha üzüm bağı yaratılmadan önce, Sevgilinin zikriyle öyle bir ezel şarabı içtik ki mest olduk!",
    meaning: "Ruhların bezm-i elestteki ezelî sarhoşluğu kâinattan öncedir.",
    author: "İbnü'l-Fârız, el-Hamriyye"
  },
  {
    quote: "Mende sığar iki cihân men bu cihâna sığmazam / Gevher-i lâ-mekân menem kevn ü mekâna sığmazam.",
    meaning: "İnsân-ı Kâmil, Kenz-i Mahfî'nin hem mekânı hem de mekânlar üstü hakikatidir.",
    author: "Seyyid Nesîmî"
  },
  {
    quote: "Aşk bir güneştir ki onun batışı yoktur. Kenz-i Mahfî'nin sırrına ancak kalbini ayna kılan ârifler erer.",
    meaning: "Aşk varlığın cevheridir.",
    author: "Mevlânâ Celâleddîn-i Rûmî"
  },
  {
    quote: "Âlem bir ulu ağaçtır; tohumu Kenz-i Mahfî, meyvesi ise İnsân-ı Kâmil'dir.",
    meaning: "Tohumdaki sır ağaçtan geçerek meyvenin çekirdeğinde yeniden zuhûr eder.",
    author: "Azîzüddîn Nesefî"
  },
  {
    quote: "Varlık tektir ve o da Nûr-ı Mutlak'tır. Karanlık ise nûrun yokluğundan ibaret bir vehimdir.",
    meaning: "İşrâkî nur metafiziği.",
    author: "Şehâbeddin Sühreverdî"
  }
];

document.addEventListener("DOMContentLoaded", async () => {
  initMermaid();
  await loadData();
  setupEvents();
  renderNav();
  updateStats();
  
  // Check URL hash for direct document loading
  if (window.location.hash) {
    const targetId = decodeURIComponent(window.location.hash.substring(1));
    if (corpusData.some(d => d.id === targetId)) {
      currentDocId = targetId;
    }
  }
  
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

async function loadData() {
  try {
    const resCorpus = await fetch('data/corpus.json');
    if (resCorpus.ok) {
      corpusData = await resCorpus.json();
    }
    
    const resGlossary = await fetch('data/glossary.json');
    if (resGlossary.ok) {
      glossaryData = await resGlossary.json();
    }
  } catch (err) {
    console.error("Veri yükleme hatası:", err);
    document.getElementById("docViewer").innerHTML = `
      <div style="text-align: center; padding: 60px;">
        <h2>⚠️ Külliyat Veritabanı Yüklenemedi</h2>
        <p>Lütfen terminalde <code>python scripts/build_site.py</code> komutunu çalıştırınız.</p>
      </div>
    `;
  }
}

function updateStats() {
  const statDocs = document.getElementById("statDocsCount");
  const statWords = document.getElementById("statWordsCount");
  if (statDocs && corpusData.length) {
    statDocs.textContent = `📚 ${corpusData.length} Doküman`;
  }
  if (statWords && corpusData.length) {
    const totalWords = corpusData.reduce((acc, cur) => acc + (cur.wordCount || 0), 0);
    statWords.textContent = `✍️ ${totalWords.toLocaleString()} Kelime`;
  }
}

function setupEvents() {
  // Search
  const searchInput = document.getElementById("searchInput");
  const clearSearch = document.getElementById("clearSearch");
  
  searchInput.addEventListener("input", (e) => {
    const query = e.target.value.trim().toLowerCase();
    clearSearch.style.display = query ? "block" : "none";
    filterCorpus(query);
  });
  
  clearSearch.addEventListener("click", () => {
    searchInput.value = "";
    clearSearch.style.display = "none";
    filterCorpus("");
  });

  // Tag filter pills
  const tagFilters = document.getElementById("tagFilters");
  tagFilters.addEventListener("click", (e) => {
    if (e.target.classList.contains("tag-pill")) {
      document.querySelectorAll(".tag-pill").forEach(p => p.classList.remove("active"));
      e.target.classList.add("active");
      activeTag = e.target.getAttribute("data-tag");
      filterCorpus(searchInput.value.trim().toLowerCase());
    }
  });

  // Sidebar toggle
  const menuToggle = document.getElementById("menuToggle");
  const sidebar = document.getElementById("sidebar");
  menuToggle.addEventListener("click", () => {
    sidebar.classList.toggle("open");
  });

  // Theme toggle
  const themeToggle = document.getElementById("themeToggle");
  themeToggle.addEventListener("click", () => {
    const currentTheme = document.body.getAttribute("data-theme");
    const newTheme = currentTheme === "light" ? "dark" : "light";
    document.body.setAttribute("data-theme", newTheme);
    showToast(`Tema değiştirildi: ${newTheme === 'light' ? 'Aydınlık' : 'Karanlık'}`);
  });

  // Font resizing
  document.getElementById("fontInc").addEventListener("click", () => {
    if (currentFontSize < 24) {
      currentFontSize += 1.5;
      document.getElementById("docViewer").style.fontSize = `${currentFontSize}px`;
    }
  });
  document.getElementById("fontDec").addEventListener("click", () => {
    if (currentFontSize > 13) {
      currentFontSize -= 1.5;
      document.getElementById("docViewer").style.fontSize = `${currentFontSize}px`;
    }
  });

  // Print
  document.getElementById("printBtn").addEventListener("click", () => {
    window.print();
  });

  // Wisdom Modal
  const wisdomModal = document.getElementById("wisdomModal");
  document.getElementById("wisdomBtn").addEventListener("click", () => {
    showWisdomQuote();
    wisdomModal.classList.add("open");
  });
  document.getElementById("closeWisdom").addEventListener("click", () => {
    wisdomModal.classList.remove("open");
  });
  document.getElementById("nextWisdomBtn").addEventListener("click", () => {
    showWisdomQuote();
  });

  // Glossary Modal
  const glossaryModal = document.getElementById("glossaryModal");
  document.getElementById("glossaryBtn").addEventListener("click", () => {
    renderGlossary();
    glossaryModal.classList.add("open");
  });
  document.getElementById("closeGlossary").addEventListener("click", () => {
    glossaryModal.classList.remove("open");
  });
  
  const glossarySearchInput = document.getElementById("glossarySearchInput");
  glossarySearchInput.addEventListener("input", (e) => {
    renderGlossary(e.target.value.trim().toLowerCase());
  });

  // Close modals on outside click
  window.addEventListener("click", (e) => {
    if (e.target === wisdomModal) wisdomModal.classList.remove("open");
    if (e.target === glossaryModal) glossaryModal.classList.remove("open");
  });

  // Scroll Reading Progress Bar
  const docViewer = document.getElementById("docViewer");
  docViewer.addEventListener("scroll", () => {
    const scrollTop = docViewer.scrollTop;
    const scrollHeight = docViewer.scrollHeight - docViewer.clientHeight;
    const progress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
    document.getElementById("readingProgressBar").style.width = `${progress}%`;
  });
}

function showWisdomQuote() {
  const quote = WISDOM_QUOTES[Math.floor(Math.random() * WISDOM_QUOTES.length)];
  const container = document.getElementById("wisdomContent");
  container.innerHTML = `
    <div class="quote-box">
      "${quote.quote}"
    </div>
    <p style="font-size: 1.05rem; margin-bottom: 12px; color: var(--text-primary);">
      ${quote.meaning}
    </p>
    <div class="quote-author">
      — ${quote.author}
    </div>
  `;
}

function renderGlossary(filter = "") {
  const container = document.getElementById("glossaryList");
  if (!glossaryData || !glossaryData.length) {
    container.innerHTML = "<p>Sözlük verisi yüklenemedi.</p>";
    return;
  }

  const filtered = glossaryData.filter(item => {
    return item.term.toLowerCase().includes(filter) ||
           (item.alt && item.alt.toLowerCase().includes(filter)) ||
           item.definition.toLowerCase().includes(filter);
  });

  if (!filtered.length) {
    container.innerHTML = "<p>Eşleşen kavram bulunamadı.</p>";
    return;
  }

  container.innerHTML = filtered.map(item => `
    <div class="glossary-item">
      <div class="glossary-term">
        ${item.term}
        ${item.alt ? `<span class="glossary-alt">(${item.alt})</span>` : ''}
      </div>
      <div class="glossary-def">${item.definition}</div>
    </div>
  `).join("");
}

function renderNav() {
  const navTree = document.getElementById("navTree");
  navTree.innerHTML = "";

  // Group by category
  const categories = {};
  corpusData.forEach(doc => {
    const cat = doc.category || "00. Genel";
    if (!categories[cat]) categories[cat] = [];
    categories[cat].push(doc);
  });

  for (const [catName, docs] of Object.entries(categories)) {
    const groupEl = document.createElement("div");
    groupEl.className = "nav-group";

    const headerEl = document.createElement("div");
    headerEl.className = "nav-group-header";
    headerEl.innerHTML = `
      <span>${catName}</span>
      <span class="nav-group-count">${docs.length}</span>
    `;
    groupEl.appendChild(headerEl);

    const itemsContainer = document.createElement("div");
    itemsContainer.className = "nav-group-items";

    docs.forEach(doc => {
      const itemEl = document.createElement("a");
      itemEl.className = `nav-item ${doc.id === currentDocId ? 'active' : ''}`;
      itemEl.setAttribute("data-id", doc.id);
      itemEl.setAttribute("data-tags", (doc.tags || []).join(","));
      itemEl.innerHTML = `<span class="nav-item-title" title="${doc.title}">${doc.title}</span>`;
      
      itemEl.onclick = () => {
        loadDocument(doc.id);
        if (window.innerWidth <= 900) {
          document.getElementById("sidebar").classList.remove("open");
        }
      };
      itemsContainer.appendChild(itemEl);
    });

    groupEl.appendChild(itemsContainer);
    navTree.appendChild(groupEl);
  }
}

function filterCorpus(query) {
  const navItems = document.querySelectorAll(".nav-item");
  const navGroups = document.querySelectorAll(".nav-group");

  navGroups.forEach(group => {
    let visibleCount = 0;
    const items = group.querySelectorAll(".nav-item");
    
    items.forEach(item => {
      const id = item.getAttribute("data-id");
      const doc = corpusData.find(d => d.id === id);
      if (!doc) return;

      const titleMatch = doc.title.toLowerCase().includes(query);
      const contentMatch = query.length > 2 && doc.content.toLowerCase().includes(query);
      const tagMatch = activeTag === "all" || (doc.tags && doc.tags.includes(activeTag));

      if ((titleMatch || contentMatch) && tagMatch) {
        item.style.display = "flex";
        visibleCount++;
      } else {
        item.style.display = "none";
      }
    });

    group.style.display = visibleCount > 0 ? "block" : "none";
  });
}

async function loadDocument(docId) {
  currentDocId = docId;
  window.location.hash = encodeURIComponent(docId);
  
  const doc = corpusData.find(d => d.id === docId);
  const docViewer = document.getElementById("docViewer");
  const currentCrumb = document.getElementById("currentCrumb");

  if (!doc) {
    docViewer.innerHTML = `<p>Belge bulunamadı: ${docId}</p>`;
    return;
  }

  currentCrumb.textContent = `${doc.category} > ${doc.title}`;

  // Update active sidebar state
  document.querySelectorAll(".nav-item").forEach(el => {
    el.classList.toggle("active", el.getAttribute("data-id") === docId);
  });

  // Build Table of Contents HTML if headings exist
  let tocHtml = "";
  if (doc.headings && doc.headings.length > 1) {
    tocHtml = `
      <div class="doc-toc">
        <div class="doc-toc-title">📑 İçindekiler</div>
        <ul>
          ${doc.headings.map(h => `
            <li class="level-${h.level}">
              <a href="#heading-${encodeURIComponent(h.text)}">${h.text}</a>
            </li>
          `).join("")}
        </ul>
      </div>
    `;
  }

  // Meta Badges
  const badgesHtml = `
    <div class="doc-meta-header">
      <div class="doc-meta-badges">
        <span class="doc-badge">${doc.category}</span>
        <span class="doc-badge doc-badge-time">⏱️ ${doc.readingTime || '5 dk okuma'}</span>
        <span class="doc-badge">✍️ ${(doc.wordCount || 0).toLocaleString()} Kelime</span>
        ${(doc.tags || []).map(t => `<span class="doc-badge">🏷️ ${t}</span>`).join("")}
      </div>
      <div class="doc-actions-quick">
        <button class="doc-quick-btn" onclick="copyShareLink()">🔗 Bağlantıyı Kopyala</button>
      </div>
    </div>
  `;

  // Render Markdown
  let renderedHtml = marked.parse(doc.content);

  // Inject IDs to headings for TOC jump
  if (doc.headings) {
    doc.headings.forEach(h => {
      const targetTagH2 = `<h2>${h.text}</h2>`;
      const replaceTagH2 = `<h2 id="heading-${encodeURIComponent(h.text)}">${h.text}</h2>`;
      const targetTagH3 = `<h3>${h.text}</h3>`;
      const replaceTagH3 = `<h3 id="heading-${encodeURIComponent(h.text)}">${h.text}</h3>`;
      renderedHtml = renderedHtml.replace(targetTagH2, replaceTagH2).replace(targetTagH3, replaceTagH3);
    });
  }

  docViewer.innerHTML = badgesHtml + tocHtml + renderedHtml;
  docViewer.scrollTop = 0;

  // Render Mermaid diagrams
  if (window.mermaid) {
    setTimeout(() => {
      const mermaidCodeBlocks = docViewer.querySelectorAll('pre code.language-mermaid');
      mermaidCodeBlocks.forEach(block => {
        const parent = block.parentElement;
        const code = block.textContent;
        const mermaidDiv = document.createElement('div');
        mermaidDiv.className = 'mermaid';
        mermaidDiv.textContent = code;
        parent.replaceWith(mermaidDiv);
      });
      mermaid.run();
    }, 60);
  }
}

window.copyShareLink = function() {
  const url = window.location.href;
  navigator.clipboard.writeText(url).then(() => {
    showToast("Belge bağlantısı panoya kopyalandı!");
  }).catch(() => {
    showToast("Bağlantı kopyalanamadı.");
  });
};

function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, 2500);
}
