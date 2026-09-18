(function () {
  const body = document.body;
  const toggle = document.getElementById('lang-toggle');
  const saved = localStorage.getItem('astrabuild-lang');
  const queryLang = new URLSearchParams(window.location.search).get('lang');
  const preferred = queryLang || saved || (navigator.language && navigator.language.toLowerCase().startsWith('zh') ? 'zh' : 'en');

  function setLang(lang) {
    const zh = lang === 'zh';
    body.classList.toggle('zh', zh);
    document.documentElement.lang = zh ? 'zh-CN' : 'en';
    if (toggle) {
      toggle.textContent = zh ? 'EN' : '中文';
      toggle.setAttribute('aria-label', zh ? 'Switch to English' : '切换到中文');
      toggle.setAttribute('aria-pressed', String(zh));
    }
    localStorage.setItem('astrabuild-lang', zh ? 'zh' : 'en');
  }

  setLang(preferred === 'zh' ? 'zh' : 'en');
  if (toggle) {
    toggle.addEventListener('click', () => setLang(body.classList.contains('zh') ? 'en' : 'zh'));
  }

  const tocLinks = Array.from(document.querySelectorAll('.toc a[href^="#"]'));
  const navLinks = Array.from(document.querySelectorAll('.nav a[href^="#"], .toc a[href^="#"], a.episode-link[href^="#"]'));

  navLinks.forEach((anchor) => {
    anchor.addEventListener('click', (event) => {
      const id = anchor.getAttribute('href').slice(1);
      const node = document.getElementById(id);
      if (!node) return;
      event.preventDefault();
      node.scrollIntoView({ behavior: 'smooth', block: 'start' });
      history.replaceState(null, '', `#${id}`);
    });
  });

  // Re-align direct deep links after media/CSS have settled. This avoids an
  // early browser hash jump landing beyond the final layout on media-heavy pages.
  window.addEventListener('load', () => {
    if (!window.location.hash) return;
    const target = document.getElementById(window.location.hash.slice(1));
    if (!target) return;
    window.setTimeout(() => target.scrollIntoView({ behavior: 'auto', block: 'start' }), 80);
  });

  const sections = tocLinks
    .map((link) => document.getElementById(link.getAttribute('href').slice(1)))
    .filter(Boolean);

  function setActiveToc(id) {
    tocLinks.forEach((link) => {
      const active = link.getAttribute('href') === `#${id}`;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }

  if ('IntersectionObserver' in window && sections.length) {
    const visible = new Map();
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) visible.set(entry.target.id, entry.boundingClientRect.top);
        else visible.delete(entry.target.id);
      });
      if (!visible.size) return;
      const active = [...visible.entries()].sort((a, b) => Math.abs(a[1] - 96) - Math.abs(b[1] - 96))[0][0];
      setActiveToc(active);
    }, { rootMargin: '-80px 0px -62% 0px', threshold: [0, 0.01, 0.2] });
    sections.forEach((section) => observer.observe(section));
  }

  const heroVideo = document.querySelector('.hero-video-frame video');
  const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (heroVideo && reduceMotion) heroVideo.pause();
  document.addEventListener('visibilitychange', () => {
    if (!heroVideo || reduceMotion) return;
    if (document.hidden) heroVideo.pause();
    else heroVideo.play().catch(() => {});
  });

  async function loadMetrics() {
    const status = document.getElementById('metrics-status');
    try {
      const response = await fetch('../release/metrics.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      document.querySelectorAll('[data-metric]').forEach((node) => {
        const item = data.headline.find((m) => m.id === node.dataset.metric);
        if (item) node.textContent = item.display;
      });
      if (status) status.textContent = `metrics.json · ${data.release}`;
    } catch (error) {
      if (status) status.textContent = 'Static metric fallback (serve over HTTP to load metrics.json)';
    }
  }

  function escapeHtml(value) {
    return String(value ?? '')
      .replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;').replaceAll("'", '&#039;');
  }

  function dossierLink(path, label) {
    if (!path) return '';
    return `<a href="${escapeHtml(path)}" target="_blank" rel="noopener">${escapeHtml(label)} ↗</a>`;
  }

  function renderDossier(dossier) {
    const familyNode = document.getElementById('dossier-family');
    const stageNode = document.getElementById('dossier-stage-strip');
    const content = document.getElementById('dossier-content');
    if (!content || !dossier) return;

    if (familyNode) familyNode.textContent = `${dossier.family} · ${dossier.image_count} images · ${dossier.output_file_count} files`;
    if (stageNode) {
      stageNode.innerHTML = dossier.stages.map((stage) => `<span>${escapeHtml(stage)}</span>`).join('');
    }

    const triplets = (dossier.view_triplets || []).slice(0, 4);
    const loose = (dossier.loose_views || []).slice(0, triplets.length ? 4 : 8);
    const process = (dossier.process_media || []).slice(0, 8);

    const tripletHtml = triplets.map((triplet) => {
      const cells = [
        ['clean', triplet.clean], ['overlay', triplet.overlay], ['reference', triplet.reference],
      ].filter(([, path]) => path).map(([role, path]) => `
        <a class="dossier-image" href="${escapeHtml(path)}" target="_blank" rel="noopener">
          <img loading="lazy" src="${escapeHtml(path)}" alt="${escapeHtml(dossier.batch)} ${escapeHtml(triplet.label)} ${role}">
          <span>${role}</span>
        </a>`).join('');
      return `<article class="dossier-triplet"><h4>${escapeHtml(triplet.label)}</h4><div>${cells}</div></article>`;
    }).join('');

    const looseHtml = loose.map((item) => `
      <a class="dossier-image" href="${escapeHtml(item.path)}" target="_blank" rel="noopener">
        <img loading="lazy" src="${escapeHtml(item.path)}" alt="${escapeHtml(item.name)}">
        <span>${escapeHtml(item.role)} · ${escapeHtml(item.name.replace(/^\d+_/, ''))}</span>
      </a>`).join('');

    const processHtml = process.length ? process.map((item) => `
      <a class="process-media-card" href="${escapeHtml(item.path)}" target="_blank" rel="noopener">
        <img loading="lazy" src="${escapeHtml(item.path)}" alt="${escapeHtml(item.name)}">
        <b>${escapeHtml(item.role)}</b><span>${escapeHtml(item.name)}</span>
      </a>`).join('') : `<p class="empty-process"><span class="lang-en">No dedicated profile/preflight/diagnostic image is recorded for this batch; its evidence is primarily the standard render/validation chain.</span><span class="lang-zh">该批次没有单独的 profile/preflight/diagnostic 图片；其过程证据主要由标准渲染与验证链构成。</span></p>`;

    const links = [
      dossierLink(dossier.review_page, 'original review'),
      dossierLink(dossier.continuation, 'continuation'),
      dossierLink(dossier.inputs, 'inputs'),
      dossierLink(dossier.measurements, 'measurements'),
      dossierLink(dossier.plan, 'plan'),
      dossierLink(dossier.validation, 'validation'),
      dossierLink(dossier.review_checks, 'review checks'),
      dossierLink(dossier.manifest, 'manifest'),
      dossierLink(dossier.coverage, 'coverage'),
    ].filter(Boolean).join('');

    const reviewHtml = dossier.review_page ? `
      <details class="original-review dossier-original-review">
        <summary><span class="lang-en">Open the batch's original interactive review page</span><span class="lang-zh">打开该批次原始交互式审查网页</span></summary>
        <div class="review-description"><span class="lang-en">This historical page was generated during the batch itself. It may contain same-camera sliders, multiple views, embedded source/reference images, or batch-specific review controls.</span><span class="lang-zh">这是批次执行时生成的历史审查网页，可能包含同机位滑块、多方向视图、内嵌粗模/参考图以及该批次专用审查控件。</span></div>
        <div class="review-actions"><button type="button" class="btn load-review" data-review-src="${escapeHtml(dossier.review_page)}" data-review-target="dossier-original-review-frame"><span class="lang-en">Load original review</span><span class="lang-zh">加载原始审查页</span></button>${dossierLink(dossier.review_page, 'open in new tab')}</div>
        <iframe id="dossier-original-review-frame" class="review-frame" title="${escapeHtml(dossier.batch)} original reconstruction review" loading="lazy" sandbox="allow-scripts allow-same-origin"></iframe>
      </details>` : '';

    content.innerHTML = `
      <div class="dossier-summary">
        <div><span>batch</span><strong>${escapeHtml(dossier.batch)}</strong></div>
        <div><span>recorded stages</span><strong>${dossier.stages.length}</strong></div>
        <div><span>review triplets</span><strong>${triplets.length}</strong></div>
        <div><span>process graphics</span><strong>${process.length}</strong></div>
      </div>
      <div class="dossier-block">
        <div class="dossier-block-head"><h3><span class="lang-en">Result gallery</span><span class="lang-zh">结果装配图库</span></h3><p><span class="lang-en">Station/local clean, overlay and reference views from the frozen batch.</span><span class="lang-zh">来自冻结批次的整站/局部 clean、overlay 与 reference 视图。</span></p></div>
        ${tripletHtml || `<div class="loose-view-grid">${looseHtml}</div>`}
        ${tripletHtml && looseHtml ? `<details class="more-views"><summary><span class="lang-en">Additional unmatched review views</span><span class="lang-zh">更多未成三联组的审查视图</span></summary><div class="loose-view-grid">${looseHtml}</div></details>` : ''}
      </div>
      <div class="dossier-block">
        <div class="dossier-block-head"><h3><span class="lang-en">Process evidence</span><span class="lang-zh">过程证据</span></h3><p><span class="lang-en">Task-specific measurement, preflight, fitting or diagnostic artifacts. Their presence varies by task.</span><span class="lang-zh">按任务产生的 measurement、preflight、拟合或诊断产物；并非每个批次都有全部类型。</span></p></div>
        <div class="process-media-grid">${processHtml}</div>
      </div>
      ${reviewHtml}
      <div class="dossier-artifacts"><b><span class="lang-en">Frozen records</span><span class="lang-zh">冻结记录</span></b>${links || '<span>—</span>'}</div>`;
  }

  document.addEventListener('click', (event) => {
    const button = event.target.closest && event.target.closest('.load-review[data-review-src]');
    if (!button) return;
    const target = document.getElementById(button.dataset.reviewTarget);
    if (!target) return;
    if (!target.src || target.src === 'about:blank') target.src = button.dataset.reviewSrc;
    target.classList.add('loaded');
    button.disabled = true;
    const zh = body.classList.contains('zh');
    button.textContent = zh ? '已加载原始审查页' : 'Original review loaded';
  });

  // Unified three-mode viewer: one representative fixed-camera view per batch.
  // Selection priority: first non-station triplet with clean+overlay+reference;
  // else first triplet with clean+overlay; else first triplet with any image;
  // else first loose view (model mode only).
  const VIEW_BANDS = [
    { id: 'repeated', test: (b) => /^B(0[7-9]|1[0-9])$/.test(b), label: 'Band · Repeated equipment 重复设备 · B07–B19' },
    { id: 'connected', test: (b) => /^B(2[0-9]|30)$/.test(b), label: 'Band · Connected systems 连接系统 · B20–B30' },
    { id: 'closure', test: (b) => /^B3[1-6]$/.test(b), label: 'Band · Site closure 整站收尾 · B31–B36' },
    { id: 'extended', test: () => true, label: 'Extended record (outside B01–B36) 扩展记录（超出 B01–B36 范围）' },
  ];

  function pickRepresentativeView(d) {
    const triplets = d.view_triplets || [];
    const full = triplets.find((t) => !t.is_station && t.clean && t.overlay && t.reference);
    if (full) return full;
    const pair = triplets.find((t) => t.clean && t.overlay);
    if (pair) return pair;
    const any = triplets.find((t) => t.clean || t.overlay || t.reference);
    if (any) return any;
    const loose = (d.loose_views || [])[0];
    return loose ? { label: loose.name, clean: loose.path, overlay: null, reference: null } : null;
  }

  function setupReviewGallery(dossiers) {
    const batchSelect = document.getElementById('view-batch-select');
    const image = document.getElementById('view-image');
    const caption = document.getElementById('view-caption');
    const original = document.getElementById('view-original');
    const prev = document.getElementById('view-prev');
    const next = document.getElementById('view-next');
    const modeButtons = ['clean', 'overlay', 'reference']
      .map((mode) => document.getElementById(`view-mode-${mode}`)).filter(Boolean);
    if (!batchSelect || !image || !caption || !original || !modeButtons.length) return;

    const reviews = dossiers
      .filter((d) => d.review_page)
      .map((d) => ({ dossier: d, view: pickRepresentativeView(d) }))
      .filter((entry) => entry.view);
    if (!reviews.length) return;

    batchSelect.innerHTML = VIEW_BANDS.map((band) => {
      const options = reviews
        .filter((entry) => band.test(entry.dossier.batch))
        .map((entry) => `<option value="${escapeHtml(entry.dossier.batch)}">${escapeHtml(entry.dossier.batch)} · ${escapeHtml(entry.dossier.review_title || entry.dossier.family)}</option>`)
        .join('');
      return options ? `<optgroup label="${escapeHtml(band.label)}">${options}</optgroup>` : '';
    }).join('');

    const requested = new URLSearchParams(window.location.search).get('review');
    let currentBatch = reviews.some((entry) => entry.dossier.batch === requested) ? requested : 'B32';
    if (!reviews.some((entry) => entry.dossier.batch === currentBatch)) currentBatch = reviews[0].dossier.batch;
    let currentMode = 'overlay';

    function renderView(batch) {
      const entry = reviews.find((item) => item.dossier.batch === batch);
      if (!entry) return;
      currentBatch = entry.dossier.batch;
      batchSelect.value = currentBatch;
      const available = (mode) => Boolean(entry.view[mode]);
      if (!available(currentMode)) currentMode = available('overlay') ? 'overlay' : (available('clean') ? 'clean' : 'reference');
      modeButtons.forEach((button) => {
        const mode = button.dataset.mode;
        button.disabled = !available(mode);
        button.classList.toggle('active', mode === currentMode);
      });
      image.src = entry.view[currentMode];
      image.alt = `${entry.dossier.batch} ${entry.view.label} ${currentMode}`;
      caption.innerHTML = `<strong>${escapeHtml(entry.dossier.batch)}</strong> · ${escapeHtml(entry.dossier.review_title || entry.dossier.family)} · ${escapeHtml(entry.view.label)}`;
      original.href = entry.dossier.review_page;
    }

    batchSelect.addEventListener('change', () => renderView(batchSelect.value));
    modeButtons.forEach((button) => {
      button.addEventListener('click', () => {
        if (button.disabled) return;
        currentMode = button.dataset.mode;
        renderView(currentBatch);
      });
    });
    function step(delta) {
      const index = Math.max(0, reviews.findIndex((entry) => entry.dossier.batch === currentBatch));
      renderView(reviews[(index + delta + reviews.length) % reviews.length].dossier.batch);
    }
    if (prev) prev.addEventListener('click', () => step(-1));
    if (next) next.addEventListener('click', () => step(1));

    renderView(currentBatch);
  }

  async function loadProcessCatalog() {
    const select = document.getElementById('dossier-select');
    const content = document.getElementById('dossier-content');
    if (!select || !content) return;
    try {
      const response = await fetch('../release/process_catalog.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const catalog = await response.json();
      const dossiers = catalog.dossiers || [];
      setupReviewGallery(dossiers);
      select.innerHTML = dossiers.map((d) => `<option value="${escapeHtml(d.batch)}">${d.featured ? '★ ' : ''}${escapeHtml(d.batch)} · ${escapeHtml(d.family)}</option>`).join('');
      const requested = new URLSearchParams(window.location.search).get('batch');
      const initial = dossiers.find((d) => d.batch === requested) || dossiers.find((d) => d.batch === 'B32') || dossiers[0];
      if (!initial) throw new Error('empty catalog');
      select.value = initial.batch;
      renderDossier(initial);
      select.addEventListener('change', () => renderDossier(dossiers.find((d) => d.batch === select.value)));
    } catch (error) {
      content.innerHTML = `<p class="loading">Process catalog unavailable: ${escapeHtml(error.message)}</p>`;
    }
  }

  loadMetrics();
  loadProcessCatalog();
})();
