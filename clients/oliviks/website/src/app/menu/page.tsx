import type { Metadata } from 'next';
import { MenuList } from '@/components/MenuList';
import { OrderCTA, CallButton } from '@/components/OrderCTA';

export const metadata: Metadata = {
  title: 'Menu',
  description:
    "Explore Oliviks Kitchen's Nigerian menu in Budapest: jollof rice, egusi soup, suya, fried yam, puff puff, plantain, and more.",
};

export default function MenuPage() {
  return (
    <div className="container-x py-16">
      <header className="mx-auto max-w-2xl text-center">
        <span className="eyebrow">Our dishes</span>
        <h1 className="mt-3 font-display text-4xl font-bold text-cocoa sm:text-5xl">Explore the Menu</h1>
        <p className="mt-4 text-lg text-cocoa/70">
          Authentic Nigerian cuisine, made fresh daily. Order for pickup at Rákóczi tér 9.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <OrderCTA label="Order on WhatsApp" />
          <CallButton />
        </div>
      </header>

      <div className="mt-14">
        <MenuList />
      </div>
    </div>
  );
}
