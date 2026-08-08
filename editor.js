(function () {
  const source = window.PORTFOLIO_CONTENT;
  const storageKey = "zhao-zhouyu-portfolio-draft-v1";
  const form = document.querySelector("[data-editor-form]");
  const status = document.querySelector("[data-status]");
  const toast = document.querySelector("[data-editor-toast]");
  if (!source || !form) return;

  const clone = (value) => JSON.parse(JSON.stringify(value));
  const original = clone(source);
  let data = loadDraft() || clone(source);
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

  const setByPath = (object, path, value) => {
    const keys = path.split(".");
    const last = keys.pop();
    const target = keys.reduce((current, key) => current[key], object);
    target[last] = value;
  };

  const getByPath = (object, path) => path.split(".").reduce((current, key) => current && current[key], object);
  const notify = (message) => {
    if (status) status.textContent = message;
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("is-visible");
    window.clearTimeout(notify.timer);
    notify.timer = window.setTimeout(() => toast.classList.remove("is-visible"), 2200);
  };

  function loadDraft() {
    try {
      const saved = localStorage.getItem(storageKey);
      return saved ? JSON.parse(saved) : null;
    } catch (_) {
      return null;
    }
  }

  const input = (name, value, rows, placeholder) => `
    <label class="field"><span>${placeholder}</span>${rows > 1 ? `<textarea data-path="${name}" rows="${rows}">${escapeHtml(value || "")}</textarea>` : `<input data-path="${name}" type="text" value="${escapeHtml(value || "")}" />`}</label>
  `;

  const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (character) => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[character]));

  const renderRepeat = (key) => {
    const container = $(`[data-repeat="${key}"]`);
    if (!container) return;
    const items = key === "works" ? data.personalWorks : key === "stats" ? data.stats : key === "facts" ? data.resume.facts : key === "experience" ? data.resume.experience : data.strengths;
    const fields = {
      stats: (item, index) => `<div class="editor-repeat-item"><div class="repeat-heading"><h3>亮点 ${String(index + 1).padStart(2, "0")}</h3></div><div class="editor-fields editor-fields-2">${input(`stats.${index}.value`, item.value, 1, "数字或短标签")}${input(`stats.${index}.label`, item.label, 1, "说明")}</div></div>`,
      facts: (item, index) => `<div class="editor-repeat-item"><div class="repeat-heading"><h3>简历事实 ${String(index + 1).padStart(2, "0")}</h3></div><div class="editor-fields editor-fields-2">${input(`resume.facts.${index}.label`, item.label, 1, "字段名")}${input(`resume.facts.${index}.value`, item.value, 2, "字段内容")}</div></div>`,
      experience: (item, index) => `<div class="editor-repeat-item"><div class="repeat-heading"><h3>经历 ${String(index + 1).padStart(2, "0")}</h3></div><div class="editor-fields editor-fields-2">${input(`resume.experience.${index}.meta`, item.meta, 1, "类型标签")}${input(`resume.experience.${index}.role`, item.role, 1, "职责标签")}</div>${input(`resume.experience.${index}.title`, item.title, 1, "经历标题")}${input(`resume.experience.${index}.body`, item.body, 4, "经历说明")}</div>`,
      strengths: (item, index) => `<div class="editor-repeat-item"><div class="repeat-heading"><h3>优势 ${String(index + 1).padStart(2, "0")}</h3></div><div class="editor-fields editor-fields-2">${input(`strengths.${index}.number`, item.number, 1, "编号")}${input(`strengths.${index}.title`, item.title, 1, "优势标题")}</div>${input(`strengths.${index}.body`, item.body, 4, "优势说明")}</div>`,
      works: (item, index) => `<div class="editor-repeat-item"><div class="repeat-heading"><h3>${escapeHtml(item.title || `作品 ${index + 1}`)}</h3><span>${escapeHtml(item.id || "")}</span></div><div class="editor-fields editor-fields-2">${input(`personalWorks.${index}.title`, item.title, 1, "作品标题")}${input(`personalWorks.${index}.category`, item.category, 1, "作品分类")}${input(`personalWorks.${index}.year`, item.year, 1, "时长 / 年份")}${input(`personalWorks.${index}.role`, item.role, 1, "我的职责")}</div>${input(`personalWorks.${index}.summary`, item.summary, 3, "卡片简介")}${input(`personalWorks.${index}.detail`, item.detail, 5, "弹窗详情")}${input(`personalWorks.${index}.tags`, (item.tags || []).join(", "), 2, "标签（用逗号分隔）")}</div>`
    };
    container.innerHTML = `<div class="repeat-heading"><h3>${({stats:"首页亮点",facts:"简历信息",experience:"项目经历",strengths:"优势条目",works:"作品列表"}[key])}</h3><span>${items.length} 项</span></div>${items.map(fields[key]).join("")}`;
  };

  const render = () => {
    $$('[data-path], [name]:not([data-array-field])', form).forEach((field) => {
      const path = field.dataset.path || field.name;
      const value = getByPath(data, path);
      field.value = Array.isArray(value) ? value.join(", ") : value || "";
    });
    ["stats", "facts", "experience", "strengths", "works"].forEach(renderRepeat);
    $$('[data-array-field="comma"]', form).forEach((field) => { field.value = data.resume.skills.join(", "); });
  };

  const collect = () => {
    $$('[data-path], [name]:not([data-array-field])', form).forEach((field) => {
      const path = field.dataset.path || field.name;
      let value = field.value;
      if (path.endsWith(".tags")) value = value.split(",").map((item) => item.trim()).filter(Boolean);
      setByPath(data, path, value);
    });
    const skills = $('[data-array-field="comma"]');
    if (skills) data.resume.skills = skills.value.split(",").map((item) => item.trim()).filter(Boolean);
  };

  const save = () => {
    collect();
    localStorage.setItem(storageKey, JSON.stringify(data));
    notify("草稿已保存到本机");
  };

  const download = async () => {
    collect();
    const text = `// Edit this file to update the portfolio without touching the layout.\nwindow.PORTFOLIO_CONTENT = ${JSON.stringify(data, null, 2)};\n`;
    const blob = new Blob([text], { type: "text/javascript;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "content.js";
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    localStorage.setItem(storageKey, JSON.stringify(data));
    notify("content.js 已下载，请替换项目里的同名文件");
  };

  $$('[data-save]').forEach((button) => button.addEventListener("click", save));
  $$('[data-download]').forEach((button) => button.addEventListener("click", download));
  const resetButton = $('[data-reset]');
  resetButton.addEventListener("click", () => {
    if (!resetButton.dataset.confirming) {
      resetButton.dataset.confirming = "true";
      resetButton.textContent = "再点一次确认恢复";
      window.clearTimeout(resetButton.confirmTimer);
      resetButton.confirmTimer = window.setTimeout(() => {
        delete resetButton.dataset.confirming;
        resetButton.textContent = "恢复网站原始内容";
      }, 4000);
      return;
    }
    data = clone(original);
    localStorage.removeItem(storageKey);
    delete resetButton.dataset.confirming;
    resetButton.textContent = "恢复网站原始内容";
    render();
    notify("已恢复原始内容");
  });
  form.addEventListener("input", () => { if (status) status.textContent = "有未保存的修改"; });
  form.addEventListener("submit", (event) => event.preventDefault());

  const menuToggle = $(".menu-toggle");
  const mobileNav = $("#editor-mobile-nav");
  if (menuToggle && mobileNav) {
    menuToggle.addEventListener("click", () => {
      const open = menuToggle.getAttribute("aria-expanded") === "true";
      menuToggle.setAttribute("aria-expanded", String(!open));
      mobileNav.hidden = open;
      menuToggle.innerHTML = `<i data-lucide="${open ? "menu" : "x"}" aria-hidden="true"></i>`;
      if (window.lucide) window.lucide.createIcons();
    });
  }
  if (window.lucide) window.lucide.createIcons();
  render();
})();
