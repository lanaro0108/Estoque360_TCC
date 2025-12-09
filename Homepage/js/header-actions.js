const bindHeaderActions = () => {
  const adjustNavLinks = () => {
    const links = document.querySelectorAll('.nav-links a[data-nav-target]');
    links.forEach((link) => {
      const target = link.getAttribute('data-nav-target');
      if (!target) return;
      if (target === '#top') {
        link.setAttribute('href', 'index.html#top');
        return;
      }
      const targetExists = document.querySelector(target);
      if (targetExists) {
        link.setAttribute('href', target);
      } else {
        link.setAttribute('href', `index.html${target}`);
      }
    });
  };

  const openStreamlit = () => {
    window.open('https://estoque360.streamlit.app', '_blank');
  };

  const aboutBtn = document.getElementById('about-button');
  if (aboutBtn && !aboutBtn.dataset.streamlitBound) {
    aboutBtn.addEventListener('click', openStreamlit);
    aboutBtn.dataset.streamlitBound = 'true';
  }

  const fishingBtn = document.getElementById('fishing-button');
  if (fishingBtn && !fishingBtn.dataset.streamlitBound) {
    fishingBtn.addEventListener('click', openStreamlit);
    fishingBtn.dataset.streamlitBound = 'true';
  }

  adjustNavLinks();
};

document.addEventListener('DOMContentLoaded', bindHeaderActions);
document.addEventListener('partials:loaded', bindHeaderActions);
