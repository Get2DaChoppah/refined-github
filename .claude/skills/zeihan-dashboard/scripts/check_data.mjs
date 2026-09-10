#!/usr/bin/env node
// Validates the country data block of a Zeihan Lens dashboard HTML file.
// Usage: node check_data.mjs path/to/dashboard.html
import fs from 'node:fs';
import vm from 'node:vm';

const file = process.argv[2];
if (!file) { console.error('usage: node check_data.mjs <dashboard.html>'); process.exit(2); }
const html = fs.readFileSync(file, 'utf8');

function extract(name) {
  const re = new RegExp(`const ${name} = `);
  const m = re.exec(html);
  if (!m) throw new Error(`could not find "const ${name} ="`);
  let i = m.index + m[0].length, depth = 0, start = i, inStr = null;
  for (; i < html.length; i++) {
    const ch = html[i];
    if (inStr) { if (ch === '\\') { i++; continue; } if (ch === inStr) inStr = null; continue; }
    if (ch === "'" || ch === '"' || ch === '`') { inStr = ch; continue; }
    if (ch === '[' || ch === '{') depth++;
    if (ch === ']' || ch === '}') { depth--; if (depth === 0) return html.slice(start, i + 1); }
  }
  throw new Error(`unterminated ${name}`);
}

const C = vm.runInNewContext('(' + extract('C') + ')');
const PATHS = vm.runInNewContext('(' + extract('PATHS') + ')');
const ids = new Set(PATHS.map(p => p.id));

const problems = [];
const seen = new Set();
const enumSec = new Set(['exporter', 'balanced', 'importer']);
const enumTraj = new Set(['rising', 'stable', 'fading', 'collapsing']);
const sum = a => a.reduce((s, x) => s + x, 0);

for (const c of C) {
  const tag = `${c.name || '?'} (${c.id})`;
  const flag = msg => problems.push(`${tag}: ${msg}`);
  if (typeof c.id !== 'string' || !/^\d{3}$/.test(c.id)) flag('id must be a 3-character zero-padded string');
  else if (!ids.has(c.id)) flag('id not present in the inlined map data');
  if (seen.has(c.id)) flag('duplicate id'); seen.add(c.id);
  for (const k of ['name', 'region', 'take']) if (!c[k]) flag(`missing ${k}`);
  if (!Array.isArray(c.risks) || c.risks.length === 0) flag('risks is empty');
  if (!Array.isArray(c.pop) || c.pop.length !== 2 || c.pop.some(x => !(x > 0))) flag('pop must be [2025, 2050] in millions');
  for (const k of ['b25', 'b50']) {
    if (!Array.isArray(c[k]) || c[k].length !== 5) { flag(`${k} must have five bands`); continue; }
    const s = sum(c[k]); if (Math.abs(s - 100) > 0.01) flag(`${k} sums to ${s.toFixed(1)}, not 100`);
  }
  if (!(c.age >= 14 && c.age <= 60)) flag(`median age ${c.age} out of range`);
  if (!(c.tfr >= 0.5 && c.tfr <= 8)) flag(`fertility ${c.tfr} out of range`);
  if (!(c.cons >= 20 && c.cons <= 95)) flag(`consumption share ${c.cons}% out of range`);
  if (!(c.exp >= 3 && c.exp <= 200)) flag(`export share ${c.exp}% out of range`);
  if (!(c.gdp > 0) || !(c.pc > 0)) flag('gdp and pc must be positive');
  if (!Number.isInteger(c.outlook) || c.outlook < 1 || c.outlook > 10) flag(`outlook ${c.outlook} must be an integer 1–10`);
  if (!enumTraj.has(c.traj)) flag(`traj "${c.traj}" invalid`);
  if (!enumSec.has(c.energy)) flag(`energy "${c.energy}" invalid`);
  if (!enumSec.has(c.food)) flag(`food "${c.food}" invalid`);
  const hi = c.outlook >= 7 && (c.traj === 'fading' || c.traj === 'collapsing');
  const lo = c.outlook <= 3 && (c.traj === 'rising' || c.traj === 'stable');
  if (hi || lo) flag(`outlook ${c.outlook} and trajectory "${c.traj}" disagree`);
}

if (problems.length) { console.log(`${problems.length} problem(s) in ${C.length} countries:`); for (const p of problems) console.log('  - ' + p); process.exit(1); }
console.log(`OK: ${C.length} countries, all bands sum to 100, all ids on the map, all fields in range.`);
