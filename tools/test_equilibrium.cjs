// Run the actual explainer script against a small DOM fixture; no browser dependency.
// Usage: node tools/test_equilibrium.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const html = fs.readFileSync(path.join(__dirname, '../explainers/equilibrium/index.html'), 'utf8');
const script = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n');
assert.ok(script, 'The explainer must contain its interactive code.');
const elements = new Map();
const get = id => {
  if (!elements.has(id)) elements.set(id, {value:'', textContent:'', style:{}, listeners:{}, attributes:{},
    addEventListener(event, handler) { this.listeners[event] = handler; },
    setAttribute(key, value) { this.attributes[key] = value; }});
  return elements.get(id);
};
get('log-k').value = '0.60'; get('initial-b').value = '20';
let reducedMotion = true, nextFrame = null;
vm.runInNewContext(script, {
  document:{getElementById:get}, performance:{now:() => 0},
  matchMedia:() => ({matches:reducedMotion}),
  requestAnimationFrame:callback => { nextFrame = callback; return 1; },
  cancelAnimationFrame:() => { nextFrame = null; },
});
const input = (id, value) => { get(id).value = String(value); get(id).listeners.input(); };
const click = id => get(id).listeners.click();
const value = id => Number.parseFloat(get(id).textContent);
for (const logK of [-2, 0, 2]) {
  for (const start of [1, 20, 99]) {
    input('log-k', logK); input('initial-b', start);
    const K = 10 ** logK, Q = start / (100-start);
    assert.ok(Math.abs(value('q') - Q) <= .00051);
    const direction = get('direction').textContent;
    assert.ok(direction.includes(Q < K ? 'below' : Q > K ? 'above' : 'equals'));
    assert.ok(Math.abs(value('free-energy') - 8.314462618*298.15*Math.log(Q/K)/1000) <= .0051);
    click('run');
    assert.ok(Math.abs(value('q') - K) <= .00051);
    assert.equal(value('free-energy'), 0);
    assert.ok(Math.abs(parseFloat(get('part-b').style.width) - 100*K/(1+K)) < 1e-10);
    assert.ok(Math.abs(parseFloat(get('part-a').style.width) + parseFloat(get('part-b').style.width) - 100) < 1e-10);
    click('reset');
    assert.ok(Math.abs(parseFloat(get('part-b').style.width) - start) < 1e-10);
  }
}
reducedMotion = false;
input('log-k', 0); input('initial-b', 20); click('run');
assert.equal(get('run').disabled, true);
nextFrame(650);
assert.ok(Math.abs(parseFloat(get('part-b').style.width) - (50 - 30/Math.E)) < 1e-10);
nextFrame(650*9);
assert.equal(get('run').disabled, false);
assert.equal(value('q'), 1);
click('run'); input('initial-b', 99);
assert.equal(nextFrame, null, 'Changing a slider cancels the previous animation.');
assert.equal(get('run').disabled, false);
assert.equal(parseFloat(get('part-b').style.width), 99);
console.log('Equilibrium checks passed: 9 mixtures, Gibbs energy, conservation, relaxation, reset, reduced motion.');
