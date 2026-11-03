import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';

const source = readFileSync(new URL('../deck.js', import.meta.url), 'utf8');

function harness({ reduced = false, animate = true, initialHash = '#talk-a' } = {}) {
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
  const ids = [
    'previous', 'next', 'notice', 'position', 'chapter-time', 'presenter',
    'fullscreen', 'print', 'jump-talk-a', 'jump-talk-b'
  ];
  const controls = Object.fromEntries(ids.map(id => [id, element()]));
  const slideData = [
    ['talk-a', 'a-context'], ['talk-a', 'a-context'], ['talk-a', 'a-m365'],
    ['talk-b', 'b-why'], ['talk-b', 'b-demo']
  ];
  const slides = slideData.map(([talk, segment], i) => {
    const slide = element();
    Object.assign(slide, { id: i === 0 ? 'talk-a' : i === 3 ? 'talk-b' : `slide-${i + 1}`,
      dataset: { talk, segment } });
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
  const location = { hash: initialHash };
  const document = {
    querySelectorAll: () => slides,
    getElementById: id => controls[id],
    documentElement: element(),
    addEventListener: (name, callback) => { events[name] = callback; },
    hidden: false,
    title: ''
  };
  const window = {
    matchMedia(query) {
      return media[query] ??= {
        matches: query === '(prefers-reduced-motion: reduce)' ? reduced
          : query === 'print' ? false : query.includes('min-width'),
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
assert.equal(h.location.hash, '#talk-a');
assert.equal(h.controls.position.textContent, 'Talk A · 1/3');
h.controls.next.click();
assert.equal(h.location.hash, '#slide-2');
assert.equal(h.animations[1].options.duration, 340);
assert.ok(h.slides[0].inert && !h.slides[1].inert, 'Only the current slide can receive focus');
const previousMotion = [...h.animations];
h.controls.next.click();
assert.ok(previousMotion.every(animation => animation.cancelled), 'Rapid navigation cancels prior work');
assert.equal(h.animations.at(-2).options.duration, 480, 'Chapter changes use a distinct transition');
assert.ok(h.animations.at(-2).frames[0].clipPath);
h.controls.previous.click();
assert.ok(h.animations.at(-2).frames[0].clipPath.includes('10% 0 0'), 'Reverse chapter navigation');
h.controls.previous.click();
assert.ok(h.animations.at(-2).frames[0].transform.includes('-40px'), 'Reverse within-chapter motion');
h.controls.previous.click();
assert.equal(h.location.hash, '#talk-a', 'Talk A cannot navigate before its first slide');
h.controls['jump-talk-b'].click();
assert.equal(h.location.hash, '#talk-b', 'Talk selector starts the independent Foundry talk');
assert.equal(h.controls.position.textContent, 'Talk B · 1/2');
assert.ok(h.animations.at(-2).frames[0].clipPath, 'Changing talks uses the chapter transition');
h.controls.next.click();
assert.equal(h.controls.next.disabled, true, 'Talk B stops at its own last slide');
h.controls.next.click();
assert.equal(h.location.hash, '#slide-5', 'Talk B cannot advance into another range');
h.controls['jump-talk-a'].click();
assert.equal(h.location.hash, '#talk-a', 'Presenter/deck talk selector returns to Talk A start');
h.events.beforeprint();
assert.ok(h.animations.every(animation => animation.cancelled));
assert.ok(h.slides.every(slide => !slide.inert && !('aria-hidden' in slide.attributes)));
assert.ok(h.slides.every(slide => !slide.classList.values.has('departing')));
h.events.afterprint();
assert.equal(h.slides.filter(slide => !slide.inert).length, 1);
const deepLink = harness({ initialHash: '#talk-b' });
assert.equal(deepLink.controls.position.textContent, 'Talk B · 1/2', 'Foundry deep link opens its own start');
const reduced = harness({ reduced: true });
reduced.controls.next.click();
assert.equal(reduced.animations.length, 0, 'Reduced motion navigates instantly');
const unsupported = harness({ animate: false });
unsupported.controls.next.click();
assert.equal(unsupported.location.hash, '#slide-2', 'Fallback still navigates without Web Animations');
const preference = harness();
preference.controls.next.click();
preference.media['(prefers-reduced-motion: reduce)'].matches = true;
preference.media['(prefers-reduced-motion: reduce)'].change();
assert.ok(preference.animations.every(animation => animation.cancelled));
preference.controls.next.click();
assert.equal(preference.animations.length, 3, 'Changed preference prevents later animation');
console.log('Motion: independent talk ranges, direct entry, transitions, interruption, inert focus, print, reduced-motion and fallback checks passed.');
