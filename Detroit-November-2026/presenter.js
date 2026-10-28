(() => {
  const audience = window.opener;
  const back = document.getElementById('back');
  const forward = document.getElementById('forward');
  const connection = document.getElementById('connection');
  let connected = false;
  let lastUpdate = 0;
  let runningSince = null;
  let accumulated = 0;

  function send(action) {
    if (audience && !audience.closed && connected) {
      audience.postMessage({ type: 'detroit-presenter-command', action }, '*');
    }
  }
  window.addEventListener('message', event => {
    if (!audience || event.source !== audience || event.data?.type !== 'detroit-presenter-state') return;
    const state = event.data;
    if (!Number.isInteger(state.index) || !Number.isInteger(state.count) ||
        state.index < 0 || state.index >= state.count ||
        !['title', 'nextTitle', 'time', 'notes'].every(key => typeof state[key] === 'string')) return;
    connected = true;
    lastUpdate = Date.now();
    connection.textContent = 'Connected. Navigation here updates the audience window; notes remain here.';
    document.getElementById('position').textContent = `Slide ${state.index + 1} of ${state.count}`;
    document.getElementById('current-title').textContent = state.title;
    document.getElementById('next-title').textContent = state.nextTitle.replace(/\s+/g, ' ').trim();
    document.getElementById('chapter').textContent = `Chapter schedule: ${state.time}`;
    // Only the known opener supplies the deck's own trusted note templates.
    document.getElementById('speaker-notes').innerHTML = state.notes;
    back.disabled = state.index === 0;
    forward.disabled = state.index === state.count - 1;
  });
  back.addEventListener('click', () => send('previous'));
  forward.addEventListener('click', () => send('next'));
  document.addEventListener('keydown', event => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.target.tagName === 'BUTTON') return;
    if (['ArrowRight', 'PageDown', ' '].includes(event.key)) { event.preventDefault(); send('next'); }
    if (['ArrowLeft', 'PageUp'].includes(event.key)) { event.preventDefault(); send('previous'); }
  });
  document.getElementById('timer-toggle').addEventListener('click', event => {
    if (runningSince === null) {
      runningSince = performance.now();
      event.target.textContent = 'Pause timer';
    } else {
      accumulated += performance.now() - runningSince;
      runningSince = null;
      event.target.textContent = 'Resume timer';
    }
  });
  document.getElementById('timer-reset').addEventListener('click', () => {
    accumulated = 0;
    runningSince = null;
    document.getElementById('timer-toggle').textContent = 'Start timer';
    document.getElementById('elapsed').textContent = '00:00:00';
  });
  setInterval(() => {
    const seconds = Math.floor((accumulated + (runningSince === null ? 0 : performance.now() - runningSince)) / 1000);
    document.getElementById('elapsed').textContent = [Math.floor(seconds / 3600), Math.floor(seconds / 60) % 60, seconds % 60]
      .map(value => String(value).padStart(2, '0')).join(':');
    if (!audience || audience.closed) {
      connected = false;
      back.disabled = forward.disabled = true;
      connection.textContent = 'Audience window is not connected. Reopen Presenter view from the deck.';
    } else if (!connected && Date.now() - lastUpdate > 2000) {
      audience.postMessage({ type: 'detroit-presenter-ready' }, '*');
      lastUpdate = Date.now();
    }
  }, 500);
  if (audience) audience.postMessage({ type: 'detroit-presenter-ready' }, '*');
})();
