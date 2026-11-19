import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.min.js';

/* 3D record viewer — sleeve (Lowrider Anthems) + record with both labels. Data comes from the stage's data-* attributes. */
const stage = document.getElementById('stage'), canvas = document.getElementById('c'), hint = document.getElementById('hint');
if (stage && canvas) {
let renderer;
try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true }); } catch (e) { stage.classList.add('nogl'); throw e; }
stage.classList.remove('nogl');
renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 50);
const BASEZ = 6.3; camera.position.set(0, 0.75, BASEZ); camera.lookAt(0, -0.35, 0);
scene.add(new THREE.HemisphereLight(0xfff4e0, 0x20302a, 1.1));
const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(2.5, 3, 4); scene.add(key);
const rim = new THREE.DirectionalLight(0xffc870, 0.8); rim.position.set(-3, 1, -3); scene.add(rim);
const loader = new THREE.TextureLoader(); loader.setCrossOrigin('anonymous');
const maxAniso = renderer.capabilities.getMaxAnisotropy();
const tex = u => { const t = loader.load(u); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = maxAniso; return t; };
const S = 1.8, D = 0.035;
const edge = new THREE.MeshStandardMaterial({ color: 0xece6da, roughness: 0.8 });
const front = new THREE.MeshStandardMaterial({ roughness: 0.38, metalness: 0.02 });
const back = new THREE.MeshStandardMaterial({ roughness: 0.38, metalness: 0.02 });
const sleeve = new THREE.Mesh(new THREE.BoxGeometry(S, S, D), [edge, edge, edge, edge, front, back]);
function discTex(labelUrl, flip) {
  const c = document.createElement('canvas'); c.width = c.height = 1024; const g = c.getContext('2d');
  g.fillStyle = '#0b0b0b'; g.beginPath(); g.arc(512, 512, 512, 0, Math.PI * 2); g.fill();
  for (let r = 172; r < 505; r += 2.2) { g.strokeStyle = `rgba(255,255,255,${0.025 + Math.random() * 0.035})`; g.lineWidth = 1; g.beginPath(); g.arc(512, 512, r, 0, Math.PI * 2); g.stroke(); }
  g.strokeStyle = 'rgba(255,255,255,.12)'; g.lineWidth = 6; g.beginPath(); g.arc(512, 512, 500, 0, Math.PI * 2); g.stroke();
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = maxAniso;
  if (labelUrl) {
    const img = new Image(); img.crossOrigin = 'anonymous';
    img.onload = () => { g.save(); if (flip) { g.translate(512, 512); g.rotate(Math.PI); g.translate(-512, -512); } g.beginPath(); g.arc(512, 512, 168, 0, Math.PI * 2); g.clip(); g.drawImage(img, 344, 344, 336, 336); g.restore();
      g.fillStyle = '#d8d8d8'; g.beginPath(); g.arc(512, 512, 9, 0, Math.PI * 2); g.fill(); t.needsUpdate = true; };
    img.src = labelUrl;
  }
  return t;
}
const R = 0.86, T = 0.012;
const recSide = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.35 });
const recA = new THREE.MeshStandardMaterial({ roughness: 0.3, metalness: 0.05, emissive: 0xffffff, emissiveIntensity: 0.32 }), recB = new THREE.MeshStandardMaterial({ roughness: 0.3, metalness: 0.05, emissive: 0xffffff, emissiveIntensity: 0.32 });
const record = new THREE.Mesh(new THREE.CylinderGeometry(R, R, T, 96, 1), [recSide, recA, recB]);
record.rotation.x = Math.PI / 2; record.rotation.y = Math.PI / 2;
const disc = new THREE.Group(); disc.add(record);
const group = new THREE.Group(); group.add(sleeve); group.add(disc); scene.add(group);
const PY = -1.38;
function blobTex(rgb, a0, a1) { const N = 256, [r, g, b] = rgb.split(',').map(Number), d = new Uint8Array(N * N * 4); const ss = (lo, hi, x) => { x = Math.min(1, Math.max(0, (x - lo) / (hi - lo))); return x * x * (3 - 2 * x); }; for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const t = Math.min(1, Math.hypot(x + 0.5 - N / 2, y + 0.5 - N / 2) / (N / 2)); const f = 1 - ss(0, 1, t), a = (a0 * f * f * f + a1 * f * f * f * f * f) / 1.3; const k = (y * N + x) * 4; d[k] = r; d[k + 1] = g; d[k + 2] = b; d[k + 3] = Math.round(a * 255); } const t = new THREE.DataTexture(d, N, N, THREE.RGBAFormat); t.colorSpace = THREE.SRGBColorSpace; t.magFilter = t.minFilter = THREE.LinearFilter; t.generateMipmaps = false; t.needsUpdate = true; return t; }
const shadowMat = new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false, toneMapped: false, fog: false });
const shadow = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 0.95), shadowMat); shadow.visible = false; /* shadow removed */
const halo = new THREE.Mesh(new THREE.PlaneGeometry(4.2, 1.7), new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false, toneMapped: false, fog: false, blending: THREE.AdditiveBlending })); halo.visible = false; /* halo removed */
function shadePod() {}


const mode = stage.dataset.mode === 'lr' ? 'lr' : 'mp';
let rotY = -0.35, rotX = 0.12, velY = 0, velX = 0, targetOut = 0, out = 0, spin = false, zoom = BASEZ, targetRotY = null, idle = 0;
const viewBtns = [...document.querySelectorAll('#views button')];
const press = (v, on) => { const b = viewBtns.find(b => b.dataset.v === v); if (b) b.setAttribute('aria-pressed', on); };
viewBtns.forEach(b => b.addEventListener('click', () => {
  const v = b.dataset.v;
  if (v === 'front' || v === 'a') { targetRotY = 0; press(v, true); press(v === 'a' ? 'b' : 'back', false); }
  if (v === 'back' || v === 'b') { targetRotY = Math.PI; press(v, true); press(v === 'b' ? 'a' : 'front', false); }
  if (v === 'out') { targetOut = targetOut ? 0 : 1; press('out', !!targetOut); }
  if (v === 'spin') { spin = !spin; press('spin', spin); if (spin && mode === 'lr' && !targetOut) { targetOut = 1; press('out', true); } }
}));

if (mode === 'lr') { if (stage.dataset.front) front.map = tex(stage.dataset.front); if (stage.dataset.back) back.map = tex(stage.dataset.back); front.needsUpdate = back.needsUpdate = true; sleeve.visible = true; } else { sleeve.visible = false; }
recA.map = recA.emissiveMap = discTex(stage.dataset.labelA, false);
recB.map = recB.emissiveMap = discTex(stage.dataset.labelB, true);
recA.needsUpdate = recB.needsUpdate = true;
disc.scale.setScalar(mode === 'mp' ? 1.12 : 1);

addEventListener('rec-play', e => {
  const sd = e.detail;
  if (sd) { spin = true; press('spin', true); if (mode === 'lr') { targetOut = 1; press('out', true); } targetRotY = sd === 'a' ? 0 : Math.PI; press(mode === 'lr' ? 'front' : 'a', sd === 'a'); if (mode === 'mp') press('b', sd === 'b'); }
  else { spin = false; press('spin', false); }
});
const pts = new Map();
stage.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; stage.setPointerCapture(e.pointerId); pts.set(e.pointerId, [e.clientX, e.clientY]); targetRotY = null; if (hint) hint.style.opacity = 0; });
stage.addEventListener('pointermove', e => {
  if (e.pointerType !== 'mouse' || !pts.has(e.pointerId)) return; const prev = pts.get(e.pointerId); pts.set(e.pointerId, [e.clientX, e.clientY]);
  if (pts.size === 2) { const [a, b] = [...pts.values()]; const d = Math.hypot(a[0] - b[0], a[1] - b[1]); if (stage._pd) zoom = THREE.MathUtils.clamp(zoom * (stage._pd / d), 3.4, 8.5); stage._pd = d; return; }
  const dx = e.clientX - prev[0], dy = e.clientY - prev[1]; velY = dx * 0.008; velX = dy * 0.006; rotY += velY; rotX = THREE.MathUtils.clamp(rotX + velX, -0.9, 0.9);
});
const end = e => { pts.delete(e.pointerId); stage._pd = null; }; stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end);
stage.addEventListener('dblclick', e => { if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return; targetRotY = -0.35; rotX = 0.12; zoom = BASEZ; targetOut = 0; spin = false; press('out', false); press('spin', false); });
stage.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') rotY -= 0.2; if (e.key === 'ArrowRight') rotY += 0.2; });
function resize() { const w = stage.clientWidth, h = stage.clientHeight; if (!w) return; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
new ResizeObserver(resize).observe(stage); resize();
const isDark = () => true; // dark mode only
function themeEdge() { const dark = isDark(); edge.color.set(dark ? 0xd9d2c4 : 0xf1ebdf); shadePod(dark); scene.fog = new THREE.Fog(dark ? 0x06090a : 0xf4f2ee, 6.6, 8.4); }
addEventListener('themechange', themeEdge); themeEdge();
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches; const clock = new THREE.Clock();
function tick() {
  requestAnimationFrame(tick);
  if (document.hidden) return;
  const dt = Math.min(clock.getDelta(), 0.05);
  if (!pts.size) {
    velY *= 0.92; velX *= 0.9; rotY += velY; rotX = THREE.MathUtils.clamp(rotX + velX, -0.9, 0.9);
    if (targetRotY !== null) { let d = targetRotY - rotY; d = Math.atan2(Math.sin(d), Math.cos(d)); rotY += d * 0.1; rotX += (0 - rotX) * 0.1; if (Math.abs(d) < 0.001) targetRotY = null; }
    else if (!reduce && Math.abs(velY) < 0.0005) { idle += dt; rotY += Math.sin(idle * 0.6) * 0.0012; }
  }
  out += (targetOut - out) * (reduce ? 1 : 0.08);
  if (mode === 'lr') { disc.position.x = out * 1.05 - out * 0.5; sleeve.position.x = -out * 0.5; } else { disc.position.x = 0; }
  if (spin) record.rotation.y += dt * (reduce ? 0 : 3.5);
  const bob = reduce ? 0 : Math.sin(clock.elapsedTime * 1.3) * 0.025;
  group.position.y = (mode === 'mp' ? -0.3 : -0.43) + bob;
  group.rotation.set(rotX, rotY, 0);
  camera.position.z += (zoom - camera.position.z) * 0.15;
  renderer.render(scene, camera);
}
tick();
}
