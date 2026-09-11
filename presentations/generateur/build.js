/* Genere une presentation commerciale par produit Konformix. */
const fs = require("fs");
const path = require("path");
const React = require("react");
const RD = require("react-dom/server");
const tb = require("react-icons/tb");
const sharp = require("sharp");
const pptxgen = require("pptxgenjs");
const { BRAND, COMPANY, FAQ, PRODUCTS } = require("./content.js");

// ---------------------------------------------------------------- palette
const INK = "05080F", PAPER = "080C17", SURF = "0E1523", SURF2 = "131C2E";
const LINE = "1F2A40", BRANDC = "38BDF8", SOFT = "7DD3FC", ACCENT = "A78BFA";
const SIGNAL = "34D399", GOLD = "FBBF24", DANGER = "F87171";
const TEXT = "E7ECF6", MUTED = "93A1BC", DIM = "5B6A85";
const HEAD = "Cambria", BODY = "Calibri";
const W = 13.33, H = 7.5, M = 0.75;

// ---------------------------------------------------------------- visuels
const LOGO_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="512" height="512">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#38BDF8"/><stop offset="100%" stop-color="#A78BFA"/>
  </linearGradient></defs>
  <rect width="32" height="32" rx="7.5" fill="url(#g)"/>
  <path d="M9.5 8.2v15.6" stroke="#05080F" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M22.6 8.6 14.2 16.6l3.4 3.3" stroke="#05080F" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <path d="m17.6 19.9 5.6-5.4" stroke="#F8FAFF" stroke-width="2.6" stroke-linecap="round"/>
</svg>`;

const cacheIcon = new Map();
async function iconData(name, color, px) {
  px = px || 256;
  const key = name + color + px;
  if (cacheIcon.has(key)) return cacheIcon.get(key);
  const El = tb[name];
  if (!El) throw new Error("icone inconnue : " + name);
  const svg = RD.renderToStaticMarkup(React.createElement(El, { color: "#" + color, size: px }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  const data = "image/png;base64," + buf.toString("base64");
  cacheIcon.set(key, data);
  return data;
}
async function logoData() {
  if (cacheIcon.has("logo")) return cacheIcon.get("logo");
  const buf = await sharp(Buffer.from(LOGO_SVG)).png().toBuffer();
  const data = "image/png;base64," + buf.toString("base64");
  cacheIcon.set("logo", data);
  return data;
}

// ------------------------------------------------------------- primitives
const txt = (o) => Object.assign({ isTextBox: true, fontFace: BODY, color: TEXT, margin: 0, valign: "top" }, o);

function card(slide, x, y, w, h, opt) {
  opt = opt || {};
  slide.addShape("roundRect", {
    x, y, w, h, rectRadius: 0.09,
    fill: { color: opt.fill || SURF, transparency: opt.transparency || 0 },
    line: { color: opt.line || LINE, width: 1 },
  });
}
function glow(slide, x, y, w, h, color, transparency) {
  slide.addShape("ellipse", { x, y, w, h, fill: { color, transparency }, line: { color, width: 0, transparency: 100 } });
}
async function tile(slide, iconName, x, y, size, color) {
  slide.addShape("roundRect", {
    x, y, w: size, h: size, rectRadius: 0.28,
    fill: { color, transparency: 84 }, line: { color, width: 1, transparency: 60 },
  });
  const inner = size * 0.54;
  slide.addImage({ data: await iconData(iconName, color, 256), x: x + (size - inner) / 2, y: y + (size - inner) / 2, w: inner, h: inner });
}
function heading(slide, eyebrow, title, sub) {
  slide.addText(eyebrow.toUpperCase(), txt({ x: M, y: 0.42, w: 11.83, h: 0.28, fontSize: 11, bold: true, color: ACCENT, charSpacing: 1.6 }));
  slide.addText(title, txt({ x: M, y: 0.72, w: 11.83, h: 0.72, fontSize: 31, bold: true, fontFace: HEAD, color: "FFFFFF" }));
  if (sub) slide.addText(sub, txt({ x: M, y: 1.46, w: 10.6, h: 0.4, fontSize: 13.5, color: MUTED }));
}
function footer(slide, product) {
  slide.addText(BRAND.name + " · " + product.name, txt({ x: M, y: 7.02, w: 7, h: 0.25, fontSize: 9, color: DIM }));
  slide.addText(BRAND.domain, txt({ x: 9.5, y: 7.02, w: 3.08, h: 0.25, fontSize: 9, color: DIM, align: "right" }));
}
function bullets(slide, items, x, y, w, h, color, size) {
  slide.addText(
    items.map((t, i) => ({ text: t, options: { bullet: { code: "2022" }, breakLine: i !== items.length - 1 } })),
    txt({ x, y, w, h, fontSize: size || 12, color: color || MUTED, paraSpaceAfter: 7, lineSpacing: 15 })
  );
}

// ---------------------------------------------------------------- diapos
async function slideCover(pres, p) {
  const s = pres.addSlide();
  s.background = { color: INK };
  glow(s, 8.0, -2.0, 7.4, 6.4, BRANDC, 90);
  glow(s, -1.8, 3.9, 6.0, 5.0, ACCENT, 93);
  s.addImage({ data: await logoData(), x: M, y: 1.15, w: 1.12, h: 1.12 });
  s.addText(BRAND.name, txt({ x: 2.05, y: 1.42, w: 5, h: 0.6, fontSize: 26, bold: true, color: "FFFFFF" }));
  s.addText(BRAND.tagline, txt({ x: 2.07, y: 1.92, w: 6, h: 0.3, fontSize: 12, color: MUTED }));
  s.addText(p.kicker.toUpperCase(), txt({ x: M, y: 3.15, w: 10, h: 0.3, fontSize: 12, bold: true, color: SOFT, charSpacing: 1.8 }));
  s.addText(p.name, txt({ x: M, y: 3.5, w: 10.5, h: 1.0, fontSize: 46, bold: true, fontFace: HEAD, color: "FFFFFF" }));
  s.addText(p.summary, txt({ x: M, y: 4.62, w: 7.9, h: 1.0, fontSize: 15.5, color: MUTED, lineSpacing: 22 }));
  s.addText("Présentation commerciale", txt({ x: M, y: 6.45, w: 6, h: 0.3, fontSize: 12, color: TEXT, bold: true }));
  s.addText(BRAND.domain + "  ·  " + BRAND.email, txt({ x: 7.0, y: 6.45, w: 5.58, h: 0.3, fontSize: 12, color: MUTED, align: "right" }));
  s.addNotes(`Ouverture. ${p.name} : ${p.kicker}. Rappeler en une phrase ce que fait le module, puis annoncer le plan : le contexte réglementaire, ce que nous constatons, le produit, la démarche.`);
}

async function slideCompany(pres, p) {
  const s = pres.addSlide();
  s.background = { color: PAPER };
  heading(s, "La société", "Konformix en bref");
  s.addText(COMPANY.pitch, txt({ x: M, y: 1.72, w: 6.3, h: 1.75, fontSize: 14.5, color: TEXT, lineSpacing: 22 }));
  s.addText(COMPANY.pitch2, txt({ x: M, y: 3.62, w: 6.3, h: 0.95, fontSize: 13, color: MUTED, lineSpacing: 20 }));
  const facts = [
    { i: "TbMapPin", t: "Conçu et édité à Dakar, Sénégal" },
    { i: "TbBuildingBank", t: "Pour les banques et établissements financiers de l'UEMOA" },
    { i: "TbLock", t: "Déploiement sur site ou en hébergement souverain régional" },
  ];
  let fy = 4.82;
  for (const f of facts) {
    await tile(s, f.i, M, fy, 0.42, BRANDC);
    s.addText(f.t, txt({ x: M + 0.62, y: fy + 0.04, w: 5.6, h: 0.35, fontSize: 12.5, color: TEXT }));
    fy += 0.66;
  }
  card(s, 7.35, 1.72, 5.23, 4.68);
  s.addText("L'équipe fondatrice", txt({ x: 7.7, y: 2.02, w: 4.5, h: 0.35, fontSize: 15, bold: true, color: "FFFFFF", fontFace: HEAD }));
  let cy = 2.6;
  for (const f of COMPANY.founders) {
    await tile(s, "TbUsers", 7.7, cy + 0.02, 0.52, ACCENT);
    s.addText(f.name, txt({ x: 8.42, y: cy, w: 3.9, h: 0.3, fontSize: 13.5, bold: true, color: TEXT }));
    s.addText(f.role, txt({ x: 8.42, y: cy + 0.3, w: 3.9, h: 0.28, fontSize: 11, color: ACCENT }));
    s.addText(f.bio, txt({ x: 7.7, y: cy + 0.68, w: 4.6, h: 1.0, fontSize: 11, color: MUTED, lineSpacing: 16 }));
    cy += 1.95;
  }
  footer(s, p);
  s.addNotes("Présentation de la société : un éditeur régional, fondé par des praticiens de la conformité bancaire, qui déploie sans faire sortir les données du périmètre de la banque.");
}

function slideContext(pres, p) {
  const s = pres.addSlide();
  s.background = { color: PAPER };
  heading(s, "Le contexte", "Un cadre durci, un superviseur plus ferme");
  const w = 3.71;
  COMPANY.stats.forEach((st, i) => {
    const x = M + i * (w + 0.35);
    card(s, x, 2.0, w, 2.55);
    s.addText(st.v, txt({ x: x + 0.35, y: 2.2, w: w - 0.7, h: 0.9, fontSize: 54, bold: true, fontFace: HEAD, color: i === 1 ? ACCENT : BRANDC }));
    s.addText(st.l, txt({ x: x + 0.35, y: 3.18, w: w - 0.7, h: 0.85, fontSize: 12.5, color: TEXT, lineSpacing: 17 }));
    s.addText("Source : " + st.s, txt({ x: x + 0.35, y: 4.12, w: w - 0.7, h: 0.3, fontSize: 9.5, color: DIM }));
  });
  card(s, M, 4.95, 11.83, 1.65, { fill: SURF2 });
  s.addText("Les instructions du 18 mars 2025 ont relevé le niveau d'exigence sur l'identification du client, la connaissance du bénéficiaire effectif et le dispositif de contrôle interne.",
    txt({ x: M + 0.45, y: 5.2, w: 11, h: 0.5, fontSize: 14, color: TEXT, lineSpacing: 20 }));
  s.addText("Le même cadre s'applique désormais aux huit pays de l'Union : ce qui est exigé à Dakar l'est aussi à Abidjan, Lomé ou Bamako.",
    txt({ x: M + 0.45, y: 5.9, w: 11, h: 0.45, fontSize: 12.5, color: MUTED }));
  footer(s, p);
  s.addNotes("Poser le contexte avant le produit : la contrainte vient du régulateur, pas de nous. Les trois chiffres sont vérifiables auprès de la BCEAO.");
}

function slideChart(pres, p) {
  const s = pres.addSlide();
  s.background = { color: PAPER };
  heading(s, "Le signal", "Un superviseur nettement plus ferme en 2025");
  s.addText(COMPANY.chart.note, txt({ x: M, y: 1.95, w: 4.1, h: 1.9, fontSize: 13, color: TEXT, lineSpacing: 20 }));
  card(s, M, 4.05, 4.1, 2.2, { fill: SURF2 });
  s.addText(COMPANY.chart.motifs, txt({ x: M + 0.32, y: 4.32, w: 3.46, h: 1.7, fontSize: 12, color: MUTED, lineSpacing: 18 }));
  s.addChart("bar", [
    { name: "2024", labels: COMPANY.chart.cats, values: COMPANY.chart.y2024 },
    { name: "2025", labels: COMPANY.chart.cats, values: COMPANY.chart.y2025 },
  ], {
    x: 5.15, y: 1.85, w: 7.45, h: 4.5,
    barDir: "col", barGapWidthPct: 55,
    chartColors: [BRANDC, GOLD],
    showTitle: false,
    showLegend: true, legendPos: "t", legendColor: TEXT, legendFontSize: 11, legendFontFace: BODY,
    showValue: true, dataLabelPosition: "outEnd", dataLabelColor: TEXT, dataLabelFontSize: 11, dataLabelFontFace: BODY,
    catAxisLabelColor: MUTED, catAxisLabelFontSize: 11, catAxisLabelFontFace: BODY, catAxisLineShow: false,
    valAxisLabelColor: MUTED, valAxisLabelFontSize: 10, valAxisLabelFontFace: BODY, valAxisLineShow: false,
    valGridLine: { color: "1B2740", size: 1 }, catGridLine: { style: "none" },
    valAxisMaxVal: 45, plotArea: { fill: { color: PAPER } }, chartArea: { fill: { color: PAPER } },
  });
  s.addText("Source : Commission Bancaire de l'UMOA, mesures 2024 et 2025.", txt({ x: 5.15, y: 6.42, w: 7.45, h: 0.3, fontSize: 9.5, color: DIM }));
  footer(s, p);
  s.addNotes("Le point de bascule de l'argumentaire : le risque n'est plus théorique. Les injonctions ont doublé, les sanctions pécuniaires progressé de 118 % en un an.");
}

async function slidePains(pres, p) {
  const s = pres.addSlide();
  s.background = { color: PAPER };
  heading(s, "Le constat", "Le problème n'est pas le manque de règles",
    "Ce que nous relevons dans presque tous les référentiels clients que nous auditons.");
  const w = 5.75, h = 2.05;
  for (let i = 0; i < COMPANY.pains.length; i++) {
    const c = COMPANY.pains[i];
    const x = M + (i % 2) * (w + 0.33), y = 2.2 + Math.floor(i / 2) * (h + 0.33);
    card(s, x, y, w, h);
    await tile(s, c.i, x + 0.35, y + 0.32, 0.62, i === 2 ? DANGER : BRANDC);
    s.addText(c.t, txt({ x: x + 1.15, y: y + 0.32, w: w - 1.5, h: 0.55, fontSize: 15, bold: true, color: "FFFFFF", lineSpacing: 20 }));
    s.addText(c.d, txt({ x: x + 1.15, y: y + 0.95, w: w - 1.5, h: 1.0, fontSize: 12, color: MUTED, lineSpacing: 17 }));
  }
  footer(s, p);
  s.addNotes("Faire réagir : demander au client lequel de ces quatre constats lui parle le plus. C'est la question qui ouvre la discussion sur le diagnostic.");
}

async function slidePromise(pres, p) {
  const s = pres.addSlide();
  s.background = { color: INK };
  glow(s, 8.2, 0.9, 6.0, 5.6, p.key === "kontrol" ? BRANDC : ACCENT, 86);
  s.addText("Le module", txt({ x: M, y: 0.9, w: 6, h: 0.3, fontSize: 11, bold: true, color: ACCENT, charSpacing: 1.6 }));
  s.addText(p.name, txt({ x: M, y: 1.25, w: 7.2, h: 0.9, fontSize: 40, bold: true, fontFace: HEAD, color: "FFFFFF" }));
  s.addText(p.kicker, txt({ x: M, y: 2.2, w: 7.0, h: 0.4, fontSize: 15, color: SOFT }));
  s.addText(p.summary, txt({ x: M, y: 2.85, w: 7.0, h: 1.3, fontSize: 15, color: MUTED, lineSpacing: 23 }));
  card(s, M, 4.35, 7.0, 1.55, { fill: SURF, line: SIGNAL });
  s.addText("RÉSULTAT VISÉ", txt({ x: M + 0.4, y: 4.6, w: 6.2, h: 0.28, fontSize: 10.5, bold: true, color: SIGNAL, charSpacing: 1.4 }));
  s.addText(p.outcome, txt({ x: M + 0.4, y: 4.95, w: 6.2, h: 0.8, fontSize: 15, color: TEXT, lineSpacing: 21 }));
  await tile(s, p.icon, 8.9, 2.2, 3.0, p.key === "kontrol" ? BRANDC : ACCENT);
  footer(s, p);
  s.addNotes(`Énoncer la promesse en une phrase et s'y tenir : ${p.outcome}`);
}

async function slideFeatures(pres, p) {
  const s = pres.addSlide();
  s.background = { color: PAPER };
  heading(s, "Fonctionnalités", "Ce que fait " + p.name);
  const w = 3.71, h = 2.35;
  for (let i = 0; i < p.features.length; i++) {
    const f = p.features[i];
    const x = M + (i % 3) * (w + 0.35), y = 1.82 + Math.floor(i / 3) * (h + 0.26);
    card(s, x, y, w, h);
    await tile(s, f.i, x + 0.32, y + 0.24, 0.55, i % 2 ? ACCENT : BRANDC);
    s.addText(f.t, txt({ x: x + 0.32, y: y + 0.88, w: w - 0.64, h: 0.48, fontSize: 13, bold: true, color: "FFFFFF", lineSpacing: 18 }));
    s.addText(f.d, txt({ x: x + 0.32, y: y + 1.4, w: w - 0.64, h: 0.85, fontSize: 11, color: MUTED, lineSpacing: 16 }));
  }
  footer(s, p);
  s.addNotes("Ne pas dérouler les six fonctions : en développer deux, celles qui répondent au constat retenu par le client, et laisser la fiche produit pour le reste.");
}

function slideZoomKontrol(pres, p) {
  const s = pres.addSlide();
  s.background = { color: PAPER };
  heading(s, "En pratique", p.zoom.title, p.zoom.intro);
  const w = 2.27;
  p.zoom.items.forEach((it, i) => {
    const x = M + i * (w + 0.16);
    card(s, x, 2.35, w, 2.45);
    s.addText(it.n, txt({ x: x + 0.3, y: 2.6, w: w - 0.6, h: 0.45, fontSize: 26, bold: true, fontFace: HEAD, color: i % 2 ? ACCENT : BRANDC }));
    s.addText(it.t, txt({ x: x + 0.3, y: 3.15, w: w - 0.6, h: 0.32, fontSize: 14, bold: true, color: "FFFFFF" }));
    s.addText(it.d, txt({ x: x + 0.3, y: 3.55, w: w - 0.6, h: 1.0, fontSize: 11, color: MUTED, lineSpacing: 16 }));
  });
  card(s, M, 5.1, 11.83, 1.35, { fill: SURF2 });
  s.addText("Les cinq mesures alimentent une note de 0 à 100 par dossier, agrégée par agence et par segment de clientèle, suivie mois après mois.",
    txt({ x: M + 0.45, y: 5.45, w: 11, h: 0.7, fontSize: 13.5, color: TEXT, lineSpacing: 20 }));
  footer(s, p);
  s.addNotes("Insister sur le caractère défendable : chaque indicateur se recalcule et s'explique. C'est ce qui distingue un score d'une impression.");
}

function slideZoomVigil(pres, p) {
  const s = pres.addSlide();
  s.background = { color: PAPER };
  heading(s, "En pratique", p.zoom.title, p.zoom.intro);
  const w = 5.75;
  card(s, M, 2.35, w, 3.5, { fill: SURF });
  s.addText("AUJOURD'HUI", txt({ x: M + 0.4, y: 2.6, w: w - 0.8, h: 0.28, fontSize: 10.5, bold: true, color: DANGER, charSpacing: 1.4 }));
  s.addText(p.zoom.before.t, txt({ x: M + 0.4, y: 2.92, w: w - 0.8, h: 0.35, fontSize: 16, bold: true, fontFace: HEAD, color: "FFFFFF" }));
  bullets(s, p.zoom.before.items, M + 0.4, 3.45, w - 0.8, 2.2, MUTED, 12.5);
  const x2 = M + w + 0.33;
  card(s, x2, 2.35, w, 3.5, { fill: SURF, line: BRANDC });
  s.addText("AVEC LE MODULE", txt({ x: x2 + 0.4, y: 2.6, w: w - 0.8, h: 0.28, fontSize: 10.5, bold: true, color: SIGNAL, charSpacing: 1.4 }));
  s.addText(p.zoom.after.t, txt({ x: x2 + 0.4, y: 2.92, w: w - 0.8, h: 0.35, fontSize: 16, bold: true, fontFace: HEAD, color: "FFFFFF" }));
  bullets(s, p.zoom.after.items, x2 + 0.4, 3.45, w - 0.8, 2.2, TEXT, 12.5);
  s.addText("Aucune alerte n'est supprimée automatiquement : le moteur réordonne, l'analyste décide, la décision est tracée.",
    txt({ x: M, y: 6.05, w: 11.83, h: 0.4, fontSize: 12.5, color: MUTED }));
  footer(s, p);
  s.addNotes("Le cœur de l'argumentaire Vigil : on ne promet pas moins d'alertes par magie, on promet un ordre de traitement justifiable.");
}

async function slideGains(pres, p) {
  const s = pres.addSlide();
  s.background = { color: PAPER };
  heading(s, "Bénéfices", "Ce que vous y gagnez");
  const w = 3.71;
  for (let i = 0; i < p.gains.length; i++) {
    const g = p.gains[i];
    const x = M + i * (w + 0.35);
    card(s, x, 2.0, w, 3.0);
    await tile(s, g.i, x + 0.35, 2.3, 0.62, i === 1 ? ACCENT : BRANDC);
    s.addText(g.t, txt({ x: x + 0.35, y: 3.1, w: w - 0.7, h: 0.6, fontSize: 15, bold: true, color: "FFFFFF", fontFace: HEAD }));
    s.addText(g.d, txt({ x: x + 0.35, y: 3.75, w: w - 0.7, h: 1.1, fontSize: 11.5, color: MUTED, lineSpacing: 17 }));
  }
  card(s, M, 5.3, 11.83, 1.15, { fill: SURF2 });
  s.addText("Chaque bénéfice se mesure sur des indicateurs convenus avec vous avant le pilote, puis suivis en comité.",
    txt({ x: M + 0.45, y: 5.62, w: 11, h: 0.5, fontSize: 13.5, color: TEXT }));
  footer(s, p);
  s.addNotes("Relier chaque bénéfice à un indicateur mesurable : c'est ce qui transformera le pilote en généralisation.");
}

async function slideAudiences(pres, p) {
  const s = pres.addSlide();
  s.background = { color: PAPER };
  heading(s, "Interlocuteurs", "À qui le module rend service");
  for (let i = 0; i < COMPANY.audiences.length; i++) {
    const a = COMPANY.audiences[i];
    const y = 1.95 + i * 1.24;
    card(s, M, y, 11.83, 1.05);
    await tile(s, a.i, M + 0.35, y + 0.22, 0.6, i % 2 ? ACCENT : BRANDC);
    s.addText(a.r, txt({ x: M + 1.15, y: y + 0.34, w: 3.9, h: 0.38, fontSize: 14, bold: true, color: "FFFFFF" }));
    s.addText(a.d, txt({ x: M + 5.2, y: y + 0.3, w: 6.3, h: 0.5, fontSize: 12, color: MUTED, lineSpacing: 17 }));
  }
  footer(s, p);
  s.addNotes("Adapter l'entrée en matière selon l'interlocuteur présent : le RCCI achète la preuve, le DSI achète l'absence de projet lourd.");
}

async function slideDiffs(pres, p) {
  const s = pres.addSlide();
  s.background = { color: PAPER };
  heading(s, "Positionnement", "Pourquoi Konformix plutôt qu'une plateforme mondiale");
  const w = 5.75, h = 2.25;
  for (let i = 0; i < COMPANY.diffs.length; i++) {
    const d = COMPANY.diffs[i];
    const x = M + (i % 2) * (w + 0.33), y = 2.0 + Math.floor(i / 2) * (h + 0.33);
    card(s, x, y, w, h);
    await tile(s, d.i, x + 0.35, y + 0.32, 0.62, i % 2 ? ACCENT : BRANDC);
    s.addText(d.t, txt({ x: x + 1.15, y: y + 0.32, w: w - 1.5, h: 0.55, fontSize: 15, bold: true, color: "FFFFFF", lineSpacing: 20 }));
    s.addText(d.d, txt({ x: x + 1.15, y: y + 0.95, w: w - 1.5, h: 1.1, fontSize: 12, color: MUTED, lineSpacing: 17 }));
  }
  footer(s, p);
  s.addNotes("Ne pas dénigrer les plateformes internationales : elles conviennent aux groupes avec équipe projet dédiée. Notre terrain, c'est le délai et le coût.");
}

function slideSteps(pres, p) {
  const s = pres.addSlide();
  s.background = { color: PAPER };
  heading(s, "La démarche", "Quatre étapes, un engagement progressif");
  const w = 2.72;
  COMPANY.steps.forEach((st, i) => {
    const x = M + i * (w + 0.32);
    card(s, x, 2.05, w, 3.35, i === 0 ? { line: BRANDC } : {});
    s.addText(st.n, txt({ x: x + 0.32, y: 2.3, w: w - 0.64, h: 0.5, fontSize: 28, bold: true, fontFace: HEAD, color: i === 0 ? BRANDC : ACCENT }));
    s.addText(st.t, txt({ x: x + 0.32, y: 2.88, w: w - 0.64, h: 0.6, fontSize: 14.5, bold: true, color: "FFFFFF" }));
    s.addText(st.d, txt({ x: x + 0.32, y: 3.55, w: w - 0.64, h: 0.28, fontSize: 11, bold: true, color: SIGNAL }));
    s.addText(st.x, txt({ x: x + 0.32, y: 3.95, w: w - 0.64, h: 1.3, fontSize: 11, color: MUTED, lineSpacing: 16 }));
  });
  card(s, M, 5.65, 11.83, 0.85, { fill: SURF2 });
  s.addText("L'étape 1 se conclut par un rapport chiffré qui vous reste acquis, même si vous n'allez pas plus loin.",
    txt({ x: M + 0.45, y: 5.9, w: 11, h: 0.4, fontSize: 13.5, color: TEXT }));
  footer(s, p);
  s.addNotes("Le diagnostic est l'objet de la vente du jour. Ne pas chercher à vendre la généralisation en première visite.");
}

async function slideFaq(pres, p) {
  const s = pres.addSlide();
  s.background = { color: PAPER };
  heading(s, "Objections", "Les questions qui reviennent en comité");
  for (let i = 0; i < p.faq.length; i++) {
    const f = FAQ[p.faq[i]];
    const y = 1.95 + i * 1.62;
    card(s, M, y, 11.83, 1.42);
    await tile(s, "TbSearch", M + 0.35, y + 0.4, 0.6, i % 2 ? ACCENT : BRANDC);
    s.addText(f.q, txt({ x: M + 1.15, y: y + 0.22, w: 10.3, h: 0.34, fontSize: 14.5, bold: true, color: "FFFFFF" }));
    s.addText(f.a, txt({ x: M + 1.15, y: y + 0.62, w: 10.3, h: 0.7, fontSize: 12, color: MUTED, lineSpacing: 18 }));
  }
  footer(s, p);
  s.addNotes("Trois objections reviennent systématiquement. Les traiter avant qu'elles ne soient posées met le client en confiance.");
}

async function slideClosing(pres, p) {
  const s = pres.addSlide();
  s.background = { color: INK };
  glow(s, 7.6, -1.2, 7.0, 6.0, ACCENT, 90);
  glow(s, -1.9, 4.2, 5.6, 4.4, BRANDC, 93);
  s.addImage({ data: await logoData(), x: M, y: 1.1, w: 0.8, h: 0.8 });
  s.addText("Commençons par mesurer, pas par vendre.", txt({ x: M, y: 2.25, w: 7.3, h: 1.6, fontSize: 34, bold: true, fontFace: HEAD, color: "FFFFFF", lineSpacing: 40 }));
  s.addText(p.closing, txt({ x: M, y: 4.1, w: 7.2, h: 1.4, fontSize: 14.5, color: MUTED, lineSpacing: 22 }));
  card(s, 8.6, 2.25, 3.98, 3.6, { fill: SURF });
  s.addText("Nous contacter", txt({ x: 8.95, y: 2.5, w: 3.3, h: 0.35, fontSize: 15, bold: true, fontFace: HEAD, color: "FFFFFF" }));
  const rows = [
    { i: "TbMail", t: BRAND.email },
    { i: "TbPhone", t: BRAND.phone },
    { i: "TbWorld", t: BRAND.domain },
    { i: "TbMapPin", t: BRAND.city },
  ];
  let y = 3.05;
  for (const r of rows) {
    await tile(s, r.i, 8.95, y, 0.44, BRANDC);
    s.addText(r.t, txt({ x: 9.6, y: y + 0.06, w: 2.9, h: 0.32, fontSize: 12, color: TEXT }));
    y += 0.66;
  }
  s.addText(BRAND.legal + " · " + BRAND.city, txt({ x: M, y: 6.6, w: 11.83, h: 0.3, fontSize: 10, color: DIM }));
  s.addNotes("Conclure sur le diagnostic à deux semaines : engagement faible pour le client, chiffres en main pour la suite. Repartir avec une date d'extraction.");
}

// ---------------------------------------------------------------- montage
async function build(key, outDir) {
  const p = PRODUCTS[key];
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.author = BRAND.legal;
  pres.company = BRAND.legal;
  pres.title = p.name + " — présentation commerciale";
  pres.subject = p.kicker;

  await slideCover(pres, p);
  await slideCompany(pres, p);
  slideContext(pres, p);
  slideChart(pres, p);
  await slidePains(pres, p);
  await slidePromise(pres, p);
  await slideFeatures(pres, p);
  if (key === "kontrol") slideZoomKontrol(pres, p); else slideZoomVigil(pres, p);
  await slideGains(pres, p);
  await slideAudiences(pres, p);
  await slideDiffs(pres, p);
  slideSteps(pres, p);
  await slideFaq(pres, p);
  await slideClosing(pres, p);

  const out = path.join(outDir, "konformix-" + key + ".pptx");
  await pres.writeFile({ fileName: out });
  console.log("écrit :", out);
}

(async () => {
  const outDir = process.argv[2] || ".";
  await build("kontrol", outDir);
  await build("vigil", outDir);
})();
