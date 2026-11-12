// ---- Core calculations (ported from the Cookiepocalypse spreadsheet) ----
const key = s => String(s ?? '').trim().toLowerCase();
const num = v => (typeof v === 'number' && isFinite(v)) ? v : (v === '' || v == null ? null : (isFinite(+v) ? +v : null));

function totalUnits(state) {
  // People!C13 = SUM(C2:C12)
  return state.people.reduce((a, p) => a + (num(p.units) || 0), 0);
}
function findRecipe(state, name) {
  const k = key(name);
  return state.recipes.find(r => key(r.name) === k) || null;
}
function batchesFor(state, item, units) {
  // 'Recipe List'!A = CEILING(CookiesPerUnit * People!C13 / #OfCookies, 1)
  const r = findRecipe(state, item.recipe);
  const per = r ? num(r.cookiesPerBatch) : null;
  const cpu = num(item.cookiesPerUnit);
  if (!per || cpu == null) return null;
  return Math.ceil(cpu * units / per - 1e-9);
}
function gramFor(state, ing) {
  // Recipe grams column: entered value; if blank, fall back to Gram Conversions (amount × grams per unit)
  const g = num(ing.grams);
  if (g != null && (g > 0 || !num(ing.amount))) return { grams: g, derived: false };
  const c = state.gramConversions.find(c => key(c.ingredient) === key(ing.name) && key(c.unit) === key(ing.unit));
  if (c && num(c.grams) != null && num(ing.amount) != null) return { grams: num(ing.amount) * num(c.grams), derived: true };
  return { grams: null, derived: false };
}
function planRows(state) {
  const units = totalUnits(state);
  return state.plan.map(item => {
    const r = findRecipe(state, item.recipe);
    const batches = batchesFor(state, item, units);
    const bm = r ? num(r.bakeMinutes) : null;
    return {
      item, recipe: r, batches,
      cookies: (batches != null && r) ? batches * num(r.cookiesPerBatch) : null,
      // 'Total Bake Time (hr)' = BakeTimePerBatch * batches / 60
      bakeHours: (bm != null && batches != null) ? bm * batches / 60 : null,
    };
  });
}
function shoppingList(state, opts = {}) {
  // Shopping List: unique (Name, Unit) across selected recipes; Amount = SUM of scaled amounts;
  // Bulk Unit / Bulk Amount from Bulk Conversions (Amount / Conversion(A/B)).
  // Extras: substitutions (buy one ingredient as others, split by weight) and combining rows that share a bulk unit.
  const subsOn = opts.substitutions !== false, mergeOn = opts.merge !== false;
  const map = new Map();
  const add = (name, unit, amount, grams, recipeLabel) => {
    const k = key(name) + '|' + key(unit);
    let e = map.get(k);
    if (!e) { e = { key: k, name: String(name).trim(), unit: String(unit || '').trim(), amount: 0, grams: 0, gramsMissing: false, recipes: [] }; map.set(k, e); }
    e.amount += amount;
    if (grams == null) e.gramsMissing = true; else e.grams += grams;
    if (!e.recipes.includes(recipeLabel)) e.recipes.push(recipeLabel);
  };
  for (const row of planRows(state)) {
    if (!row.recipe || row.batches == null) continue;
    for (const ing of row.recipe.ingredients) {
      if (!String(ing.name || '').trim()) continue;
      const g = gramFor(state, ing);
      const amount = (num(ing.amount) || 0) * row.batches;
      const subs = subsOn ? (state.substitutions || []).filter(x => key(x.ingredient) === key(ing.name) && num(x.share)) : [];
      if (subs.length && g.grams != null) {
        for (const x of subs) { const sg = g.grams * row.batches * num(x.share); add(x.buyAs, 'Grams', sg, sg, row.recipe.name + ' (as ' + ing.name.trim() + ')'); }
        continue;
      }
      const ui = unitInfo(ing.unit);
      if (opts.byWeight !== false && g.grams != null && ui && ui.kind !== 'butterstick' && !(ui.kind === 'vol' && key(ing.unit).startsWith('m'))) {
        add(ing.name, 'Grams', g.grams * row.batches, g.grams * row.batches, row.recipe.name);   // weights are the source of truth
      } else add(ing.name, ing.unit, amount, g.grams == null ? null : g.grams * row.batches, row.recipe.name);
    }
  }
  let out = [...map.values()].filter(e => e.amount > 0);
  for (const e of out) {
    const b = state.bulkConversions.find(b => key(b.ingredient) === key(e.name) && key(b.unit) === key(e.unit));
    if (b && num(b.perBulk)) { e.bulkUnit = b.bulkUnit; e.bulkAmount = e.amount / num(b.perBulk); }
    else if (opts.defaultBulk !== false && key(e.unit) === 'grams') { const lb = e.amount >= 453.592; e.bulkUnit = lb ? 'Pounds' : 'Ounces'; e.bulkAmount = e.amount / (lb ? 453.592 : 28.3495); }
    else if (opts.defaultBulk !== false && key(e.unit) === 'milliliters') { e.bulkUnit = 'Fluid Ounces'; e.bulkAmount = e.amount / 29.5735; }
    e.parts = [{ amount: e.amount, unit: e.unit }];
  }
  if (mergeOn) {
    const merged = new Map(), rest = [];
    for (const e of out) {
      if (!e.bulkUnit) { rest.push(e); continue; }
      const k = key(e.name) + '|bulk:' + key(e.bulkUnit);
      const m = merged.get(k);
      if (!m) { merged.set(k, { ...e, key: k, parts: [...e.parts], recipes: [...e.recipes] }); continue; }
      m.parts.push(...e.parts); m.bulkAmount += e.bulkAmount; m.grams += e.grams; m.gramsMissing = m.gramsMissing || e.gramsMissing;
      for (const r of e.recipes) if (!m.recipes.includes(r)) m.recipes.push(r);
    }
    for (const m of merged.values()) if (m.parts.length > 1) { m.amount = null; m.unit = ''; }
    // single-row bulk entries keep their original name|unit key so existing checkmarks survive
    for (const [k, m] of merged) if (m.parts.length === 1) m.key = key(m.name) + '|' + key(m.parts[0].unit);
    out = [...rest, ...merged.values()];
  }
  for (const e of out) e.purchased = !!(state.purchased || {})[e.key];
  out.sort((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: 'base' }) || String(a.unit).localeCompare(String(b.unit)));
  return out;
}

// Weights are the source of truth; the volume/count measure is derived from grams where a conversion exists.
function measureFor(state, ing, mult = 1) {
  const g = gramFor(state, ing).grams;
  const ui = unitInfo(ing.unit);
  if (g != null && ui && ui.kind !== 'butterstick') {
    const gp = gramsPerUnit(state, ing.name, ing.unit);
    if (gp && gp.g) return { amount: g * mult / gp.g, unit: ing.unit };
  }
  return { amount: (num(ing.amount) || 0) * mult, unit: ing.unit };
}
// Keep amount and grams in step after an edit. which = 'grams' (weight edited) or 'measure' (amount/unit edited).
function syncIngredient(state, ing, which) {
  const ui = unitInfo(ing.unit);
  if (ui && ui.kind === 'wt') { if (which === 'grams' && num(ing.grams) != null) ing.amount = ing.grams / ui.f; else ing.grams = (num(ing.amount) || 0) * ui.f; return; }
  const gp = gramsPerUnit(state, ing.name, ing.unit);
  if (!gp || !gp.g) return;
  if (which === 'grams' && num(ing.grams) != null) { if (!ui || ui.kind === 'vol') ing.amount = ing.grams / gp.g; }
  else ing.grams = Math.round((num(ing.amount) || 0) * gp.g * 100) / 100;
}

// Salt: recipes assume table salt by volume; show the kosher-salt equivalent for the baker's salt.
function kosherTsp(state, ing, mult = 1) {
  const kg = num(state.kosherSaltGPerTsp);
  if (!kg || key(ing.name) !== 'salt') return null;
  const ui = unitInfo(ing.unit);
  if (!ui || ui.kind !== 'vol') return null;
  const g = gramFor(state, ing).grams;
  return g == null ? null : g * mult / kg;
}

// Apply a data patch (conversions, renames, recipe ingredient edits, settings). Idempotent per id.
function applyPatch(state, p) {
  if (!p || (state.appliedPatches || []).includes(p.id)) return false;
  const sameIng = (a, b) => key(a.ingredient) === key(b.ingredient) && key(a.unit) === key(b.unit);
  for (const rn of p.renames || []) {
    const from = new Set(rn.from.map(key));
    const cf = rn.field === 'name' ? 'ingredient' : 'unit';
    for (const r of state.recipes) for (const i of r.ingredients) if (from.has(key(i[rn.field]))) i[rn.field] = rn.to;
    for (const c of [...state.gramConversions, ...state.bulkConversions]) if (from.has(key(c[cf]))) c[cf] = rn.to;
  }
  for (const ed of p.ingredientEdits || []) {
    const r = state.recipes.find(x => key(x.name) === key(ed.recipe)); if (!r) continue;
    const out = [];
    for (const i of r.ingredients) {
      if (key(i.name) === key(ed.find.name) && (!ed.find.unit || key(i.unit) === key(ed.find.unit)) && (!ed.find.phase || key(i.phase || '').includes(key(ed.find.phase)))) {
        for (const rw of ed.replaceWith) { const n = { ...rw }; if (!n.phase && i.phase) n.phase = i.phase; out.push(n); }
      } else out.push(i);
    }
    r.ingredients = out;
  }
  const upsert = (arr, row, extraMatch) => {
    const idx = []; arr.forEach((c, n) => { if (sameIng(c, row) && (!extraMatch || extraMatch(c))) idx.push(n); });
    if (!idx.length) { arr.push({ ...row }); return; }
    Object.assign(arr[idx[0]], row);
    for (const n of idx.slice(1).reverse()) arr.splice(n, 1);
  };
  for (const g of p.gram || []) upsert(state.gramConversions, g);
  for (const b of p.bulk || []) upsert(state.bulkConversions, b);
  if (p.recalcBulk) {
    for (const b of state.bulkConversions) {
      const ua = unitInfo(b.unit), ub = unitInfo(b.bulkUnit);
      if (!ua || !ub || ub.kind !== 'wt') continue;
      if (ua.kind === 'wt') b.perBulk = Math.round(ub.f / ua.f * 10000) / 10000;
      else if (ua.kind === 'vol') { const gp = gramsPerUnit(state, b.ingredient, b.unit); if (gp && gp.g) b.perBulk = Math.round(ub.f / gp.g * 10000) / 10000; }
    }
  }
  if (p.syncWeights) {
    for (const r of state.recipes) for (const i of r.ingredients) {
      const ui = unitInfo(i.unit);
      const typed = num(i.grams) != null && (num(i.grams) > 0 || !num(i.amount));
      if (ui && ui.kind === 'wt') { if (typed) i.amount = i.grams / ui.f; else i.grams = (num(i.amount) || 0) * ui.f; continue; }
      const gp = gramsPerUnit(state, i.name, i.unit);
      if (!gp || !gp.g) { if (!typed) delete i.grams; continue; }
      if (typed) { if (ui && ui.kind === 'vol') i.amount = Math.round(i.grams / gp.g * 10000) / 10000; }
      else i.grams = Math.round((num(i.amount) || 0) * gp.g * 100) / 100;
    }
  }
  for (const sp of p.splits || []) {
    for (const r of state.recipes) {
      const out = [];
      for (const i of r.ingredients) {
        if (key(i.name) !== key(sp.name) || num(i.grams) == null) { out.push(i); continue; }
        for (const part of sp.into) {
          const g = Math.round(i.grams * part.share * 100) / 100;
          const ex = out.find(o => key(o.name) === key(part.name) && key(o.unit) === key(i.unit) && (o.phase || '') === (i.phase || ''));
          const gp = gramsPerUnit(state, part.name, i.unit), ui = unitInfo(i.unit);
          const toAmt = grams => ui && ui.kind === 'wt' ? grams / ui.f : gp ? Math.round(grams / gp.g * 10000) / 10000 : grams;
          if (ex && num(ex.grams) != null) { ex.grams = Math.round((ex.grams + g) * 100) / 100; ex.amount = toAmt(ex.grams); }
          else { const n = { name: part.name, amount: toAmt(g), unit: i.unit, grams: g }; if (i.phase) n.phase = i.phase; out.push(n); }
        }
      }
      // merge same ingredient + unit + phase rows created by the split
      const merged = [];
      for (const i of out) {
        const ex = merged.find(o => key(o.name) === key(i.name) && key(o.unit) === key(i.unit) && (o.phase || '') === (i.phase || '') && num(o.grams) != null && num(i.grams) != null);
        if (ex && sp.into.some(x => key(x.name) === key(i.name))) { ex.grams = Math.round((ex.grams + i.grams) * 100) / 100; ex.amount = (num(ex.amount) || 0) + (num(i.amount) || 0); }
        else merged.push(i);
      }
      r.ingredients = merged;
    }
  }
  for (const rs of p.removeSubstitutions || []) state.substitutions = (state.substitutions || []).filter(x => key(x.ingredient) !== key(rs));
  for (const nt of p.notes || []) { const r = state.recipes.find(x => key(x.name) === key(nt.recipe)); if (r) r.notes = nt.notes; }
  for (const t of p.times || []) { const r = state.recipes.find(x => key(x.name) === key(t.recipe)); if (r) for (const f of ['prepMinutes', 'restMinutes', 'bakeMinutes']) if (t[f] != null && (r[f] == null || t.overwrite)) r[f] = t[f]; }
  for (const mr of p.methodReplace || []) for (const r of state.recipes) if (r.method) r.method = r.method.split(mr.from).join(mr.to);
  for (const mt of p.methods || []) { const r = state.recipes.find(x => key(x.name) === key(mt.recipe)); if (r) { if (!r.method || mt.overwrite) r.method = mt.method; if (mt.notes != null) r.notes = mt.notes; } }
  if (p.setPlan) {
    const prev = new Map(state.plan.map(x => [key(x.recipe), x]));
    state.plan = p.setPlan.filter(n => state.recipes.some(r => key(r.name) === key(n))).map(n => prev.get(key(n)) || { recipe: n, cookiesPerUnit: 6, bakeDay: '' });
  }
  if (p.removeRecipes) {
    const inPlan = new Set(state.plan.map(x => key(x.recipe)));
    const drop = new Set(p.removeRecipes.map(key));
    state.recipes = state.recipes.filter(r => !drop.has(key(r.name)) || inPlan.has(key(r.name)));
  }
  if (p.removeEmptyRecipes) {
    const inPlan = new Set(state.plan.map(x => key(x.recipe)));
    state.recipes = state.recipes.filter(r => r.ingredients.length || inPlan.has(key(r.name)));
  }
  if (p.pruneConversions) {
    const used = new Set(state.recipes.flatMap(r => r.ingredients.map(i => key(i.name))));
    state.gramConversions = state.gramConversions.filter(c => used.has(key(c.ingredient)));
    state.bulkConversions = state.bulkConversions.filter(c => used.has(key(c.ingredient)));
  }
  for (const x of p.substitutions || []) {
    state.substitutions = state.substitutions || [];
    if (!state.substitutions.some(y => key(y.ingredient) === key(x.ingredient) && key(y.buyAs) === key(x.buyAs))) state.substitutions.push({ ...x });
  }
  if (p.settings) Object.assign(state, p.settings);
  // Replace a baking-plan session's task list, keeping the checkmark on any task whose text is unchanged
  for (const se of p.sessionTasks || []) {
    const ss = (state.sessions || []).find(x => (se.n != null && x.n === se.n) || (se.label && x.label === se.label)); if (!ss) continue;
    const was = new Map((ss.tasks || []).map(t => typeof t === 'string' ? [t, false] : [t.text, !!t.done]));
    ss.tasks = se.tasks.map(t => ({ text: t, done: was.get(t) || false }));
    if (se.title) ss.title = se.title;
    if (se.hours) ss.hours = se.hours;
  }
  state.appliedPatches = [...(state.appliedPatches || []), p.id];
  return true;
}

// Times per batch: total = prep + rest + bake (null when none are known)
function totalMinutes(r) {
  const parts = [r.prepMinutes, r.restMinutes, r.bakeMinutes].map(num).filter(v => v != null);
  return parts.length ? parts.reduce((a, b) => a + b, 0) : null;
}
function fmtMinutes(m) {
  m = num(m); if (m == null) return '';
  const h = Math.floor(m / 60), mm = Math.round(m - h * 60);
  return h ? (mm ? `${h} h ${mm} min` : `${h} h`) : `${mm} min`;
}

// ---- Method (Cooking for Engineers table) ----
// Text format, one step per line, in cooking order:
//   prep: Heat oven to 350°F; line sheets
//   label = action text <- input + input + ...
// Inputs are earlier step labels or ingredient names (add "@word" to pick the ingredient whose phase contains that word).
// The last step is the finished dish. Lines starting with # are comments.
function parseMethod(recipe, text) {
  const out = { prep: [], steps: [], root: null, warnings: [], rows: [], unused: [] };
  const used = new Set();
  const labels = new Map();
  const findIng = (ref) => {
    let [name, ph] = ref.split('@').map(x => x.trim());
    const cands = recipe.ingredients.map((i, k) => ({ i, k })).filter(({ i, k }) => !used.has(k) && key(i.name) === key(name) && (!ph || key(i.phase || '').includes(key(ph))));
    if (!cands.length) return null;
    used.add(cands[0].k);
    return { kind: 'ing', k: cands[0].k, ing: cands[0].i };
  };
  const lines = String(text || '').split(/\r?\n/);
  lines.forEach((raw, ln) => {
    const line = raw.trim();
    if (!line || line.startsWith('#')) return;
    if (/^prep\s*:/i.test(line)) { out.prep.push(line.replace(/^prep\s*:\s*/i, '')); return; }
    const arrow = line.indexOf('<-');
    if (arrow < 0) { out.warnings.push(`Line ${ln + 1}: needs "<-" followed by what this step uses.`); return; }
    let head = line.slice(0, arrow).trim(), label = null;
    const m = head.match(/^([A-Za-z][\w-]*)\s*=\s*(.+)$/);
    if (m) { label = m[1]; head = m[2].trim(); }
    const inputs = [];
    for (const refRaw of line.slice(arrow + 2).split(/\s\+\s/)) {
      const ref = refRaw.trim(); if (!ref) continue;
      if (labels.has(key(ref))) {
        const st = labels.get(key(ref));
        if (st.consumed) out.warnings.push(`Line ${ln + 1}: "${ref}" is already used by another step.`);
        st.consumed = true; inputs.push(st); continue;
      }
      const ing = findIng(ref);
      if (ing) inputs.push(ing);
      else { inputs.push({ kind: 'extra', text: ref }); out.warnings.push(`Line ${ln + 1}: "${ref}" isn't an ingredient (or is already used) — shown as a plain row.`); }
    }
    if (!inputs.length) { out.warnings.push(`Line ${ln + 1}: list what this step uses after "<-".`); return; }
    const step = { kind: 'step', text: head, inputs, label, consumed: false };
    out.steps.push(step);
    if (label) labels.set(key(label), step);
  });
  if (!out.steps.length) return out;
  out.root = out.steps[out.steps.length - 1];
  for (const st of out.steps.slice(0, -1)) if (!st.consumed) out.warnings.push(`Step "${st.text}" isn't used by a later step${st.label ? '' : ' (give it a label, e.g. "dough = ...")'}.`);
  // layout: rows = leaves in order, column = height
  const walk = (n) => {
    if (n.kind !== 'step') { n.h = 0; n.r0 = out.rows.length; out.rows.push(n); n.r1 = out.rows.length; return; }
    n.r0 = out.rows.length; let h = 0;
    for (const c of n.inputs) { walk(c); h = Math.max(h, c.h); }
    n.h = h + 1; n.r1 = out.rows.length;
  };
  walk(out.root);
  out.cols = out.root.h;
  out.unused = recipe.ingredients.filter((_, k) => !used.has(k));
  if (out.unused.length) out.warnings.push('Not used in the method: ' + out.unused.map(i => i.name + (i.phase ? ' (' + i.phase + ')' : '')).join(', '));
  return out;
}

// ---- Import / export helpers ----
const CSV_COLS = ['Recipe', 'Ingredient', 'Amount', 'Unit', 'Grams', 'Phase', 'Book', 'Book URL', 'Page', 'Cookies Per Batch', 'Refrigerate', 'Oven Temp', 'Bake Minutes Per Batch', 'Notes', 'Method', 'Prep Minutes', 'Rest Minutes'];
function csvEsc(v) { v = v == null ? '' : String(v); return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
function recipesToCSV(recipes) {
  const lines = [CSV_COLS.join(',')];
  for (const r of recipes) {
    const meta = [r.book, r.bookUrl, r.page, r.cookiesPerBatch, r.refrigerate, r.ovenTemp, r.bakeMinutes, r.notes, r.method, r.prepMinutes, r.restMinutes];
    const ings = r.ingredients.length ? r.ingredients : [{}];
    ings.forEach((i, n) => lines.push([r.name, i.name, i.amount, i.unit, i.grams, i.phase, ...(n === 0 ? meta : meta.map(() => ''))].map(csvEsc).join(',')));
  }
  return lines.join('\n');
}
function parseCSV(text) {
  const rows = []; let row = [], f = '', q = false;
  text = text.replace(/^﻿/, '');
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
    else if (c === '"') q = true;
    else if (c === ',' || c === '\t') { row.push(f); f = ''; }
    else if (c === '\n' || c === '\r') { if (c === '\r' && text[i + 1] === '\n') i++; row.push(f); rows.push(row); row = []; f = ''; }
    else f += c;
  }
  if (f !== '' || row.length) { row.push(f); rows.push(row); }
  return rows.filter(r => r.some(x => String(x).trim() !== ''));
}
function recipesFromCSV(text) {
  const rows = parseCSV(text);
  if (!rows.length) throw new Error('The CSV is empty.');
  const hdr = rows[0].map(h => key(h).replace(/[^a-z]/g, ''));
  const idx = n => hdr.indexOf(n);
  const col = { recipe: idx('recipe'), name: idx('ingredient'), amount: idx('amount'), unit: idx('unit'), grams: idx('grams'), phase: idx('phase'),
    book: idx('book'), bookUrl: idx('bookurl'), page: idx('page'), cookiesPerBatch: idx('cookiesperbatch'), refrigerate: idx('refrigerate'), ovenTemp: idx('oventemp'), bakeMinutes: idx('bakeminutesperbatch'), notes: idx('notes'), method: idx('method'), prepMinutes: idx('prepminutes'), restMinutes: idx('restminutes') };
  if (col.recipe < 0 || col.name < 0) throw new Error('The CSV needs at least "Recipe" and "Ingredient" columns. Export a recipe as CSV to see the expected layout.');
  const byName = new Map();
  for (const r of rows.slice(1)) {
    const get = k => col[k] >= 0 ? String(r[col[k]] ?? '').trim() : '';
    const rn = get('recipe'); if (!rn) continue;
    let rec = byName.get(key(rn));
    if (!rec) { rec = { name: rn, book: '', bookUrl: '', page: '', cookiesPerBatch: null, refrigerate: '', ovenTemp: '', bakeMinutes: null, prepMinutes: null, restMinutes: null, notes: '', method: '', ingredients: [] }; byName.set(key(rn), rec); }
    for (const k of ['book', 'bookUrl', 'page', 'refrigerate', 'ovenTemp', 'notes', 'method']) if (get(k) && !rec[k]) rec[k] = get(k);
    for (const k of ['cookiesPerBatch', 'bakeMinutes', 'prepMinutes', 'restMinutes']) if (get(k) && rec[k] == null) rec[k] = num(get(k));
    if (get('name')) {
      const ing = { name: get('name'), amount: num(get('amount')) ?? 0, unit: get('unit') };
      if (num(get('grams')) != null && get('grams') !== '') ing.grams = num(get('grams'));
      if (get('phase')) ing.phase = get('phase');
      rec.ingredients.push(ing);
    }
  }
  return [...byName.values()];
}
function normalizeRecipe(r) {
  if (!r || typeof r !== 'object' || !String(r.name || '').trim()) throw new Error('Each recipe needs a "name".');
  return {
    name: String(r.name).trim(), book: String(r.book ?? ''), bookUrl: String(r.bookUrl ?? ''), page: String(r.page ?? ''),
    cookiesPerBatch: num(r.cookiesPerBatch), refrigerate: String(r.refrigerate ?? ''), ovenTemp: String(r.ovenTemp ?? ''), bakeMinutes: num(r.bakeMinutes),
    prepMinutes: num(r.prepMinutes), restMinutes: num(r.restMinutes),
    notes: String(r.notes ?? ''),
    method: String(r.method ?? ''),
    ingredients: (Array.isArray(r.ingredients) ? r.ingredients : []).filter(i => i && String(i.name || '').trim()).map(i => {
      const o = { name: String(i.name).trim(), amount: num(i.amount) ?? 0, unit: String(i.unit ?? '').trim() };
      if (num(i.grams) != null) o.grams = num(i.grams);
      if (i.phase) o.phase = String(i.phase);
      return o;
    }),
  };
}
function normalizeState(s) {
  const arr = v => Array.isArray(v) ? v : [];
  return {
    version: 1,
    seedVersion: num(s.seedVersion) || 1,
    title: String(s.title || 'Cookie Plan'),
    recipes: arr(s.recipes).map(normalizeRecipe),
    plan: arr(s.plan).filter(p => p && p.recipe).map(p => ({ recipe: String(p.recipe), cookiesPerUnit: num(p.cookiesPerUnit), bakeDay: p.bakeDay == null ? '' : p.bakeDay })),
    gramConversions: arr(s.gramConversions).filter(c => c && c.ingredient).map(c => ({ ingredient: String(c.ingredient), unit: String(c.unit ?? ''), grams: num(c.grams) })),
    bulkConversions: arr(s.bulkConversions).filter(c => c && c.ingredient).map(c => ({ ingredient: String(c.ingredient), unit: String(c.unit ?? ''), bulkUnit: String(c.bulkUnit ?? ''), perBulk: num(c.perBulk) })),
    people: arr(s.people).filter(p => p && p.name != null).map(p => ({ name: String(p.name), boxSize: String(p.boxSize ?? ''), units: num(p.units) ?? 0 })),
    substitutions: arr(s.substitutions).filter(x => x && x.ingredient).map(x => ({ ingredient: String(x.ingredient), buyAs: String(x.buyAs ?? ''), share: num(x.share) })),
    kosherSaltGPerTsp: num(s.kosherSaltGPerTsp),
    // Baking plan: dated sessions with checkable tasks. n = session number (matches a plan row's bake day); null for order/shop/buffer days
    sessions: arr(s.sessions).filter(x => x && (x.title || x.date)).map(x => ({
      n: num(x.n), label: String(x.label ?? ''), date: String(x.date ?? ''), end: String(x.end ?? ''), hours: String(x.hours ?? ''),
      title: String(x.title ?? ''), buy: String(x.buy ?? ''),
      tasks: arr(x.tasks).map(t => typeof t === 'string' ? { text: t, done: false } : { text: String(t?.text ?? ''), done: !!t?.done }).filter(t => t.text),
    })),
    appliedPatches: arr(s.appliedPatches).map(String),
    ignoredChecks: (s.ignoredChecks && typeof s.ignoredChecks === 'object') ? { ...s.ignoredChecks } : {},
    purchased: (s.purchased && typeof s.purchased === 'object') ? Object.fromEntries(Object.entries(s.purchased).map(([k, v]) => [key(k.split('|')[0]) + '|' + key(k.split('|')[1]), !!v])) : {},
  };
}
if (typeof module !== 'undefined') module.exports = { totalMinutes, fmtMinutes, totalUnits, planRows, shoppingList, kosherTsp, applyPatch, measureFor, syncIngredient, parseMethod, gramFor, recipesToCSV, recipesFromCSV, normalizeState, normalizeRecipe, key };

// ---- Conversion checks ----
const UNIT = (() => {
  const m = {};
  const add = (names, kind, f) => names.forEach(n => m[n] = { kind, f });
  add(['teaspoon', 'teaspoons', 'tsp', 'tsps', 't'], 'vol', 1);
  add(['tablespoon', 'tablespoons', 'tbsp', 'tbsps', 'tbs', 'tb'], 'vol', 3);
  add(['cup', 'cups', 'c'], 'vol', 48);
  add(['pint', 'pints'], 'vol', 96);
  add(['quart', 'quarts'], 'vol', 192);
  add(['ml', 'milliliter', 'milliliters'], 'vol', 1 / 4.92892);
  add(['gram', 'grams', 'g'], 'wt', 1);
  add(['kilogram', 'kilograms', 'kg'], 'wt', 1000);
  add(['ounce', 'ounces', 'oz'], 'wt', 28.3495);
  add(['pound', 'pounds', 'lb', 'lbs'], 'wt', 453.592);
  add(['stick', 'sticks'], 'butterstick', 1);
  return m;
})();
const unitInfo = u => UNIT[key(u)] || null;
const singular = s => key(s).replace(/(ies)$/, 'y').replace(/(es)$/, (x, _, i, str) => /(ch|sh|x|s|z|o)es$/.test(str) ? '' : 'e').replace(/s$/, '');
const near = (a, b, tol) => Math.abs(a - b) <= tol * Math.max(Math.abs(a), Math.abs(b));

// grams per 1 of `unit` for an ingredient, from the Gram Conversions table (direct or via unit math)
function gramsPerUnit(state, name, unit) {
  const ui = unitInfo(unit);
  if (ui && ui.kind === 'wt') return { g: ui.f, how: 'weight unit' };
  const rows = state.gramConversions.filter(c => key(c.ingredient) === key(name) && num(c.grams) != null);
  const direct = rows.find(c => key(c.unit) === key(unit));
  if (direct) return { g: num(direct.grams), how: 'table' };
  if (ui && ui.kind === 'vol') {
    const v = rows.find(c => unitInfo(c.unit)?.kind === 'vol');
    if (v) return { g: num(v.grams) / unitInfo(v.unit).f * ui.f, how: `derived from ${v.unit}` };
  }
  return null;
}

function conversionChecks(state, tol = 0.05) {
  const issues = [];
  const planned = new Set(state.plan.map(p => key(p.recipe)));
  // 1. Ingredient coverage (every name+unit used in a recipe)
  const used = new Map();
  for (const r of state.recipes) for (const i of r.ingredients) {
    const k = key(i.name) + '|' + key(i.unit);
    let e = used.get(k);
    if (!e) { e = { name: i.name, unit: i.unit, recipes: new Set(), planned: false }; used.set(k, e); }
    e.recipes.add(r.name); if (planned.has(key(r.name))) e.planned = true;
  }
  const coverage = [...used.values()].map(e => {
    const gp = gramsPerUnit(state, e.name, e.unit);
    const bulk = state.bulkConversions.find(b => key(b.ingredient) === key(e.name) && key(b.unit) === key(e.unit));
    return { ...e, recipes: [...e.recipes], grams: gp, bulk: bulk || null };
  }).sort((a, b) => (b.planned - a.planned) || a.name.localeCompare(b.name));

  // 2. (Weights typed into recipes are the source of truth, so they are not compared against the table.)

  // 3. Gram Conversions table: duplicates & inconsistent units for one ingredient
  const byIng = new Map();
  state.gramConversions.forEach((c, idx) => { const k = key(c.ingredient); if (!byIng.has(k)) byIng.set(k, []); byIng.get(k).push({ ...c, idx }); });
  for (const rows of byIng.values()) {
    for (let x = 0; x < rows.length; x++) for (let y = x + 1; y < rows.length; y++) {
      const A = rows[x], B = rows[y];
      if (key(A.unit) === key(B.unit)) {
        if (!near(num(A.grams), num(B.grams), 0.001)) issues.push({ type: 'gram-dup', severity: 'high', title: `${A.ingredient} has two gram values per ${A.unit}`,
          detail: `${fmt(A.grams)} g and ${fmt(B.grams)} g. Only the first one is used. Keep the right one.`,
          choices: [{ label: `Keep ${fmt(A.grams)} g`, fix: { kind: 'dropGram', ingredient: B.ingredient, unit: B.unit, grams: num(B.grams) } },
                    { label: `Keep ${fmt(B.grams)} g`, fix: { kind: 'dropGram', ingredient: A.ingredient, unit: A.unit, grams: num(A.grams) } }] });
        continue;
      }
      const ua = unitInfo(A.unit), ub = unitInfo(B.unit);
      const metric = u => key(u).startsWith('m');   // metric ml use true density; cup weights follow King Arthur's convention
      if (ua && ub && ua.kind === 'vol' && ub.kind === 'vol' && metric(A.unit) === metric(B.unit)) {
        const ga = num(A.grams) / ua.f, gb = num(B.grams) / ub.f;
        if (!near(ga, gb, tol)) issues.push({ type: 'gram-units', severity: 'med', title: `${A.ingredient}: ${A.unit} and ${B.unit} disagree`,
          detail: `${fmt(A.grams)} g per ${A.unit} implies ${fmt(ga * ub.f)} g per ${B.unit}, but the table says ${fmt(B.grams)} g.` });
      }
    }
  }

  // 4. Bulk Conversions: compare "A per B" against what grams/unit math implies
  for (const b of state.bulkConversions) {
    const per = num(b.perBulk); if (!per) { issues.push({ type: 'bulk', severity: 'med', title: `${b.ingredient}: missing bulk factor`, detail: `No number in Conversion (A/B) for ${b.unit} → ${b.bulkUnit}.` }); continue; }
    const ua = unitInfo(b.unit), ub = unitInfo(b.bulkUnit);
    let expect = null, how = '';
    if (key(b.unit) === key(b.bulkUnit)) { expect = 1; how = 'same unit'; }
    else if (ua && ub && ua.kind === ub.kind && ua.kind !== 'butterstick') { expect = ub.f / ua.f; how = 'unit math'; }
    else if (ub && ub.kind === 'butterstick' && key(b.ingredient).includes('butter') && ua?.kind === 'vol') { expect = 24 / ua.f; how = '1 stick = 8 Tbsp'; }
    else if (ub && ub.kind === 'wt') {
      const gp = gramsPerUnit(state, b.ingredient, b.unit);
      if (gp) { expect = ub.f / gp.g; how = `${fmt(gp.g)} g per ${b.unit}`; }
    }
    if (expect != null && !near(per, expect, Math.max(tol, 0.1))) issues.push({ type: 'bulk', severity: Math.abs(per - expect) / Math.max(per, expect) > 0.3 ? 'high' : 'med',
      title: `${b.ingredient}: ${b.unit} per ${b.bulkUnit}`,
      detail: `Table says ${fmt(per)} ${b.unit} per ${b.bulkUnit}; ${how} suggests about ${fmt(expect)}.`,
      fix: { kind: 'setBulk', ingredient: b.ingredient, unit: b.unit, bulkUnit: b.bulkUnit, perBulk: Math.round(expect * 1000) / 1000 } });
    if (b.bulkUnit && ub?.kind === 'butterstick' && !key(b.ingredient).includes('butter') && ua?.kind === 'vol')
      issues.push({ type: 'bulk', severity: 'med', title: `${b.ingredient}: ${b.unit} → ${b.bulkUnit}`, detail: `“${b.bulkUnit}” for ${b.ingredient} with factor ${fmt(per)} looks off. Double-check it.` });
  }

  // 5. Spelling variants that split one ingredient across shopping-list rows
  const variant = (field) => {
    const groups = new Map();
    for (const r of state.recipes) for (const i of r.ingredients) {
      const raw = String(i[field] || '').trim(); if (!raw) continue;
      const g = singular(raw); if (!groups.has(g)) groups.set(g, new Map());
      const m = groups.get(g); m.set(raw, (m.get(raw) || 0) + 1);
    }
    for (const m of groups.values()) if (m.size > 1) {
      const sorted = [...m.entries()].sort((a, b) => b[1] - a[1]);
      issues.push({ type: 'variant', severity: 'low', title: `${field === 'unit' ? 'Unit' : 'Ingredient'} spelled ${m.size} ways: ${sorted.map(s => `“${s[0]}” (${s[1]})`).join(', ')}`,
        detail: `These become separate shopping-list rows and miss conversions written for the other spelling.`,
        fix: { kind: 'rename', field, from: sorted.slice(1).map(s => s[0]), to: sorted[0][0] } });
    }
  };
  variant('unit'); variant('name');

  // 6. Coverage gaps for planned recipes
  const typedAll = (c) => state.recipes.filter(r => planned.has(key(r.name))).every(r => r.ingredients.filter(i => key(i.name) === key(c.name) && key(i.unit) === key(c.unit)).every(i => num(i.grams) != null));
  for (const c of coverage) if (c.planned) {
    if (!c.grams && typedAll(c)) { /* every planned use already has a typed weight */ }
    else if (!c.grams && !unitInfo(c.unit)) issues.push({ type: 'missing', severity: 'low', title: `${c.name} (${c.unit || 'no unit'}): no gram conversion`, detail: `Used in ${c.recipes.join(', ')}. Grams won't total on the shopping list.` });
    else if (!c.grams) issues.push({ type: 'missing', severity: 'low', title: `${c.name} (${c.unit}): no gram conversion`, detail: `Used in ${c.recipes.join(', ')}.` });
    if (!c.bulk && !(unitInfo(c.unit) && unitInfo(c.unit).kind !== 'butterstick')) issues.push({ type: 'missing-bulk', severity: 'low', title: `${c.name} (${c.unit || 'no unit'}): no bulk conversion`, detail: `Shopping list will show the recipe unit only.` });
  }
  issues.forEach(i => i.id = i.type + ':' + i.title);
  const order = { high: 0, med: 1, low: 2 };
  issues.sort((a, b) => order[a.severity] - order[b.severity] || (b.planned ? 1 : 0) - (a.planned ? 1 : 0));
  return { issues, coverage };
}
function fmt(n, d) {
  n = num(n); if (n == null) return '';
  if (d == null) d = Math.abs(n) >= 100 ? 0 : Math.abs(n) >= 10 ? 1 : Math.abs(n) >= 0.1 || n === 0 ? 2 : 4;
  return (+n.toFixed(d)).toLocaleString(undefined, { maximumFractionDigits: d });
}
if (typeof module !== 'undefined') Object.assign(module.exports, { conversionChecks, gramsPerUnit, unitInfo, fmt });
