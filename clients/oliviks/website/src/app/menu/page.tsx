import type { Metadata } from 'next';
import { MenuList } from '@/components/MenuList';
import { OrderCTA, CallButton } from '@/components/OrderCTA';

export const metadata: Metadata = {
  title: 'Menu',
  description:
    "What Oliviks cooks in Budapest: jollof rice, fried rice, egusi, oha, ogbono, suya, plantain, puff puff, snacks, and drinks.",
};

export default function MenuPage() {
  return (
    <div className="container-x py-16">
      <header className="mx-auto max-w-3xl text-center">
        <span className="eyebrow">Our dishes</span>
        <h1 className="mt-3 font-display text-4xl font-bold text-cocoa sm:text-5xl">What We Cook</h1>
        <p className="mt-4 text-lg leading-relaxed text-cocoa/70">
          The menu runs deep. Jollof rice and fried rice. Egusi, oha, and ogbono soup with swallow. Suya.
          Pepper soup. Fried yam, plantain, and puff puff. Each dish is made fresh and served the way it would be
          served in Nigeria. If you are new, start light and build up. If you already know what you want, you know
          where to find it. Order direct for pickup, message us on WhatsApp, or come in to Rákóczi tér 9.
        </p>
        <p className="mt-4 rounded-2xl border border-gold/40 bg-gold/10 px-4 py-3 text-sm font-medium text-cocoa/75">
          First time here? Start with jollof, plantain, and puff puff.
        </p>
        <p className="mt-3 text-sm text-cocoa/60">
          Pepper soup and Abacha and Fish are shown as placeholders while final details are confirmed.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <OrderCTA />
          <CallButton />
        </div>
      </header>

      <div className="mt-14">
        <MenuList />
      </div>
    </div>
  );
}
