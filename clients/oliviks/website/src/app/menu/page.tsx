import type { Metadata } from 'next';
import { MenuList } from '@/components/MenuList';
import { OrderCTA, CallButton } from '@/components/OrderCTA';
import { getMenuCategories } from '@/lib/cms/menu';

export const metadata: Metadata = {
  title: 'Menu',
  description:
    "What Oliviks cooks in Budapest: jollof rice, fried rice, egusi, oha, ogbono, suya, plantain, puff puff, snacks, and drinks.",
};

export default async function MenuPage() {
  const menuLoad = await getMenuCategories();

  return (
    <div className="bg-cream">
      <section className="border-b border-cocoa/10">
        <div className="container-x py-16 sm:py-20">
          <div className="max-w-2xl">
            <span className="eyebrow">Our dishes</span>
            <h1 className="mt-4 font-display text-5xl font-bold leading-tight text-cocoa sm:text-6xl">
              What We Cook
            </h1>
            <p className="mt-5 text-lg leading-relaxed text-cocoa/70">
              Jollof rice, egusi, suya, plantain, puff puff, and more. Order direct for pickup at Rákóczi tér 9, or message the kitchen for catering.
            </p>
            <div className="mt-7 flex flex-wrap gap-3">
              <OrderCTA />
              <CallButton />
            </div>
          </div>
        </div>
      </section>

      <section className="container-x py-14">
        <MenuList categories={menuLoad.categories} />
      </section>
    </div>
  );
}
