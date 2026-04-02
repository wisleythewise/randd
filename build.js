#!/usr/bin/env node
// Reads PASSWORD from .env, hashes it, and injects into index.html
const fs = require('fs');
const crypto = require('crypto');

// Parse .env
const env = {};
fs.readFileSync('.env', 'utf8').split('\n').forEach(line => {
  const [k, ...v] = line.split('=');
  if (k && v.length) env[k.trim()] = v.join('=').trim();
});

const password = env.PASSWORD;
if (!password) { console.error('PASSWORD not set in .env'); process.exit(1); }

const hash = crypto.createHash('sha256').update(password).digest('hex');

let html = fs.readFileSync('index.html', 'utf8');
html = html.replace(/const PASSWORD_HASH = '[^']*';/, `const PASSWORD_HASH = '${hash}';`);
fs.writeFileSync('index.html', html);

console.log(`Password hash injected: ${hash.slice(0, 12)}…`);
