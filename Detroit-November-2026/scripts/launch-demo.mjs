import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const read = path => readFileSync(join(root, path), 'utf8');
const json = path => JSON.parse(read(path));
const source = json('data\\manufacturer-products.json');
const retailer = json('data\\retailer-requirements.json');
const schema = json('contracts\\launch-package.schema.json');
const fixture = json('fixtures\\expected-facts.json');
const templates = Object.fromEntries(
  ['launch-brief.md', 'retailer-listing.csv', 'handoff-email.md']
    .map(name => [name, read(`templates\\${name}`)])
);

function pointer(value, path) {
  assert.ok(path.startsWith('/'), `Invalid pointer: ${path}`);
  return path.slice(1).split('/').reduce((node, key) => {
    const decoded = key.replace(/~1/g, '/').replace(/~0/g, '~');
    assert.ok(node !== null && typeof node === 'object' && Object.hasOwn(node, decoded), `Missing pointer: ${path}`);
    return node[decoded];
  }, value);
}

// This bounded validator supports exactly the keywords used by our local schema.
// Unknown keywords fail rather than silently weakening contract enforcement.
function validateSchema(value, rule, path = '$') {
  const supported = new Set(['$schema', 'title', 'description', 'type', 'const', 'enum',
    'required', 'properties', 'additionalProperties', 'minLength', 'maxLength',
    'pattern', 'minimum', 'items', 'minItems', 'maxItems']);
  for (const key of Object.keys(rule)) assert.ok(supported.has(key), `Unsupported schema keyword: ${key}`);
  if (Object.hasOwn(rule, 'const')) assert.deepEqual(value, rule.const, `${path}: const`);
  if (rule.enum) assert.ok(rule.enum.includes(value), `${path}: enum`);
  const type = value === null ? 'null' : Array.isArray(value) ? 'array' : typeof value;
  if (rule.type) {
    const allowed = Array.isArray(rule.type) ? rule.type : [rule.type];
    assert.ok(allowed.includes(type) || (allowed.includes('integer') && Number.isInteger(value)), `${path}: type`);
  }
  if (typeof value === 'string') {
    const length = [...value].length;
    if (rule.minLength !== undefined) assert.ok(length >= rule.minLength, `${path}: minLength`);
    if (rule.maxLength !== undefined) assert.ok(length <= rule.maxLength, `${path}: maxLength`);
    if (rule.pattern) assert.match(value, new RegExp(rule.pattern), `${path}: pattern`);
  }
  if (typeof value === 'number' && rule.minimum !== undefined) assert.ok(value >= rule.minimum, `${path}: minimum`);
  if (type === 'array') {
    if (rule.minItems !== undefined) assert.ok(value.length >= rule.minItems, `${path}: minItems`);
    if (rule.maxItems !== undefined) assert.ok(value.length <= rule.maxItems, `${path}: maxItems`);
    value.forEach((item, index) => validateSchema(item, rule.items, `${path}[${index}]`));
  }
  if (type === 'object') {
    for (const key of rule.required ?? []) assert.ok(Object.hasOwn(value, key), `${path}: missing ${key}`);
    for (const [key, child] of Object.entries(value)) {
      if (rule.additionalProperties === false) assert.ok(Object.hasOwn(rule.properties, key), `${path}: unexpected ${key}`);
      if (rule.properties?.[key]) validateSchema(child, rule.properties[key], `${path}.${key}`);
    }
  }
}

function blockersFor(product) {
  return retailer.requiredForSubmission.filter(({ field }) => {
    const value = product[field];
    return value === null || value === '' || (Array.isArray(value) && value.length === 0);
  });
}

function buildPackage(product, index) {
  const blockers = blockersFor(product);
  const listingFields = ['sku', 'currency', 'msrp', 'gtin', 'imageAssets', 'warrantyTerms', 'specifications'];
  const evidence = listingFields.map(field => ({
    field: `/listing/${field}`, sourceId: source.sourceId, pointer: `/products/${index}/${field}`
  }));
  evidence.push(
    { field: '/listing/brand', sourceId: source.sourceId, pointer: '/manufacturer/brand' },
    { field: '/listing/bullets', sourceId: source.sourceId, pointer: `/products/${index}/approvedBullets` },
    ...['launchDate', 'audience', 'inBox'].map(field => ({
      field: `/brief/${field}`, sourceId: source.sourceId, pointer: `/products/${index}/${field}`
    }))
  );
  return {
    schemaVersion: '1.0', synthetic: true, generationMode: 'deterministic-local-reference',
    productId: product.productId, retailerId: retailer.retailerId,
    listing: {
      ...Object.fromEntries(listingFields.map(field => [field, product[field]])),
      title: `${source.manufacturer.brand} ${product.name}`,
      brand: source.manufacturer.brand,
      category: retailer.categoryMap[product.category],
      bullets: product.approvedBullets
    },
    brief: {
      launchDate: product.launchDate, audience: product.audience, inBox: product.inBox,
      knownGaps: blockers.map(blocker => blocker.message)
    },
    handoff: {
      subject: `Review requested: ${product.sku} retail launch draft`,
      body: `Category reviewer and manufacturer fact owner: please review the ${product.name} draft for ${retailer.retailerName}. Target launch: ${product.launchDate}. ${blockers.length} required onboarding fields are unresolved. Resolve the blockers and verify source facts before submission. This is synthetic conference data; no approval or submission has occurred.`
    },
    evidence,
    review: { status: 'needs_review', approvedBy: null, blockers }
  };
}

function validatePackage(pkg) {
  validateSchema(pkg, schema);
  const expected = fixture.products.find(product => product.productId === pkg.productId);
  assert.ok(expected, `Unknown fixture product: ${pkg.productId}`);
  assert.deepEqual(pkg.listing, expected.listing, `${pkg.productId}: listing facts differ from independent fixture`);
  const { knownGaps, ...briefFacts } = pkg.brief;
  assert.deepEqual(briefFacts, expected.brief, `${pkg.productId}: brief facts`);
  const index = source.products.findIndex(product => product.productId === pkg.productId);
  assert.ok(index >= 0, 'Product missing from source');
  const product = source.products[index];
  const expectedBlockers = blockersFor(product);
  assert.deepEqual(pkg.review.blockers, expectedBlockers, 'Missing or altered onboarding blockers');
  assert.deepEqual(pkg.review.blockers.map(item => item.code), expected.blockerCodes, 'Fixture blockers');
  assert.deepEqual(knownGaps, expectedBlockers.map(item => item.message), 'Brief must disclose all gaps');
  assert.equal(pkg.listing.title, `${source.manufacturer.brand} ${product.name}`, 'Title derivation');
  assert.equal(pkg.listing.category, retailer.categoryMap[product.category], 'Retailer category mapping');
  const requiredEvidence = buildPackage(product, index).evidence;
  assert.deepEqual(pkg.evidence, requiredEvidence, 'Evidence coverage or source path differs');
  for (const evidence of pkg.evidence) {
    assert.deepEqual(pointer(pkg, evidence.field), pointer(source, evidence.pointer), `Evidence mismatch: ${evidence.field}`);
  }
  const copy = JSON.stringify([pkg.listing, pkg.brief, pkg.handoff]).toLowerCase();
  for (const claim of retailer.copyPolicy.prohibitedUnsubstantiatedClaims) {
    assert.ok(!copy.includes(claim.toLowerCase()), `Unsupported claim: ${claim}`);
  }
  assert.equal(pkg.listing.bullets.length, retailer.bulletCount);
  assert.ok([...pkg.listing.title].length <= retailer.titleMaxLength);
  pkg.listing.bullets.forEach(bullet => assert.ok([...bullet].length <= retailer.bulletMaxLength));
}

function render(template, values) {
  const result = template.replace(/\{\{(\w+)\}\}/g, (_, key) => {
    assert.ok(Object.hasOwn(values, key), `Missing template value: ${key}`);
    return values[key];
  });
  assert.ok(!/\{\{|\}\}/.test(result), 'Unresolved template token');
  return result;
}

const csvCell = value => `"${String(value ?? '').replaceAll('"', '""')}"`;
function artifacts(pkg) {
  const values = {
    ...pkg.listing, ...pkg.brief, ...pkg.handoff, retailerName: retailer.retailerName,
    msrp: pkg.listing.msrp.toFixed(2),
    inBox: pkg.brief.inBox.map(item => `- ${item}`).join('\n'),
    bullets: pkg.listing.bullets.map(item => `- ${item}`).join('\n'),
    gaps: pkg.brief.knownGaps.map(item => `- ${item}`).join('\n')
  };
  values.row = [pkg.listing.sku, pkg.listing.title, pkg.listing.brand, pkg.listing.category,
    pkg.listing.currency, values.msrp, pkg.listing.gtin, pkg.listing.imageAssets.join(';'),
    pkg.listing.warrantyTerms, ...pkg.listing.bullets, pkg.review.status, 'true'].map(csvCell).join(',');
  return {
    'package.json': `${JSON.stringify(pkg, null, 2)}\n`,
    'review.json': `${JSON.stringify({ synthetic: true, productId: pkg.productId, ...pkg.review }, null, 2)}\n`,
    ...Object.fromEntries(Object.entries(templates).map(([name, template]) => [name, render(template, values)]))
  };
}

function negativeTests(pkg) {
  const mutations = [
    value => { value.listing.msrp = 99; },
    value => { value.listing.specifications.maxSpeedRpm = 9999; },
    value => { value.listing.title = 'x'.repeat(81); },
    value => { value.listing.bullets.pop(); },
    value => { value.listing.bullets[0] = 'UL listed'; },
    value => { value.listing.gtin = '0123456789012'; },
    value => { value.evidence.pop(); },
    value => { value.evidence[0].pointer = '/products/99/sku'; },
    value => { value.review.status = 'approved'; },
    value => { value.review.approvedBy = 'Demo'; },
    value => { value.review.blockers = []; },
    value => { value.brief.knownGaps = []; },
    value => { value.productId = 'unknown'; },
    value => { value.listing.extra = 'unexpected'; },
    value => { value.handoff.body = 'Certified safest tool'; }
  ];
  for (const mutate of mutations) {
    const bad = structuredClone(pkg);
    mutate(bad);
    assert.throws(() => validatePackage(bad), `Mutation was accepted: ${mutate}`);
  }
  assert.throws(() => render('{{missing}}', {}));
  assert.throws(() => pointer(source, '/products/99/sku'));
  assert.throws(() => validateSchema({}, { type: 'object', unknownKeyword: true }));
}

function knowledgeDocuments() {
  const specLabels = {
    nominalVoltageV: 'Nominal voltage (V)',
    batteryCapacityAh: 'Battery capacity per battery (Ah)',
    batteryCount: 'Battery count',
    maxSpeedRpm: 'Maximum speed (rpm)',
    maxTorqueNm: 'Maximum torque (Nm)',
    toolHolder: 'Tool holder',
    massWithBatteryKg: 'Mass with battery (kg)'
  };
  const products = [
    '# Manufacturer product specifications',
    '', 'SYNTHETIC CONFERENCE DATA', '', source.notice, '',
    `Source ID: ${source.sourceId}`,
    `Schema version: ${source.schemaVersion}`,
    `Manufacturer: ${source.manufacturer.name}`,
    `Location: ${source.manufacturer.location}`,
    `Brand: ${source.manufacturer.brand}`, '',
    ...source.products.flatMap(product => [
      `## ${product.name}`, '',
      `Product ID: ${product.productId}`,
      `SKU: ${product.sku}`,
      `Manufacturer category: ${product.category}`,
      `Target launch date: ${product.launchDate}`,
      `Audience: ${product.audience}`,
      `Manufacturer MSRP: ${product.currency} ${product.msrp.toFixed(2)} (not retailer selling price)`, '',
      '### Specifications', '',
      ...Object.entries(product.specifications).map(([key, value]) => {
        assert.ok(specLabels[key], `Missing readable specification label: ${key}`);
        return `- ${specLabels[key]}: ${value}`;
      }), '',
      '### In the box', '',
      ...product.inBox.map(item => `- ${item}`), '',
      '### Approved listing bullets', '',
      ...product.approvedBullets.map(item => `- ${item}`), '',
      '### Missing onboarding information', '',
      `GTIN: ${product.gtin ?? 'unknown; manufacturer must supply a verified identifier'}`,
      `Approved images: ${product.imageAssets.length ? product.imageAssets.join('; ') : 'none supplied'}`,
      `Warranty terms: ${product.warrantyTerms ?? 'unknown; approved terms required'}`, ''
    ])
  ].join('\n');
  const policy = [
    '# Retailer onboarding requirements', '',
    'SYNTHETIC CONFERENCE DATA', '', retailer.notice, '',
    `Source ID: ${retailer.sourceId}`,
    `Schema version: ${retailer.schemaVersion}`,
    `Retailer: ${retailer.retailerName}`,
    `Retailer ID: ${retailer.retailerId}`, '',
    '## Listing format', '',
    `- Title: brand + product name; maximum ${retailer.titleMaxLength} characters.`,
    `- Bullets: exactly ${retailer.bulletCount}; maximum ${retailer.bulletMaxLength} characters each.`,
    `- Currency: ${retailer.currency}. Manufacturer MSRP is not retailer selling price.`, '',
    '## Category mapping', '',
    ...Object.entries(retailer.categoryMap).map(([category, mapped]) => `- ${category} -> ${mapped}`), '',
    '## Required for submission', '',
    ...retailer.requiredForSubmission.map(item => `- ${item.field} (${item.code}): ${item.message}`), '',
    '## Copy policy', '',
    `Facts only: ${retailer.copyPolicy.factsOnly ? 'yes' : 'no'}.`,
    retailer.copyPolicy.instructions, '',
    'Do not add these unsubstantiated claims:', '',
    ...retailer.copyPolicy.prohibitedUnsubstantiatedClaims.map(claim => `- ${claim}`), '',
    '## Human review and disposition', '', retailer.approvalPolicy, ''
  ].join('\n');
  return Object.fromEntries(
    [['manufacturer-products', products], ['retailer-requirements', policy]]
      .flatMap(([name, content]) => ['md', 'txt'].map(extension => [`${name}.${extension}`, content]))
  );
}

const command = process.argv[2];
assert.ok(['build', 'check'].includes(command), 'Usage: node scripts\\launch-demo.mjs build|check');
assert.equal(source.synthetic, true);
assert.equal(retailer.synthetic, true);
assert.equal(source.schemaVersion, schema.properties.schemaVersion.const);
assert.equal(retailer.schemaVersion, source.schemaVersion);
assert.deepEqual(source.products.map(p => p.productId).sort(), fixture.products.map(p => p.productId).sort());
assert.equal(new Set(source.products.map(p => p.productId)).size, source.products.length);
assert.equal(new Set(source.products.map(p => p.sku)).size, source.products.length);
for (const [index, product] of source.products.entries()) {
  const pkg = buildPackage(product, index);
  validatePackage(pkg);
  const files = artifacts(pkg);
  if (command === 'build') {
    const output = join(root, 'examples', product.productId);
    mkdirSync(output, { recursive: true });
    for (const [name, content] of Object.entries(files)) writeFileSync(join(output, name), content, 'utf8');
  } else {
    validatePackage(json(`examples\\${product.productId}\\package.json`));
    for (const [name, expected] of Object.entries(files)) {
      assert.equal(read(`examples\\${product.productId}\\${name}`), expected, `Stale artifact: ${product.productId}\\${name}`);
    }
    negativeTests(pkg);
  }
}
const knowledge = knowledgeDocuments();
if (command === 'build') mkdirSync(join(root, 'knowledge'), { recursive: true });
for (const [name, content] of Object.entries(knowledge)) {
  const path = `knowledge\\${name}`;
  if (command === 'build') writeFileSync(join(root, path), content, 'utf8');
  else assert.equal(read(path), content, `Stale knowledge document: ${name}`);
}
console.log(`${command}: ${source.products.length} synthetic product packages; no cloud calls, approvals or submissions.`);
if (command === 'check') console.log('Contract, independent facts, evidence, artifact/knowledge freshness and 36 negative checks passed.');
