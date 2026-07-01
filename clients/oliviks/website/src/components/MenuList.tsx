'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { menu, type Dish, type MenuCategory } from '@/data/menu';
import { DishImage } from './DishImage';
import { waLink } from '@/data/site';
import { shopProductUrl } from '@/data/shopLinks';

const orderOnline = waLink("Hi Oliviks, I'd like to place an order:");

export function MenuList({ categories: providedCategories }: { categories?: MenuCategory[] }) {
  const sourceMenu = providedCategories ?? menu;
  const [active, setActive] = useState<string>('All');
  const cats = ['All', ...sourceMenu.map((c) => c.title)];
  const categories = active === 'All' ? sourceMenu : sourceMenu.filter((c) => c.title === active);

  return (
    <div>
      {/* Category chips — sticky below the pinned header bar */}
      <div className="sticky top-[66px] z-20 -mx-5 mb-12 border-b-2 border-ink/10 bg-cream/95 px-5 py-4 backdrop-blur-sm sm:-mx-8 sm:px-8">
        <div className="flex flex-wrap gap-2.5">
          {cats.map((cat) => {
            const on = cat === active;
            return (
              <button
                key={cat}
                type="button"
                onClick={() => setActive(cat)}
                className={`rounded-full border-2 px-4 py-2 font-display text-[14px] font-bold transition-all hover:-translate-y-px ${
                  on
                    ? 'border-ink bg-gold text-ink shadow-[4px_4px_0_0_#761212]'
                    : 'border-ink/15 bg-white text-cocoa/70 hover:border-palm hover:text-palm'
                }`}
              >
                {cat}
              </button>
            );
          })}
        </div>
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={active}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.18 }}
          className="space-y-16"
        >
          {categories.map((cat, catIndex) => (
            <section key={cat.id} id={cat.id} className="scroll-mt-44">
              {/* Section header — numbered, editorial */}
              <div className="mb-7 flex items-start gap-5">
                <span
                  aria-hidden="true"
                  className="mt-1 font-display text-[2.6rem] font-extrabold leading-none text-transparent [-webkit-text-stroke:2px_#FAB73A]"
                >
                  {String(catIndex + 1).padStart(2, '0')}
                </span>
                <div>
                  <h2 className="font-display text-[clamp(1.8rem,3.5vw,2.4rem)] font-extrabold leading-tight tracking-tight text-cocoa">
                    {cat.title}
                  </h2>
                  <p className="mt-1.5 max-w-[660px] text-[15.5px] text-cocoa/55">{cat.blurb}</p>
                  <div className="ankara-rule-thin mt-3.5 w-[52px]" aria-hidden="true" />
                </div>
              </div>

              <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {cat.items.map((dish, i) => (
                  <MenuCard key={dish.name} dish={dish} delay={(i % 3) * 0.06} />
                ))}
              </div>
            </section>
          ))}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

function MenuCard({ dish, delay }: { dish: Dish; delay: number }) {
  const isPopular = dish.tags?.includes('popular');
  const heat = dish.tags?.find((t) => t !== 'popular');
  // Deep-link straight to the WooCommerce product when it exists in the shop;
  // dishes without a shop product are ordered over WhatsApp.
  const productUrl = shopProductUrl(dish.name);
  const orderHref = productUrl ?? orderOnline;
  const orderLabel = productUrl ? 'Order' : 'Order on WhatsApp';

  // Protein/swallow note — pulled from description if it contains "Add a protein" or "Served with a swallow"
  const optionsNote = dish.description.includes('Add a protein from Sides')
    ? 'Add a protein from Sides: grilled chicken, turkey, mackerel, or beef'
    : dish.description.includes('Served with one swallow') || dish.description.includes('Served with a swallow')
    ? 'Served with a swallow: pounded yam or eba'
    : dish.description.includes('Contains peanuts')
    ? 'Contains peanuts'
    : null;

  // Strip the options note from the displayed description to avoid repetition
  const displayDesc = dish.description
    .replace(/ Add a protein from Sides[^.]*\.?/, '')
    .replace(/ Dried fish variant on request, subject to availability\.?/, '')
    .replace(/ Contains peanuts\.?/, '')
    .trim();

  return (
    <motion.article
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-40px' }}
      transition={{ duration: 0.4, delay }}
      className="group flex flex-col overflow-hidden rounded-2xl border-2 border-ink/10 bg-white transition-all duration-300 hover:-translate-y-1.5 hover:border-ink hover:shadow-pop-sm"
    >
      {/* Image */}
      <div className="relative h-[180px] overflow-hidden bg-stone-100">
        <DishImage
          src={dish.image}
          alt={dish.name}
          className="h-full w-full transition-transform duration-500 group-hover:scale-[1.06]"
        />
        {isPopular && (
          <span className="absolute left-3 top-3 rounded-full bg-gold px-3 py-1 font-display text-[11px] font-bold uppercase tracking-[0.1em] text-ink">
            Popular
          </span>
        )}
        {heat && (
          <span className="absolute right-3 top-3 rounded-full bg-ink/70 px-2.5 py-1 text-[11px] font-semibold tracking-[0.02em] text-cream backdrop-blur-sm">
            {heat}
          </span>
        )}
      </div>

      {/* Body */}
      <div className="flex flex-1 flex-col gap-2.5 p-5">
        <div className="flex items-baseline">
          <h3 className="font-display text-[17px] font-extrabold text-cocoa">{dish.name}</h3>
          <span className="price-leader" aria-hidden="true" />
          {dish.price && (
            <span className="shrink-0 font-display text-[15px] font-bold text-palm">
              {dish.price}
            </span>
          )}
        </div>

        <p className="flex-1 text-[13.5px] leading-[1.55] text-cocoa/55">{displayDesc}</p>

        {optionsNote && (
          <div className="rounded-lg bg-palm-50 px-3 py-1.5 text-[12px] font-medium text-palm">
            {optionsNote}
          </div>
        )}

        <a
          href={orderHref}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-1 rounded-full border-2 border-ink/10 py-2.5 text-center font-display text-[14px] font-bold text-cocoa transition-all group-hover:border-gold group-hover:bg-gold group-hover:text-ink hover:-translate-y-0.5 active:scale-95"
        >
          {orderLabel}
        </a>
      </div>
    </motion.article>
  );
}
