import type { Metadata } from 'next';
import Link from 'next/link';
import { Database, ExternalLink, ShieldCheck, Utensils } from 'lucide-react';
import { AdminMenuEditor } from '@/components/AdminMenuEditor';
import { getMenuCategories } from '@/lib/cms/menu';
import { isSupabaseAdminConfigured, isSupabaseConfigured } from '@/lib/supabase/server';

export const metadata: Metadata = {
  title: 'Oliviks Admin',
  description: 'Owner dashboard foundation for editing Oliviks Kitchen menu and site content.',
  robots: { index: false, follow: false },
};

export default async function AdminPage() {
  const menuLoad = await getMenuCategories();
  const configured = isSupabaseConfigured();
  const adminConfigured = isSupabaseAdminConfigured();
  const itemCount = menuLoad.categories.reduce((total, category) => total + category.items.length, 0);

  return (
    <div className="container-x py-16">
      <header className="mx-auto max-w-3xl text-center">
        <span className="eyebrow">Owner dashboard</span>
        <h1 className="mt-3 font-display text-4xl font-bold text-cocoa sm:text-5xl">Oliviks Admin</h1>
        <p className="mt-4 text-lg leading-relaxed text-cocoa/70">
          This is the client-editable CMS foundation for menu, prices, images, availability, catering, and site settings.
        </p>
      </header>

      <section className="mt-12 grid gap-5 md:grid-cols-3">
        <StatusCard icon={<Database />} title="Database">
          {configured ? 'Supabase public read keys are configured.' : 'Waiting for Supabase URL and anon key.'}
        </StatusCard>
        <StatusCard icon={<ShieldCheck />} title="Admin writes">
          {adminConfigured ? 'Server-side service role key is configured.' : 'Server-side service role key still needs to be added.'}
        </StatusCard>
        <StatusCard icon={<Utensils />} title="Menu source">
          {menuLoad.source === 'supabase' ? 'Loaded from Supabase.' : `Using static fallback: ${itemCount} items.`}
        </StatusCard>
      </section>

      <section className="mt-10 rounded-[2rem] border border-cocoa/10 bg-white p-6 shadow-sm sm:p-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <h2 className="font-display text-2xl font-bold text-cocoa">Menu editor foundation</h2>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-cocoa/65">
              The public menu now reads through a CMS adapter. Until Supabase credentials and owner login are connected, it safely falls back to the current approved static menu.
            </p>
          </div>
          <Link href="/menu" className="btn-ghost shrink-0">
            View menu <ExternalLink size={16} />
          </Link>
        </div>

        <div className="mt-6 overflow-hidden rounded-2xl border border-cocoa/10">
          <table className="w-full text-left text-sm">
            <thead className="bg-cream text-xs uppercase tracking-[0.16em] text-cocoa/55">
              <tr>
                <th className="px-4 py-3">Category</th>
                <th className="px-4 py-3">Items</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-cocoa/10 bg-white">
              {menuLoad.categories.map((category) => (
                <tr key={category.id}>
                  <td className="px-4 py-3 font-semibold text-cocoa">{category.title}</td>
                  <td className="px-4 py-3 text-cocoa/65">{category.items.length}</td>
                  <td className="px-4 py-3 text-cocoa/65">
                    {menuLoad.source === 'supabase' ? 'Editable' : 'Prepared for CMS seed'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-8">
          <AdminMenuEditor categories={menuLoad.categories} source={menuLoad.source} />
        </div>
      </section>

      <section className="mt-8 rounded-3xl border border-gold/35 bg-gold/10 p-6 text-cocoa">
        <h2 className="font-display text-xl font-bold">How to use this page</h2>
        <p className="mt-2 text-sm leading-relaxed text-cocoa/70">
          Pick a dish, edit its name, description, price, image, or availability, paste the
          admin access code, and save. The public menu updates within about a minute. Note:
          this edits the website menu; the prices customers pay at checkout are set in
          WooCommerce on shop.oliviks.com.
        </p>
      </section>
    </div>
  );
}

function StatusCard({ icon, title, children }: { icon: React.ReactNode; title: string; children: React.ReactNode }) {
  return (
    <article className="rounded-3xl border border-cocoa/10 bg-white p-6 shadow-sm">
      <div className="mb-4 text-palm">{icon}</div>
      <h2 className="font-display text-xl font-bold text-cocoa">{title}</h2>
      <p className="mt-2 text-sm leading-relaxed text-cocoa/65">{children}</p>
    </article>
  );
}
