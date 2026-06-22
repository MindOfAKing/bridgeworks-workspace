import type { Metadata } from 'next';
import { CheckCircle2, MessageCircle, SlidersHorizontal, Utensils } from 'lucide-react';
import { MenuList } from '@/components/MenuList';
import { OrderCTA, CallButton } from '@/components/OrderCTA';
import { DeliveryStickers } from '@/components/DeliveryStickers';
import { getMenuCategories } from '@/lib/cms/menu';

export const metadata: Metadata = {
  title: 'Menu',
  description:
    "What Oliviks cooks in Budapest: jollof rice, fried rice, egusi, oha, ogbono, suya, plantain, puff puff, snacks, and drinks.",
};

const orderSteps = [
  {
    icon: Utensils,
    title: 'Choose your plate',
    text: 'Browse Nigerian rice plates, soups, sides, snacks, and drinks.',
  },
  {
    icon: SlidersHorizontal,
    title: 'Customize options',
    text: 'Select protein, swallow, or extra hot stew where the dish allows it.',
  },
  {
    icon: MessageCircle,
    title: 'Send to WhatsApp',
    text: 'Your order opens in WhatsApp so Oliviks can confirm pickup and final total.',
  },
];

export default async function MenuPage() {
  const menuLoad = await getMenuCategories();

  return (
    <div className="bg-cream">
      <section className="container-x py-12 sm:py-16">
        <div className="menu-hero-panel overflow-hidden rounded-[2rem] bg-cocoa text-cream shadow-xl">
          <div className="grid gap-8 p-7 sm:p-10 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
            <div>
              <span className="inline-flex rounded-full bg-gold px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] text-cocoa">
                Our dishes
              </span>
              <h1 className="mt-5 font-display text-4xl font-bold leading-tight sm:text-6xl">What We Cook</h1>
              <p className="mt-5 max-w-2xl text-lg leading-relaxed text-cream/82">
                Jollof rice, fried rice, egusi, oha, ogbono soup with swallow, suya, pepper soup, fried yam,
                plantain, puff puff, snacks, and drinks. Order direct in under a minute, then Oliviks confirms
                pickup and final total on WhatsApp.
              </p>
              <div className="mt-7 flex flex-wrap gap-3">
                <OrderCTA />
                <CallButton />
              </div>
              <div className="mt-5">
                <DeliveryStickers tone="dark" />
              </div>
            </div>

            <div className="rounded-3xl border border-cream/15 bg-white/10 p-5 backdrop-blur">
              <p className="font-display text-2xl font-bold text-cream">Easy direct ordering</p>
              <div className="mt-5 grid gap-3">
                {orderSteps.map(({ icon: Icon, title, text }) => (
                  <article key={title} className="rounded-2xl bg-cream p-4 text-cocoa">
                    <div className="flex gap-3">
                      <Icon className="mt-0.5 shrink-0 text-palm" size={20} />
                      <div>
                        <h2 className="font-display text-lg font-bold">{title}</h2>
                        <p className="mt-1 text-sm leading-relaxed text-cocoa/68">{text}</p>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
              <p className="mt-5 flex items-start gap-2 rounded-2xl border border-gold/40 bg-gold/15 px-4 py-3 text-sm text-cream/90">
                <CheckCircle2 className="mt-0.5 shrink-0 text-gold" size={17} />
                First time here? Start with jollof, plantain, and puff puff.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="container-x pb-16">
        <p className="mx-auto max-w-3xl rounded-2xl border border-cocoa/10 bg-white px-4 py-3 text-center text-sm text-cocoa/60 shadow-sm">
          Pepper soup remains marked Price TBC because no product price was found on oliviks.com or in the export scan. Abacha and Fish uses recovered export order pricing.
        </p>
        <div className="mt-10">
          <MenuList categories={menuLoad.categories} />
        </div>
      </section>
    </div>
  );
}
