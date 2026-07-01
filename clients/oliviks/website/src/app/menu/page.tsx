import type { Metadata } from 'next';
import { Star } from 'lucide-react';
import { MenuList } from '@/components/MenuList';
import { site, waLink } from '@/data/site';
import { getMenuCategories } from '@/lib/cms/menu';

export const metadata: Metadata = {
  title: 'Menu',
  description:
    'What Oliviks cooks in Budapest: jollof rice, fried rice, egusi, oha, ogbono, suya, plantain, puff puff, snacks, and drinks.',
};

export default async function MenuPage() {
  const menuLoad = await getMenuCategories();
  const orderOnline = site.ordering.shopUrl;
  const wa = waLink('Hi Oliviks, I have a question before I order:');

  return (
    <div>
      {/* ================= Hero ================= */}
      <section className="grain bg-gradient-to-b from-palm-800 to-palm-900 text-cream">
        <div className="container-x relative pb-14 pt-14">
          <div aria-hidden="true" className="absolute -right-32 -top-40 h-96 w-96 rounded-full border border-cream/10" />

          <div className="grid items-center gap-10 lg:grid-cols-[1.25fr_0.75fr]">
            <div>
              <p className="eyebrow-onred animate-hero-down">Our dishes</p>
              <h1 className="animate-hero-up anim-d-100 mt-5 font-display text-[clamp(2.8rem,6.5vw,4.4rem)] font-extrabold leading-[0.98] tracking-tight">
                What We Cook
              </h1>
              <p className="animate-hero-up anim-d-220 mt-5 max-w-[560px] text-[17px] leading-relaxed text-cream/80">
                Jollof and fried rice. Egusi, oha, and ogbono soup with swallow. Suya, pepper soup,
                fried yam, plantain, and puff puff. Each dish is made fresh and served the way it
                would be in Nigeria.
              </p>
              <div className="animate-hero-up anim-d-310 mt-5 inline-flex items-center gap-2 rounded-full border border-gold/40 bg-cream/5 px-4 py-2">
                <span className="text-[13.5px] font-semibold text-gold">
                  First time here? Start with jollof, plantain, and puff puff.
                </span>
              </div>
              <div className="animate-hero-up anim-d-380 mt-7 flex flex-wrap gap-3">
                <a href={orderOnline} target="_blank" rel="noopener noreferrer" className="btn-appetite text-[16px]">
                  Order Online
                </a>
                <a href="#menu" className="btn-chalk-outline text-[16px]">
                  See the Menu
                </a>
              </div>
            </div>

            {/* Rating card */}
            <div className="animate-hero-up anim-d-240 rounded-3xl border border-cream/15 bg-cream/5 p-8">
              <div className="flex items-center gap-3">
                <span className="font-display text-[3rem] font-extrabold leading-none text-gold">
                  {site.reviews.rating}
                </span>
                <span className="text-[13px] leading-tight text-cream/70">
                  <span className="flex text-gold" aria-hidden="true">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} size={13} fill="currentColor" />
                    ))}
                  </span>
                  {site.reviews.count} reviews on Google
                </span>
              </div>
              <p className="mt-5 font-display text-[19px] font-medium italic leading-snug text-cream">
                &ldquo;Honest food with soul.&rdquo;
              </p>
              <div className="my-5 h-px bg-cream/15" aria-hidden="true" />
              <div className="text-[13.5px] leading-[1.8] text-cream/70">
                <p>
                  <strong className="text-cream">Pickup</strong> &middot; {site.address.street},{' '}
                  {site.address.city}
                </p>
                <p>
                  <strong className="text-cream">Mon–Sat</strong> &middot; 11:00–20:00
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div className="ankara-rule-thin" />

      {/* ================= Menu ================= */}
      <section className="container-x pb-16 pt-8" id="menu">
        <MenuList categories={menuLoad.categories} />
      </section>

      {/* ================= Ordering note ================= */}
      <div className="container-x pb-16">
        <div className="flex flex-wrap items-center justify-between gap-5 rounded-3xl border-2 border-ink/10 bg-gold-50 px-7 py-6">
          <div className="max-w-[640px]">
            <p className="font-display text-[18px] font-extrabold text-cocoa">How ordering works</p>
            <p className="mt-2 text-[14.5px] leading-relaxed text-cocoa/70">
              Message us on WhatsApp with your order. Mention your protein or swallow preference
              where needed. Pickup at Rákóczi tér 9. Already on Wolt or Marwa? You can order there
              too.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <a
              href={orderOnline}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary px-6 py-3 text-[14px]"
            >
              Order Online
            </a>
            <a
              href={wa}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-ghost px-6 py-3 text-[14px]"
            >
              Message on WhatsApp
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
