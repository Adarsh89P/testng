// ?v=puppet (default) | ?v=oil ; ?test=sheet for the character model sheet
import { DUR } from './timeline.js';
const q = new URLSearchParams(location.search);
const mod = await import(q.get('v') === 'oil' ? './oil.js' : './puppet.js');
const draw = await mod.setup(q);
window.render = t => draw(t); window.DUR = DUR;
window.render(0); window.READY = true;
