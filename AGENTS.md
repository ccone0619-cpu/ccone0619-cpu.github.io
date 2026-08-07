# Repository Guidelines

## Project Structure & Module Organization

This is a static, multi-page portfolio site for HR/recruiter review. The three entry pages are `index.html` (summary and contact), `resume.html` (experience and skills), and `works.html` (video and project archive). Shared behavior lives in `app.js`; editable portfolio copy and project metadata live in `content.js`; the visual system is in `styles.css`. Media is grouped under `assets/images/` and `assets/videos/`, and the downloadable resume is `assets/zhao-zhouyu-resume.pdf`.

## Build, Test, and Development Commands

There is no framework build step. Run a local server from the repository root:

```bash
python3 -m http.server 4173
```

Open `http://127.0.0.1:4173/index.html`. Check JavaScript syntax with `node --check app.js` and `node --check content.js`. Before publishing, test the homepage and works page at 375px and desktop widths, including the project dialog and native video controls.

## Coding Style & Naming Conventions

Use two-space indentation for HTML, CSS, and JavaScript. Keep content changes in `content.js` rather than hardcoding copy into templates. Use kebab-case for CSS classes and project IDs (`fang-pv-edit`), camelCase for JavaScript functions, and semantic HTML with descriptive `data-*` hooks. Use Lucide icons for interface controls and preserve visible focus states.

## Testing Guidelines

This repository has no automated test suite. Manual smoke testing is required after UI changes: verify no horizontal overflow, keyboard activation of project cards, Escape/backdrop closing of dialogs, contact copy buttons, mobile navigation, and video loading only after opening a project.

## Commit & Pull Request Guidelines

Use short imperative commits that describe one change, such as `Redesign recruiter portfolio homepage` or `Add video portfolio work`. Pull requests should explain the user-facing change, list pages/assets touched, include desktop and mobile screenshots for visual work, and mention any external media URLs or deployment checks.

## Editing Content Safely

To update the site later, edit `window.PORTFOLIO_CONTENT` in `content.js`: update `identity`, `hero`, `resume`, `strengths`, or add an object to `personalWorks`. Keep video files in COS or `assets/videos/`, add a poster under `assets/images/`, and include a descriptive `imageAlt`, `summary`, `detail`, `role`, and `tags` for each work.
