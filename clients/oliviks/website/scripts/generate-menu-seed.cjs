const fs = require('fs');
const ts = require('typescript');
const vm = require('vm');
const crypto = require('crypto');

const source = fs.readFileSync('src/data/menu.ts', 'utf8');
const js = ts.transpileModule(source, {
  compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
}).outputText;

const sandbox = { exports: {}, require, console };
vm.runInNewContext(js, sandbox, { filename: 'src/data/menu.ts' });
const menu = sandbox.exports.menu;

if (!Array.isArray(menu)) throw new Error('Could not read exported menu from src/data/menu.ts');

function deterministicUuid(name) {
  const h = crypto.createHash('sha1').update(`oliviks-kitchen:${name}`).digest();
  // Avoid bitwise operators because Hermes terminal guard can misread ampersands in inline commands.
  h[6] = (h[6] % 16) + 80;
  h[8] = (h[8] % 64) + 128;
  const hex = h.subarray(0, 16).toString('hex');
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20, 32)}`;
}

function q(value) {
  return value == null ? 'null' : `'${String(value).replace(/'/g, "''")}'`;
}

function textArray(values) {
  return values && values.length ? `array[${values.map(q).join(', ')}]::text[]` : `'{}'::text[]`;
}

const out = [];
out.push('-- Oliviks Kitchen seed data generated from src/data/menu.ts');
out.push('-- Run after supabase/schema.sql in the Supabase SQL editor.');
out.push('');
out.push('begin;');
out.push('');
out.push('delete from public.menu_options;');
out.push('delete from public.menu_option_groups;');
out.push('delete from public.menu_items;');
out.push('delete from public.menu_categories;');
out.push('');

menu.forEach((category, categoryIndex) => {
  out.push(
    `insert into public.menu_categories (id, title, blurb, sort_order, is_active) values (${q(category.id)}, ${q(category.title)}, ${q(category.blurb || '')}, ${categoryIndex}, true) on conflict (id) do update set title = excluded.title, blurb = excluded.blurb, sort_order = excluded.sort_order, is_active = excluded.is_active, updated_at = now();`,
  );
});

out.push('');

menu.forEach((category) => {
  (category.items || []).forEach((item, itemIndex) => {
    const itemId = deterministicUuid(`item:${category.id}:${item.name}`);
    const tags = item.tags || [];
    const featured = tags.includes('popular');

    out.push(
      `insert into public.menu_items (id, category_id, name, description, price_label, image_url, tags, is_available, is_featured, sort_order) values (${q(itemId)}::uuid, ${q(category.id)}, ${q(item.name)}, ${q(item.description || '')}, ${q(item.price)}, ${q(item.image)}, ${textArray(tags)}, true, ${featured ? 'true' : 'false'}, ${itemIndex}) on conflict (id) do update set category_id = excluded.category_id, name = excluded.name, description = excluded.description, price_label = excluded.price_label, image_url = excluded.image_url, tags = excluded.tags, is_available = excluded.is_available, is_featured = excluded.is_featured, sort_order = excluded.sort_order, updated_at = now();`,
    );

    (item.optionGroups || []).forEach((group, groupIndex) => {
      const groupId = deterministicUuid(`group:${category.id}:${item.name}:${group.id}`);
      out.push(
        `insert into public.menu_option_groups (id, item_id, group_key, label, type, is_required, sort_order) values (${q(groupId)}::uuid, ${q(itemId)}::uuid, ${q(group.id)}, ${q(group.label)}, ${q(group.type)}, ${group.required ? 'true' : 'false'}, ${groupIndex}) on conflict (id) do update set item_id = excluded.item_id, group_key = excluded.group_key, label = excluded.label, type = excluded.type, is_required = excluded.is_required, sort_order = excluded.sort_order, updated_at = now();`,
      );

      (group.options || []).forEach((option, optionIndex) => {
        const optionId = deterministicUuid(`option:${category.id}:${item.name}:${group.id}:${option.label}`);
        out.push(
          `insert into public.menu_options (id, group_id, label, price_note, unit_price_ft, sort_order) values (${q(optionId)}::uuid, ${q(groupId)}::uuid, ${q(option.label)}, ${q(option.priceNote)}, ${option.unitPriceFt == null ? 'null' : Number(option.unitPriceFt)}, ${optionIndex}) on conflict (id) do update set group_id = excluded.group_id, label = excluded.label, price_note = excluded.price_note, unit_price_ft = excluded.unit_price_ft, sort_order = excluded.sort_order, updated_at = now();`,
        );
      });
    });
  });
});

out.push('');
out.push('commit;');
out.push('');
out.push(`-- Seed summary: ${menu.length} categories, ${menu.reduce((count, category) => count + (category.items || []).length, 0)} items.`);

fs.writeFileSync('supabase/seed-menu.sql', `${out.join('\n')}\n`, 'utf8');
console.log(`Wrote supabase/seed-menu.sql with ${menu.length} categories.`);
