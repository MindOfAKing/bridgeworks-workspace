import type { Metadata } from 'next';
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
  const orderOnline = waLink("Hi Oliviks, I'd like to place an order:");
  const wa = waLink('Hi Oliviks, I have a question before I order:');

  return (
    <div className="menu-page-bg">

      {/* Hero */}
      <section className="mx-auto max-w-[1180px] px-7 pb-8 pt-14 relative">
        {/* Papaya glow */}
        <div
          aria-hidden="true"
          className="menu-hero-glow pointer-events-none absolute left-[-6%] top-[-30px] z-0 h-[360px] w-[60%]"
        />

        <div className="relative z-10 grid items-center gap-9 lg:grid-cols-[1.3fr_0.7fr]">

          {/* Left */}
          <div>
            <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-palm">
              Our dishes
            </p>
            <h1 className="mt-3 font-display text-[clamp(2.6rem,6vw,3.75rem)] font-extrabold leading-[1.02] tracking-tight text-cocoa">
              What We Cook
            </h1>
            <p className="mt-4 max-w-[560px] text-[18px] leading-relaxed text-cocoa/70">
              Jollof and fried rice. Egusi, oha, and ogbono soup with swallow. Suya, pepper soup,
              fried yam, plantain, and puff puff. Each dish is made fresh and served the way it
              would be in Nigeria.
            </p>
            <div className="mt-5 inline-flex items-center gap-2 rounded-full border border-gold/40 bg-[#fff9ec] px-4 py-2">
              <span className="text-[13.5px] font-semibold text-palm">
                First time here? Start with jollof, plantain, and puff puff.
              </span>
            </div>
            <div className="mt-6 flex flex-wrap items-center gap-3">
              <a
                href={orderOnline}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-full bg-gold px-7 py-3.5 text-[16px] font-semibold text-cocoa shadow-[0_10px_28px_rgba(250,183,58,0.35)] transition-all hover:-translate-y-0.5 hover:shadow-lg active:scale-95"
              >
                Order Online
              </a>
              <a
                href="#menu"
                className="rounded-full border-2 border-palm px-7 py-3.5 text-[16px] font-semibold text-palm transition-all hover:-translate-y-0.5 active:scale-95"
              >
                See the Menu
              </a>
            </div>
          </div>

          {/* Right — info card */}
          <div className="rounded-[28px] bg-palm px-8 py-8 text-cream shadow-xl relative overflow-hidden">
            <div className="flex items-center gap-3">
              <span className="font-display text-[46px] font-extrabold leading-none">
                4.8<span className="text-[30px] text-gold">★</span>
              </span>
              <span className="flex h-[30px] w-[30px] items-center justify-center rounded-full bg-white shadow-sm">
                <svg width="18" height="18" viewBox="0 0 48 48">
                  <path fill="#4285F4" d="M43.611 20.083H42V20H24v8h11.303c-1.649 4.657-6.08 8-11.303 8-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4 12.955 4 4 12.955 4 24s8.955 20 20 20 20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z"/>
                  <path fill="#34A853" d="M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238C29.211 35.091 26.715 36 24 36c-5.202 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44z"/>
                  <path fill="#FBBC05" d="M6.306 14.691l6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4 16.318 4 9.656 8.337 6.306 14.691z"/>
                  <path fill="#EA4335" d="M43.611 20.083H42V20H24v8h11.303c-.792 2.237-2.231 4.166-4.087 5.571l6.19 5.238C39.99 36.205 44 30.659 44 24c0-1.341-.138-2.65-.389-3.917z"/>
                </svg>
              </span>
            </div>
            <p className="mt-2 text-[14px] text-[#f3dcdc]">Rated on Google</p>
            <p className="mt-5 font-display text-[19px] font-medium italic leading-snug">
              &ldquo;Honest food with soul.&rdquo;
            </p>
            <div className="my-5 h-px bg-white/20" />
            <div className="text-[13.5px] leading-[1.7] text-[#f3dcdc]">
              <p><strong className="text-cream">Pickup</strong> &middot; {site.address.street}, {site.address.city}</p>
              <p><strong className="text-cream">Mon–Sat</strong> &middot; 11:00–20:00</p>
            </div>
          </div>

        </div>
      </section>

      {/* Press strip */}
      <div className="bg-cocoa text-[#a3a59d]">
        <div className="mx-auto flex max-w-[1180px] flex-wrap items-center gap-3 px-7 py-4 font-display text-[13px] tracking-[0.04em]">
          <span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-gold">
            As featured in
          </span>
          {site.press.map((name, i) => (
            <span key={name} className="flex items-center gap-3">
              {i > 0 && <span className="opacity-40">&middot;</span>}
              <span className="font-semibold text-cream">{name}</span>
            </span>
          ))}
        </div>
      </div>

      {/* Menu */}
      <section className="mx-auto max-w-[1180px] px-7 pb-16 pt-9" id="menu">
        <MenuList categories={menuLoad.categories} />
      </section>

      {/* Ordering note */}
      <div className="mx-auto max-w-[1180px] px-7 pb-16">
        <div className="flex flex-wrap items-center justify-between gap-5 rounded-[20px] border border-gold/30 bg-[#fff9ec] px-7 py-6">
          <div className="max-w-[640px]">
            <p className="font-display text-[18px] font-bold text-cocoa">How ordering works</p>
            <p className="mt-2 text-[14.5px] leading-relaxed text-cocoa/70">
              Message us on WhatsApp with your order. Mention your protein or swallow preference
              where needed. Pickup at Rákóczi tér 9. Already on Wolt or Marwa? You can order there too.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <a
              href={orderOnline}
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-full bg-palm px-6 py-3 text-[14px] font-semibold text-cream transition-all hover:-translate-y-0.5 hover:shadow-md active:scale-95"
            >
              Order Online
            </a>
            <a
              href={wa}
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-full border-2 border-palm px-6 py-3 text-[14px] font-semibold text-palm transition-all hover:-translate-y-0.5 active:scale-95"
            >
              Message on WhatsApp
            </a>
          </div>
        </div>
      </div>

    </div>
  );
}
