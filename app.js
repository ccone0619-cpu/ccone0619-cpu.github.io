(function () {
  const data = window.PORTFOLIO_CONTENT;
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

  const setText = (selector, value) => {
    const element = $(selector);
    if (element) element.textContent = value;
  };

  const renderIcons = () => {
    if (window.lucide && typeof window.lucide.createIcons === "function") window.lucide.createIcons();
  };

  const renderIdentity = () => {
    setText("[data-brand-mark]", data.identity.mark);
    setText("[data-brand-name]", data.identity.name.toUpperCase());
    setText("[data-footer-name]", data.identity.name.toUpperCase());
    setText("[data-location]", data.identity.location);
    const location = $("[data-location]");
    if (location) location.hidden = !data.identity.location;
    setText("[data-year]", new Date().getFullYear());
    const phoneLink = $("[data-phone-link]");
    if (phoneLink) {
      phoneLink.textContent = data.identity.phone;
      phoneLink.href = `tel:${data.identity.phone}`;
    }
    setText("[data-wechat]", data.identity.wechat);
    $$('[data-email-link]').forEach((emailLink) => {
      const hasEmail = Boolean(data.identity.email);
      emailLink.hidden = !hasEmail;
      if (hasEmail) {
        emailLink.textContent = data.identity.email;
        emailLink.href = `mailto:${data.identity.email}`;
      }
    });
    const hasCv = Boolean(data.identity.cvUrl && data.identity.cvUrl !== "#");
    $$('[data-cv-link]').forEach((cvLink) => {
      cvLink.hidden = !hasCv;
      if (hasCv) cvLink.href = data.identity.cvUrl;
    });
    $$('[data-cv-download]').forEach((cvLink) => {
      cvLink.hidden = !hasCv;
      if (hasCv) cvLink.href = data.identity.cvUrl;
    });
    $$('[data-open-resume-viewer]').forEach((button) => { button.hidden = !hasCv; });
    const socials = $("[data-socials]");
    if (socials) socials.innerHTML = data.identity.socials.map((item) => `<a href="${item.url}" target="_blank" rel="noreferrer">${item.label}</a>`).join("");
  };

  const renderHero = () => {
    setText("[data-hero-name]", data.identity.name);
    setText("[data-hero-role]", data.identity.role);
    setText("[data-hero-title]", data.hero.title);
    setText("[data-hero-description]", data.hero.description);
    setText("[data-hero-note]", data.hero.note);
    if (data.hero.proof) {
      setText("[data-hero-proof-eyebrow]", data.hero.proof.eyebrow);
      setText("[data-hero-proof-value]", data.hero.proof.value);
      setText("[data-hero-proof-label]", data.hero.proof.label);
      setText("[data-hero-proof-note]", data.hero.proof.note);
    }
  };

  const renderAbout = () => {
    setText("[data-about-eyebrow]", data.about.eyebrow);
    setText("[data-about-title]", data.about.title);
    setText("[data-about-body]", data.about.body);
    setText("[data-about-quote]", data.about.quote);
    const stats = $("[data-stats]");
    if (!stats) return;
    stats.innerHTML = data.stats.map((stat) => `
      <div class="stat">
        <span class="stat-value">${stat.value}</span>
        <span class="stat-label">${stat.label}</span>
      </div>
    `).join("");
  };

  const renderStrengths = () => {
    const strengths = $("[data-strengths]");
    if (!strengths) return;
    strengths.innerHTML = data.strengths.map((item) => `
      <article class="strength reveal">
        <span class="strength-number">${item.number}</span>
        <h3>${item.title}</h3>
        <p>${item.body}</p>
      </article>
    `).join("");
  };

  const renderResume = () => {
    setText("[data-resume-eyebrow]", data.resume.eyebrow);
    setText("[data-resume-title]", data.resume.title);
    setText("[data-resume-intro]", data.resume.intro);
    setText("[data-resume-file-note]", data.resume.fileNote);
    const facts = $("[data-resume-facts]");
    const skills = $("[data-resume-skills]");
    const experience = $("[data-resume-experience]");
    if (!facts || !skills || !experience) return;
    facts.innerHTML = data.resume.facts.map((item) => `
      <div class="resume-fact">
        <dt>${item.label}</dt>
        <dd>${item.value}</dd>
      </div>
    `).join("");
    skills.innerHTML = data.resume.skills.map((skill) => `<span class="resume-skill">${skill}</span>`).join("");
    experience.innerHTML = data.resume.experience.map((item, index) => `
      <article class="resume-item reveal" data-reveal-delay="${index * 70}">
        <span class="resume-item-meta">${item.meta}</span>
        <div>
          <h3>${item.title}</h3>
          <p class="resume-item-role">${item.role}</p>
          <p>${item.body}</p>
        </div>
      </article>
    `).join("");
  };

  const projectMedia = (project, inDialog = false) => {
    if (project.type === "video") {
      return inDialog
        ? `<video controls playsinline preload="metadata" poster="${project.image}" aria-label="播放 ${project.title}"><source src="${project.video}" type="video/mp4" />你的浏览器不支持视频播放。</video>`
        : `<img class="project-media-image" src="${project.image}" alt="${project.imageAlt || `${project.title} 视频封面`}" loading="lazy" decoding="async" />`;
    }
    const imageClass = project.layout ? ` project-media-${project.layout}` : "";
    return `<img class="project-media-image${imageClass}" src="${project.image}" alt="${project.imageAlt || `${project.title} 项目视觉`}" loading="lazy" decoding="async" />`;
  };

  const projectCard = (project, index) => `
    <article class="project-card${project.layout ? ` project-card-${project.layout}` : ""} reveal" data-project-id="${project.id}" data-category="${project.category}" tabindex="0" role="button" aria-label="查看 ${project.title} 项目详情" data-reveal-delay="${index * 80}">
      <div class="project-visual">
        ${projectMedia(project)}
        ${project.type === "video" ? '<span class="media-badge"><i data-lucide="play" aria-hidden="true"></i> 播放</span>' : `<span class="media-badge"><i data-lucide="sparkles" aria-hidden="true"></i> ${project.badge || "项目"}</span>`}
      </div>
      <div class="project-info">
        <div class="project-meta"><span>${project.category}</span><span>${project.year}</span></div>
        <h3>${project.title}</h3>
        <p>${project.summary}</p>
        <span class="project-arrow" aria-hidden="true"><i data-lucide="arrow-up-right"></i></span>
      </div>
    </article>
  `;

  const editingCard = (project, index) => `
    <article class="editing-card reveal" data-project-id="${project.id}" tabindex="0" role="button" aria-label="播放 ${project.title}" data-reveal-delay="${index * 80}">
      <div class="editing-card-visual">
        <img src="${project.image}" alt="${project.imageAlt || `${project.title} 视频封面`}" loading="lazy" decoding="async" />
      </div>
      <div class="editing-card-info">
        <div class="editing-card-meta"><span>作品 0${index + 1}</span><span>${project.year}</span></div>
        <h3>${project.title}</h3>
        <p>${project.summary}</p>
      </div>
    </article>
  `;

  const renderEditingWorks = () => {
    const container = $("[data-editing-works]");
    if (!container) return;
    const editingWorks = data.personalWorks.filter((project) => project.type === "video").slice(0, 3);
    container.innerHTML = editingWorks.map(editingCard).join("");
  };

  const renderPersonalWorks = () => {
    const container = $("[data-personal-works]");
    if (!container) return;
    if (!data.personalWorks.length) {
      container.innerHTML = `
        <div class="personal-work-empty reveal">
          <span class="personal-work-empty-icon" aria-hidden="true"><i data-lucide="folder-open"></i></span>
          <div>
            <span class="personal-work-empty-label">待上传</span>
            <h3>作品整理中</h3>
            <p>完整成片、剪辑片段和视觉资产案例将陆续收录。</p>
          </div>
        </div>
      `;
      return;
    }
    container.innerHTML = data.personalWorks.map(projectCard).join("");
  };

  const openProject = (project) => {
    const dialog = $("#project-dialog");
    if (!dialog || !project) return;
    const media = $("[data-dialog-media]");
    media.innerHTML = projectMedia(project, true);
    const video = $("video", media);
    if (video) {
      video.addEventListener("error", () => {
        media.innerHTML = `
          <div class="media-error" role="status">
            <i data-lucide="circle-alert" aria-hidden="true"></i>
            <strong>视频暂时无法加载</strong>
            <p>请检查网络后重试。作品说明和制作过程仍可继续查看。</p>
          </div>
        `;
        renderIcons();
      }, { once: true });
    }
    setText("[data-dialog-category]", project.category);
    setText("[data-dialog-year]", project.year);
    setText("[data-dialog-title]", project.title);
    setText("[data-dialog-detail]", project.detail);
    setText("[data-dialog-role]", project.role);
    $("[data-dialog-tags]").innerHTML = project.tags.map((tag) => `<span class="tag">${tag}</span>`).join("");
    const process = $("[data-dialog-process]");
    const gallery = $("[data-dialog-gallery]");
    const hasGallery = Boolean(project.gallery && project.gallery.length);
    process.hidden = !hasGallery;
    gallery.innerHTML = hasGallery ? project.gallery.map((item) => `
      <figure class="dialog-gallery-item">
        <button class="dialog-gallery-trigger" type="button" data-gallery-image="${item.image}" data-gallery-alt="${item.alt}" data-gallery-label="${item.label}" aria-label="放大查看 ${item.label}">
          <img src="${item.image}" alt="${item.alt}" loading="lazy" />
          <span class="dialog-gallery-zoom" aria-hidden="true"><i data-lucide="maximize-2"></i></span>
        </button>
        <figcaption>${item.label}</figcaption>
      </figure>
    `).join("") : "";
    if (typeof dialog.showModal === "function") dialog.showModal();
    else {
      dialog.classList.add("is-fallback");
      dialog.setAttribute("open", "");
      document.body.classList.add("dialog-open");
    }
    renderIcons();
  };

  const bindInteractions = () => {
    const allProjects = data.personalWorks;
    $$('[data-personal-works], [data-editing-works]').forEach((container) => {
      container.addEventListener("click", (event) => {
        const card = event.target.closest("[data-project-id]");
        if (card) openProject(allProjects.find((project) => project.id === card.dataset.projectId));
      });
      container.addEventListener("keydown", (event) => {
        if (event.key !== "Enter" && event.key !== " ") return;
        const card = event.target.closest("[data-project-id]");
        if (card) {
          event.preventDefault();
          openProject(allProjects.find((project) => project.id === card.dataset.projectId));
        }
      });
    });

    const dialog = $("#project-dialog");
    if (dialog) {
      const clearProjectDialog = () => {
        const media = $("[data-dialog-media]");
        const video = $("video", media);
        if (video) {
          video.pause();
          video.currentTime = 0;
        }
        media.innerHTML = "";
      };
      const closeProjectDialog = () => {
        if (dialog.classList.contains("is-fallback")) {
          dialog.removeAttribute("open");
          dialog.classList.remove("is-fallback");
          document.body.classList.remove("dialog-open");
          clearProjectDialog();
          return;
        }
        dialog.close();
      };
      $("[data-dialog-close]").addEventListener("click", closeProjectDialog);
      dialog.addEventListener("click", (event) => { if (event.target === dialog) closeProjectDialog(); });
      dialog.addEventListener("close", clearProjectDialog);
      document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && dialog.classList.contains("is-fallback")) closeProjectDialog();
      });
    }

    const lightbox = $("#image-lightbox");
    if (lightbox) {
      const lightboxImage = $("[data-lightbox-image]", lightbox);
      const lightboxCaption = $("[data-lightbox-caption]", lightbox);
      const closeLightbox = () => {
        if (lightbox.classList.contains("is-fallback")) {
          lightbox.removeAttribute("open");
          lightbox.classList.remove("is-fallback");
          document.body.classList.remove("image-lightbox-open");
        } else if (lightbox.open) {
          lightbox.close();
        }
      };
      const clearLightbox = () => {
        lightboxImage.removeAttribute("src");
        lightboxImage.alt = "";
        lightboxCaption.textContent = "";
      };
      document.addEventListener("click", (event) => {
        const trigger = event.target.closest("[data-gallery-image]");
        if (!trigger) return;
        lightboxImage.src = trigger.dataset.galleryImage;
        lightboxImage.alt = trigger.dataset.galleryAlt;
        lightboxCaption.textContent = trigger.dataset.galleryLabel;
        if (typeof lightbox.showModal === "function") lightbox.showModal();
        else {
          lightbox.classList.add("is-fallback");
          lightbox.setAttribute("open", "");
          document.body.classList.add("image-lightbox-open");
        }
      });
      $("[data-lightbox-close]", lightbox).addEventListener("click", closeLightbox);
      lightbox.addEventListener("click", (event) => { if (event.target === lightbox) closeLightbox(); });
      lightbox.addEventListener("close", clearLightbox);
      document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && lightbox.classList.contains("is-fallback")) {
          closeLightbox();
          clearLightbox();
        }
      });
    }

    const resumeViewer = $("#resume-viewer");
    if (resumeViewer) {
      const resumeFrame = $("[data-resume-frame]", resumeViewer);
      const closeResumeViewer = () => {
        if (resumeViewer.classList.contains("is-fallback")) {
          resumeViewer.removeAttribute("open");
          resumeViewer.classList.remove("is-fallback");
          document.body.classList.remove("resume-viewer-open");
        } else if (resumeViewer.open) {
          resumeViewer.close();
        }
      };
      const openResumeViewer = () => {
        if (!data.identity.cvUrl) return;
        if (!resumeFrame.getAttribute("src")) resumeFrame.src = data.identity.cvUrl;
        if (typeof resumeViewer.showModal === "function") resumeViewer.showModal();
        else {
          resumeViewer.classList.add("is-fallback");
          resumeViewer.setAttribute("open", "");
          document.body.classList.add("resume-viewer-open");
        }
      };
      $$('[data-open-resume-viewer]').forEach((button) => button.addEventListener("click", openResumeViewer));
      $("[data-resume-viewer-close]", resumeViewer).addEventListener("click", closeResumeViewer);
      resumeViewer.addEventListener("click", (event) => { if (event.target === resumeViewer) closeResumeViewer(); });
      document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && resumeViewer.classList.contains("is-fallback")) closeResumeViewer();
      });
    }

    const copyToClipboard = async (value, message) => {
      try {
        await navigator.clipboard.writeText(value);
        showToast(message);
      } catch (_) {
        showToast(value);
      }
    };
    const copyPhone = $("[data-copy-phone]");
    const copyWechat = $("[data-copy-wechat]");
    const copyEmail = $("[data-copy-email]");
    if (copyPhone) copyPhone.addEventListener("click", () => copyToClipboard(data.identity.phone, "手机号已复制"));
    if (copyWechat) copyWechat.addEventListener("click", () => copyToClipboard(data.identity.wechat, "微信号已复制"));
    if (copyEmail) copyEmail.addEventListener("click", () => copyToClipboard(data.identity.email, "邮箱已复制"));

    const menuToggle = $(".menu-toggle");
    const mobileNav = $("#mobile-nav");
    if (menuToggle && mobileNav) {
      const closeMobileNav = () => {
        mobileNav.hidden = true;
        menuToggle.setAttribute("aria-expanded", "false");
        menuToggle.setAttribute("aria-label", "打开菜单");
        menuToggle.innerHTML = '<i data-lucide="menu" aria-hidden="true"></i>';
        renderIcons();
      };
      menuToggle.addEventListener("click", () => {
        const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
        menuToggle.setAttribute("aria-expanded", String(!isOpen));
        menuToggle.setAttribute("aria-label", isOpen ? "打开菜单" : "关闭菜单");
        mobileNav.hidden = isOpen;
        menuToggle.innerHTML = `<i data-lucide="${isOpen ? "menu" : "x"}" aria-hidden="true"></i>`;
        renderIcons();
      });
      $$(".mobile-nav a").forEach((link) => link.addEventListener("click", closeMobileNav));
      document.addEventListener("keydown", (event) => { if (event.key === "Escape" && !mobileNav.hidden) closeMobileNav(); });
      window.addEventListener("resize", () => { if (window.innerWidth > 760 && !mobileNav.hidden) closeMobileNav(); });
    }

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!reduceMotion && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
      $$(".project-card video").forEach((video) => {
        const card = video.closest(".project-card");
        card.addEventListener("pointerenter", () => video.play().catch(() => {}));
        card.addEventListener("pointerleave", () => {
          video.pause();
          video.currentTime = 0;
        });
      });
    }
  };

  const showToast = (message) => {
    const toast = $("[data-toast]");
    if (!toast) return;
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

  const initScrollEffects = () => {
    const header = $(".site-header");
    const progress = $("[data-scroll-progress]");
    if (!header || !progress) return;
    let frame = 0;
    const update = () => {
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
      const value = maxScroll > 0 ? Math.min(1, Math.max(0, window.scrollY / maxScroll)) : 0;
      progress.style.transform = `scaleX(${value})`;
      header.classList.toggle("is-scrolled", window.scrollY > 12);
      frame = 0;
    };
    const schedule = () => {
      if (!frame) frame = window.requestAnimationFrame(update);
    };
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    update();
  };

  const init = () => {
    renderIdentity();
    renderHero();
    renderAbout();
    renderResume();
    renderStrengths();
    renderEditingWorks();
    renderPersonalWorks();
    bindInteractions();
    document.documentElement.classList.add("js");
    renderIcons();
    initReveal();
    initScrollEffects();
  };

  init();
})();
