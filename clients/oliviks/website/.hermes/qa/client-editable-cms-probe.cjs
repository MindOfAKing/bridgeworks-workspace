const fs = require('fs');
const path = require('path');
const root = process.cwd();
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
const exists = (file) => fs.existsSync(path.join(root, file));

const pkg = read('package.json');
const menuPage = read('src/app/menu/page.tsx');

const checks = [
  ['Supabase dependency installed', pkg.includes('@supabase/supabase-js')],
  ['Supabase schema exists', exists('supabase/schema.sql')],
  ['schema has menu_categories table', exists('supabase/schema.sql') && read('supabase/schema.sql').includes('create table if not exists public.menu_categories')],
  ['schema has menu_items table', exists('supabase/schema.sql') && read('supabase/schema.sql').includes('create table if not exists public.menu_items')],
  ['schema has menu_option_groups table', exists('supabase/schema.sql') && read('supabase/schema.sql').includes('create table if not exists public.menu_option_groups')],
  ['schema has menu_options table', exists('supabase/schema.sql') && read('supabase/schema.sql').includes('create table if not exists public.menu_options')],
  ['schema has site_settings table', exists('supabase/schema.sql') && read('supabase/schema.sql').includes('create table if not exists public.site_settings')],
  ['schema has owner email allowlist setting', exists('supabase/schema.sql') && read('supabase/schema.sql').includes('admin_allowed_emails')],
  ['env example documents Supabase keys without secrets', exists('.env.example') && read('.env.example').includes('NEXT_PUBLIC_SUPABASE_URL=') && read('.env.example').includes('SUPABASE_SERVICE_ROLE_KEY=')],
  ['Supabase server helper isolated', exists('src/lib/supabase/server.ts') && read('src/lib/supabase/server.ts').includes('createClient')],
  ['CMS menu loader exists', exists('src/lib/cms/menu.ts') && read('src/lib/cms/menu.ts').includes('getMenuCategories')],
  ['CMS loader preserves static fallback', exists('src/lib/cms/menu.ts') && read('src/lib/cms/menu.ts').includes('staticMenu') && read('src/lib/cms/menu.ts').includes('fallback')],
  ['public menu page reads through CMS loader', menuPage.includes('await getMenuCategories()') && menuPage.includes('<MenuList categories=')],
  ['MenuList accepts categories prop', read('src/components/MenuList.tsx').includes('categories?: MenuCategory[]')],
  ['admin page exists', exists('src/app/admin/page.tsx') && read('src/app/admin/page.tsx').includes('Oliviks Admin')],
  ['admin menu API exists', exists('src/app/api/admin/menu/route.ts') && read('src/app/api/admin/menu/route.ts').includes('export async function GET')],
  ['admin API avoids browser service role exposure', exists('src/app/api/admin/menu/route.ts') && read('src/app/api/admin/menu/route.ts').includes('serverSupabase')],
  ['admin write API has server-side secret guard', exists('src/app/api/admin/menu/route.ts') && read('src/app/api/admin/menu/route.ts').includes('ADMIN_API_SECRET') && read('.env.example').includes('ADMIN_API_SECRET=')],
];

const failed = checks.filter(([, ok]) => !ok).map(([name]) => name);
if (failed.length) {
  console.error('Client-editable CMS probe failed:\n- ' + failed.join('\n- '));
  process.exit(1);
}
console.log('Client-editable CMS probe passed');
