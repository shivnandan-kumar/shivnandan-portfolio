"use strict";

(() => {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const revealTargets = document.querySelectorAll(
    ".hero-copy, .hero-profile-card, .project-card, .about-introduction, " +
      ".education-card, .skill-group, .contact-form, .project-detail-header, " +
      ".project-detail-gallery, .project-detail-content, .project-detail-stack",
  );

  if (!revealTargets.length || !("IntersectionObserver" in window)) return;

  const observer = new IntersectionObserver(
    (entries, currentObserver) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        entry.target.classList.add("is-visible");
        currentObserver.unobserve(entry.target);
      });
    },
    {
      threshold: 0.12,
      rootMargin: "0px 0px -4% 0px",
    },
  );

  document.documentElement.classList.add("motion-ready");
  revealTargets.forEach((element) => {
    element.classList.add("reveal-on-scroll");
    observer.observe(element);
  });
})();
