document.addEventListener("DOMContentLoaded", () => {
  const progress = document.getElementById("scrollProgress");
  const updateProgress = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.width = (max > 0 ? window.scrollY / max * 100 : 0) + "%";
  };
  window.addEventListener("scroll", updateProgress, { passive: true });
  updateProgress();

  const toggle = document.getElementById("menuToggle");
  const nav = document.getElementById("nav");
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
  });
  nav.querySelectorAll("a").forEach(link => link.addEventListener("click", () => {
    nav.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  }));

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible", "in-view");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal, .skill-card").forEach(el => observer.observe(el));

  const words = ["ideas.", "experiences.", "solutions.", "the future."];
  const word = document.getElementById("rotatingWord");
  let index = 0;
  if (word && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    setInterval(() => {
      word.classList.add("word-out");
      setTimeout(() => {
        index = (index + 1) % words.length;
        word.textContent = words[index];
        word.classList.remove("word-out");
      }, 220);
    }, 2200);
  }

  document.querySelectorAll(".toast").forEach(toast => {
    setTimeout(() => {
      toast.style.transition = "opacity .4s, transform .4s";
      toast.style.opacity = "0";
      toast.style.transform = "translateY(10px)";
      setTimeout(() => toast.remove(), 450);
    }, 4500);
  });
});
