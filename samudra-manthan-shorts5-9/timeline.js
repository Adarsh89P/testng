// Dispatcher: ?ep=5..9 picks the Short's timeline; shared helpers come from tlc.js.
export * from './tlc.js';
import { makeCueAt } from './tlc.js';
export const EP = (typeof location !== 'undefined' && new URLSearchParams(location.search).get('ep')) || (globalThis.EP_OVERRIDE ?? '5');
const M = await import(`./tl${EP}.js`);
export const DUR = M.DUR, CUES = M.CUES, frame = M.frame, HOOK = M.HOOK, THUMB = M.THUMB;
export const cueAt = makeCueAt(CUES, DUR);
