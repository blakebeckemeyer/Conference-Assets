(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const previous = document.getElementById('previous');
  const next = document.getElementById('next');
  const notice = document.getElementById('notice');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const printMedia = window.matchMedia('print');
  let motion = [];
  let departingSlide = null;
  let initialized = false;
  let presenterWindow = null;
  const times = {
    opening: '00:00-00:08', m365: '00:08-00:23', cowork: '00:23-00:36',
    lifecycle: '00:36-01:01', reuse: '01:01-01:06', break: '01:06-01:11',
    studio: '01:11-01:35', foundry: '01:35-01:53', close: '01:53-02:00'
  };
  let current = 0;
  function stopMotion() {
    motion.forEach(animation => animation.cancel());
    motion = [];
    if (departingSlide) {
      departingSlide.classList.remove('departing');
      departingSlide = null;
    }
  }
  function transition(outgoing, incoming, direction) {
    if (reducedMotion.matches || printMedia.matches || !incoming.animate) return;
    const chapterChange = outgoing.dataset.segment !== incoming.dataset.segment;
    const desktop = window.matchMedia('(min-width: 761px)').matches;
    const options = { duration: chapterChange ? 480 : 340, easing: 'cubic-bezier(0.16, 1, 0.3, 1)' };
    if (desktop) {
      departingSlide = outgoing;
      outgoing.classList.add('departing');
      const exit = outgoing.animate([
        { opacity: 1, transform: 'translateX(0)' },
        { opacity: 0, transform: `translateX(${-direction * 24}px)` }
      ], { duration: 180, easing: 'ease-out' });
      exit.onfinish = () => {
        outgoing.classList.remove('departing');
        if (departingSlide === outgoing) departingSlide = null;
      };
      motion.push(exit);
    }
    // Chapter changes turn a new sheet; within a chapter the work moves forward.
    motion.push(incoming.animate(chapterChange ? [
      { opacity: 0.2, clipPath: direction > 0 ? 'inset(0 0 0 10%)' : 'inset(0 10% 0 0)' },
      { opacity: 1, clipPath: 'inset(0 0 0 0)' }
    ] : [
      { opacity: 0, transform: `translateX(${direction * (desktop ? 40 : 16)}px)` },
      { opacity: 1, transform: 'translateX(0)' }
    ], options));
    const artifact = incoming.querySelector('.commands, blockquote, .integration');
    if (artifact) {
      motion.push(artifact.animate([
        { transform: 'translateY(12px)', opacity: 0.45 },
        { transform: 'translateY(0)', opacity: 1 }
      ], { ...options, duration: 380, delay: 70 }));
    }
  }
  function updatePresenter() {
    if (!presenterWindow || presenterWindow.closed) return;
    const slide = slides[current];
    presenterWindow.postMessage({
      type: 'detroit-presenter-state',
      index: current,
      count: slides.length,
      title: slide.querySelector('h1, h2').innerText.replace(/\s+/g, ' ').trim(),
      nextTitle: slides[current + 1]?.querySelector('h1, h2').textContent ?? 'End of deck',
      time: times[slide.dataset.segment],
      notes: slide.querySelector('template.speaker-notes').innerHTML
    }, '*');
  }
  function show(index, updateHash = true) {
    const oldIndex = current;
    stopMotion();
    current = Math.max(0, Math.min(slides.length - 1, index));
    slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === current);
      slide.setAttribute('aria-hidden', String(i !== current));
      slide.inert = i !== current;
    });
    previous.disabled = current === 0;
    next.disabled = current === slides.length - 1;
    document.getElementById('position').textContent = `${current + 1} / ${slides.length}`;
    document.getElementById('chapter-time').textContent = times[slides[current].dataset.segment];
    document.title = `${slides[current].querySelector('h1, h2').innerText.replace(/\s+/g, ' ').trim()} | Detroit 2026`;
    if (updateHash) history.replaceState(null, '', `#${slides[current].id}`);
    window.scrollTo(0, 0);
    updatePresenter();
    if (initialized && current !== oldIndex) {
      transition(slides[oldIndex], slides[current], Math.sign(current - oldIndex));
    }
    initialized = true;
  }
  function fromHash() {
    const index = slides.findIndex(slide => `#${slide.id}` === location.hash);
    show(index < 0 ? 0 : index, false);
  }
  function openPresenter() {
    notice.hidden = true;
    if (presenterWindow && !presenterWindow.closed) {
      presenterWindow.focus();
      updatePresenter();
      return;
    }
    presenterWindow = window.open('presenter.html', 'detroit-presenter', 'popup,width=1000,height=760');
    if (!presenterWindow) {
      notice.textContent = 'Presenter view was blocked. Allow popups for this deck and try again. Notes remain hidden from the slides.';
      notice.hidden = false;
    }
  }
  window.addEventListener('message', event => {
    if (!presenterWindow || event.source !== presenterWindow) return;
    if (event.data?.type === 'detroit-presenter-ready') updatePresenter();
    if (event.data?.type !== 'detroit-presenter-command') return;
    if (event.data.action === 'previous') show(current - 1);
    if (event.data.action === 'next') show(current + 1);
  });
  async function fullscreen() {
    notice.hidden = true;
    if (!document.fullscreenEnabled) {
      notice.textContent = 'Full screen is unavailable here. Open the deck in a standalone browser or use its full-screen command.';
      notice.hidden = false;
      return;
    }
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else await document.documentElement.requestFullscreen();
    } catch (error) {
      notice.textContent = `Full screen could not open: ${error.message}. Use the browser full-screen command instead.`;
      notice.hidden = false;
    }
  }
  previous.addEventListener('click', () => show(current - 1));
  next.addEventListener('click', () => show(current + 1));
  document.getElementById('presenter').addEventListener('click', openPresenter);
  document.getElementById('fullscreen').addEventListener('click', fullscreen);
  document.getElementById('print').addEventListener('click', () => window.print());
  window.addEventListener('hashchange', fromHash);
  document.addEventListener('keydown', event => {
    if (event.altKey || event.ctrlKey || event.metaKey || /^(INPUT|TEXTAREA|SELECT|BUTTON|A)$/.test(event.target.tagName)) return;
    const actions = {
      ArrowRight: () => show(current + 1), PageDown: () => show(current + 1),
      ' ': () => show(current + 1), ArrowLeft: () => show(current - 1),
      PageUp: () => show(current - 1), Home: () => show(0), End: () => show(slides.length - 1),
      p: openPresenter, P: openPresenter, f: fullscreen, F: fullscreen
    };
    if (actions[event.key]) {
      event.preventDefault();
      actions[event.key]();
    }
  });
  // Print exposes every slide, so remove screen-only accessibility hiding too.
  reducedMotion.addEventListener('change', stopMotion);
  printMedia.addEventListener('change', stopMotion);
  window.addEventListener('resize', stopMotion);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stopMotion();
  });
  window.addEventListener('beforeprint', () => {
    stopMotion();
    slides.forEach(slide => {
      slide.removeAttribute('aria-hidden');
      slide.inert = false;
    });
  });
  window.addEventListener('afterprint', () => show(current, false));
  fromHash();
  document.documentElement.classList.add('js');
})();
