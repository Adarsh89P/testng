// Subtitles and the puppet theatre frame (2D overlay, viewport coordinates)
import { W, H, cueAt, ss } from './timeline.js';
const PI = Math.PI;

export function theatreFrame() {
  const c = document.createElement('canvas'); c.width = W; c.height = H; const st = c.getContext('2d');
  const lac = '#2a0d08', gold = '#8a6430';
  st.fillStyle = lac; st.fillRect(0, 0, W, 96); st.fillRect(0, H - 110, W, 110); st.fillRect(0, 0, 30, H); st.fillRect(W - 30, 0, 30, H);
  st.fillStyle = '#46140c'; st.fillRect(30, 22, W - 60, 52); st.fillRect(30, H - 92, W - 60, 40);
  st.strokeStyle = gold; st.lineWidth = 2.5;
  for (let x = 40; x < W - 60; x += 100) { st.beginPath(); for (let i = 0; i <= 30; i++) { const a = i / 30 * PI * 2.1, r = 22 * (1 - i / 30 * .75), px = x + 50 + Math.cos(a) * r, py = 48 + Math.sin(a) * r * .7; i ? st.lineTo(px, py) : st.moveTo(px, py); } st.stroke(); }
  st.strokeRect(36, 18, W - 72, 60); st.strokeRect(36, H - 96, W - 72, 48);
  return c;
}
// puppet: the storyteller's lacquer board with a lotus seal
export function placard(g, t) {
  const c = cueAt(t); if (!c) return; const [text, u] = c, a = ss(u / .15);
  g.save(); g.globalAlpha = a; g.font = '700 54px "FreeSerif"';
  const tw = g.measureText(text).width, seal = 52, w = Math.min(1000, 24 + seal + 20 + tw + 36), h = 88, x = W / 2 - w / 2, y = 1488 + (1 - a) * 14;
  g.shadowColor = 'rgba(0,0,0,.6)'; g.shadowBlur = 20; g.shadowOffsetY = 4;
  const gr = g.createLinearGradient(0, y, 0, y + h); gr.addColorStop(0, 'rgba(46,22,14,.94)'); gr.addColorStop(1, 'rgba(22,10,7,.94)');
  g.fillStyle = gr; g.beginPath(); g.roundRect(x, y, w, h, 8); g.fill(); g.shadowColor = 'transparent';
  g.strokeStyle = 'rgba(168,129,63,.85)'; g.lineWidth = 1.6; g.beginPath(); g.roundRect(x + 7, y + 7, w - 14, h - 14, 4); g.stroke();
  const sx = x + 24, sy = y + (h - seal) / 2;
  g.fillStyle = '#b3261b'; g.beginPath(); g.roundRect(sx, sy, seal, seal, 4); g.fill();
  g.fillStyle = '#f6dcc0'; for (const an of [-.9, -.45, 0, .45, .9]) { g.save(); g.translate(sx + seal / 2, sy + seal * .76); g.rotate(an); g.beginPath(); g.ellipse(0, -12, 4.6, 12, 0, 0, 2 * PI); g.fill(); g.restore(); }
  g.fillStyle = '#f3e2bf'; g.textBaseline = 'middle'; g.textAlign = 'left'; g.fillText(text, sx + seal + 20, y + h / 2 + 3, w - (seal + 80));
  g.restore();
}
// oil: crisp serif text in a calm dark plane (knife strokes can't carry small letters)
export function oilSub(g, t) {
  const c = cueAt(t); if (!c) return; const [text, u] = c, a = ss(u / .15);
  g.save(); g.globalAlpha = a; g.font = '700 56px "FreeSerif"';
  const tw = Math.min(980, g.measureText(text).width), w = tw + 70, h = 92, x = W / 2 - w / 2, y = 1488;
  g.fillStyle = 'rgba(16,12,24,.62)'; g.beginPath(); g.roundRect(x, y, w, h, 46); g.fill();
  g.fillStyle = '#fbefd6'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.shadowColor = 'rgba(0,0,0,.5)'; g.shadowBlur = 6;
  g.fillText(text, W / 2, y + h / 2 + 3, 980);
  g.restore();
}
