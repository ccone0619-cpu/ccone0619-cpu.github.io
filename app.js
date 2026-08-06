(function () {
  const data = window.PORTFOLIO_CONTENT;
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

  const setText = (selector, value) => {
    const element = $(selector);
    if (element) element.textContent = value;
  };

  const setAttribute = (selector, name, value) => {
    const element = $(selector);
    if (element && value != null) element.setAttribute(name, value);
  };

  const renderIdentity = () => {
    setText("[data-brand-mark]", data.identity.mark);
    setText("[data-brand-name]", data.identity.name.toUpperCase());
    setText("[data-footer-name]", data.identity.name.toUpperCase());
    setText("[data-availability]", data.identity.availability);
    setText("[data-location]", data.identity.location);
    setText("[data-year]", new Date().getFullYear());
    document.title = `${data.identity.name} — Personal Portfolio`;
    const emailLink = $("[data-email-link]");
    emailLink.textContent = data.identity.email;
    emailLink.href = `mailto:${data.identity.email}`;
    const cvLink = $("[data-cv-link]");
    cvLink.href = data.identity.cvUrl;
    const socials = $("[data-socials]");
    socials.innerHTML = data.identity.socials.map((item) => `<a href="${item.url}" target="_blank" rel="noreferrer">${item.label}</a>`).join("");
  };

  const renderHero = () => {
    setText("[data-hero-name]", data.identity.name);
    setText("[data-hero-role]", data.identity.role);
    setText("[data-hero-title]", data.hero.title);
    setText("[data-hero-description]", data.hero.description);
    setText("[data-hero-note]", data.hero.note);
    setAttribute("[data-hero-image]", "src", data.hero.image);
    setAttribute("[data-hero-image]", "alt", data.hero.imageAlt);
    setText("[data-hero-count]", data.hero.imageCount);
    setText("[data-hero-caption]", data.hero.imageCaption);
  };

  const renderAbout = () => {
    setText("[data-about-eyebrow]", data.about.eyebrow);
    setText("[data-about-title]", data.about.title);
    setText("[data-about-body]", data.about.body);
    setText("[data-about-quote]", data.about.quote);
    $("[data-stats]").innerHTML = data.stats.map((stat) => `
      <div class="stat">
        <span class="stat-value">${stat.value}</span>
        <span class="stat-label">${stat.label}</span>
      </div>
    `).join("");
  };

  const renderStrengths = () => {
    $("[data-strengths]").innerHTML = data.strengths.map((item) => `
      <article class="strength reveal">
        <span class="strength-number">${item.number}</span>
        <h3>${item.title}</h3>
        <p>${item.body}</p>
      </article>
    `).join("");
  };

  const projectMedia = (project, inDialog = false) => {
    if (project.type === "video") {
      return inDialog
        ? `<video controls playsinline preload="metadata" poster="${project.image}"><source src="${project.video}" type="video/mp4" />你的浏览器不支持视频播放。</video>`
        : `<video muted loop playsinline preload="metadata" poster="${project.image}"><source src="${project.video}" type="video/mp4" /></video>`;
    }
    return `<img src="${project.image}" alt="${project.title} 项目视觉" loading="lazy" />`;
  };

  const renderFilters = () => {
    const filters = ["全部", ...new Set(data.projects.map((project) => project.category))];
    $("[data-filters]").innerHTML = filters.map((filter, index) => `
      <button class="filter-button${index === 0 ? " is-active" : ""}" type="button" data-filter="${filter}">${filter}</button>
    `).join("");
  };

  const renderProjects = () => {
    $("[data-projects]").innerHTML = data.projects.map((project, index) => `
      <article class="project-card reveal" data-project-id="${project.id}" data-category="${project.category}" tabindex="0" role="button" aria-label="查看 ${project.title} 项目详情" data-reveal-delay="${index * 80}">
        <div class="project-visual">
          ${projectMedia(project)}
          ${project.type === "video" ? '<span class="media-badge"><i data-lucide="play" aria-hidden="true"></i> VIDEO</span>' : '<span class="media-badge"><i data-lucide="image" aria-hidden="true"></i> IMAGE</span>'}
        </div>
        <div class="project-info">
          <div class="project-meta"><span>${project.category}</span><span>${project.year}</span></div>
          <h3>${project.title}</h3>
          <p>${project.summary}</p>
          <span class="project-arrow" aria-hidden="true"><i data-lucide="arrow-up-right"></i></span>
        </div>
      </article>
    `).join("");
  };

  const openProject = (project) => {
    const dialog = $("#project-dialog");
    $("[data-dialog-media]").innerHTML = projectMedia(project, true);
    setText("[data-dialog-category]", project.category);
    setText("[data-dialog-year]", project.year);
    setText("[data-dialog-title]", project.title);
    setText("[data-dialog-detail]", project.detail);
    setText("[data-dialog-role]", project.role);
    $("[data-dialog-tags]").innerHTML = project.tags.map((tag) => `<span class="tag">${tag}</span>`).join("");
    if (typeof dialog.showModal === "function") dialog.showModal();
    else dialog.setAttribute("open", "");
    lucide.createIcons();
  };

  const bindInteractions = () => {
    $("[data-filters]").addEventListener("click", (event) => {
      const button = event.target.closest("[data-filter]");
      if (!button) return;
      $$(".filter-button").forEach((item) => item.classList.toggle("is-active", item === button));
      const filter = button.dataset.filter;
      $$(".project-card").forEach((card) => card.classList.toggle("is-hidden", filter !== "全部" && card.dataset.category !== filter));
    });

    $("[data-projects]").addEventListener("click", (event) => {
      const card = event.target.closest("[data-project-id]");
      if (card) openProject(data.projects.find((project) => project.id === card.dataset.projectId));
    });
    $("[data-projects]").addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") return;
      const card = event.target.closest("[data-project-id]");
      if (card) { event.preventDefault(); openProject(data.projects.find((project) => project.id === card.dataset.projectId)); }
    });

    const dialog = $("#project-dialog");
    const closeProjectDialog = () => dialog.close();
    $("[data-dialog-close]").addEventListener("click", closeProjectDialog);
    dialog.addEventListener("click", (event) => { if (event.target === dialog) closeProjectDialog(); });
    dialog.addEventListener("close", () => {
      const media = $("[data-dialog-media]");
      const video = $("video", media);
      if (video) {
        video.pause();
        video.currentTime = 0;
      }
      media.innerHTML = "";
    });

    $("[data-copy-email]").addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(data.identity.email);
        showToast("邮箱地址已复制");
      } catch (_) {
        showToast(data.identity.email);
      }
    });

    const menuToggle = $(".menu-toggle");
    const mobileNav = $("#mobile-nav");
    menuToggle.addEventListener("click", () => {
      const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
      menuToggle.setAttribute("aria-expanded", String(!isOpen));
      menuToggle.setAttribute("aria-label", isOpen ? "打开菜单" : "关闭菜单");
      mobileNav.hidden = isOpen;
      menuToggle.innerHTML = `<i data-lucide="${isOpen ? "menu" : "x"}" aria-hidden="true"></i>`;
      lucide.createIcons();
    });
    $$(".mobile-nav a").forEach((link) => link.addEventListener("click", () => {
      mobileNav.hidden = true;
      menuToggle.setAttribute("aria-expanded", "false");
      menuToggle.innerHTML = '<i data-lucide="menu" aria-hidden="true"></i>';
      lucide.createIcons();
    }));
  };

  const showToast = (message) => {
    const toast = $("[data-toast]");
    toast.textContent = message;
    toast.classList.add("is-visible");
    window.clearTimeout(showToast.timer);
    showToast.timer = window.setTimeout(() => toast.classList.remove("is-visible"), 2200);
  };

  const initReveal = () => {
    const items = $$(".reveal");
    if (!("IntersectionObserver" in window)) { items.forEach((item) => item.classList.add("is-visible")); return; }
    const observer = new IntersectionObserver((entries, instance) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const delay = Number(entry.target.dataset.revealDelay || 0);
        window.setTimeout(() => entry.target.classList.add("is-visible"), delay);
        instance.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach((item) => observer.observe(item));
  };

  const init = () => {
    renderIdentity();
    renderHero();
    renderAbout();
    renderStrengths();
    renderFilters();
    renderProjects();
    bindInteractions();
    lucide.createIcons();
    initReveal();
  };

  init();
})();
