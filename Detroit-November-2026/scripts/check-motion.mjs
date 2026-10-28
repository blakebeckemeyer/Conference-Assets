import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';

const source = readFileSync(new URL('../deck.js', import.meta.url), 'utf8');

function harness({ reduced = false, animate = true } = {}) {
  const animations = [];
  const events = {};
  const media = {};
  const element = () => ({
    classList: {
      values: new Set(),
      add(name) { this.values.add(name); },
      remove(name) { this.values.delete(name); },
      toggle(name, enabled) { enabled ? this.add(name) : this.remove(name); }
    },
    attributes: {},
    setAttribute(name, value) { this.attributes[name] = value; },
    removeAttribute(name) { delete this.attributes[name]; },
    addEventListener(name, callback) { this[name] = callback; }
  });
  const controls = Object.fromEntries(
    ['previous', 'next', 'notice', 'position', 'chapter-time', 'presenter', 'fullscreen', 'print']
      .map(id => [id, element()])
  );
  const slides = ['opening', 'opening', 'm365'].map((segment, i) => {
    const slide = element();
    Object.assign(slide, { id: `slide-${i + 1}`, dataset: { segment } });
    const heading = { innerText: `Title ${i}`, textContent: `Title ${i}` };
    const artifact = {};
    if (animate) {
      slide.animate = artifact.animate = (frames, options) => {
        const animation = { frames, options, cancelled: false, cancel() { this.cancelled = true; } };
        animations.push(animation);
        return animation;
      };
    }
    slide.querySelector = selector => selector === 'h1, h2' ? heading
      : selector === 'template.speaker-notes' ? { innerHTML: `Private notes ${i}` } : artifact;
    return slide;
  });
  const location = { hash: '' };
  const document = {
    querySelectorAll: () => slides,
    getElementById: id => controls[id],
    documentElement: element(),
    addEventListener: (name, callback) => { events[name] = callback; },
    hidden: false
  };
  const window = {
    matchMedia(query) {
      return media[query] ??= {
        matches: query === '(prefers-reduced-motion: reduce)' ? reduced : query.includes('min-width'),
        addEventListener(name, callback) { this[name] = callback; }
      };
    },
    addEventListener: (name, callback) => { events[name] = callback; },
    scrollTo() {}
  };
  runInNewContext(source, {
    window, document, location,
    history: { replaceState: (state, unused, hash) => { location.hash = hash; } }
  });
  return { slides, controls, animations, events, media, location, document };
}

const h = harness();
assert.equal(h.animations.length, 0, 'Initial/deep-link load must not animate');
h.controls.next.click();
assert.equal(h.location.hash, '#slide-2');
assert.equal(h.animations[1].options.duration, 340);
assert.ok(h.slides[0].inert && !h.slides[1].inert, 'Only current slide can receive focus');
const previousMotion = [...h.animations];
h.controls.next.click();
assert.ok(previousMotion.every(a => a.cancelled), 'Rapid navigation cancels prior work');
assert.equal(h.animations.at(-2).options.duration, 480, 'Chapter changes use a distinct transition');
assert.ok(h.animations.at(-2).frames[0].clipPath);
h.controls.previous.click();
assert.ok(h.animations.at(-2).frames[0].clipPath.includes('10% 0 0'), 'Reverse chapter navigation');
h.controls.previous.click();
assert.ok(h.animations.at(-2).frames[0].transform.includes('-40px'), 'Reverse within-chapter motion');
h.events.beforeprint();
assert.ok(h.animations.every(a => a.cancelled));
assert.ok(h.slides.every(s => !s.inert && !('aria-hidden' in s.attributes)));
assert.ok(h.slides.every(s => !s.classList.values.has('departing')));
h.events.afterprint();
assert.equal(h.slides.filter(s => !s.inert).length, 1);
const reduced = harness({ reduced: true });
reduced.controls.next.click();
assert.equal(reduced.animations.length, 0, 'Reduced motion must navigate instantly');
const unsupported = harness({ animate: false });
unsupported.controls.next.click();
assert.equal(unsupported.location.hash, '#slide-2', 'No-animation API fallback still navigates');
const preference = harness();
preference.controls.next.click();
preference.media['(prefers-reduced-motion: reduce)'].matches = true;
preference.media['(prefers-reduced-motion: reduce)'].change();
assert.ok(preference.animations.every(a => a.cancelled));
preference.controls.next.click();
assert.equal(preference.animations.length, 3, 'Changed preference prevents later animation');
console.log('Motion: direction, chapter pacing, interruption, inert focus, print, reduced-motion and fallback checks passed.');
