'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { menu, type Dish, type MenuCategory } from '@/data/menu';
import { DishImage } from './DishImage';
import { waLink } from '@/data/site';

const orderOnline = waLink("Hi Oliviks, I'd like to place an order:");

export function MenuList({ categories: providedCategories }: { categories?: MenuCategory[] }) {
  const sourceMenu = providedCategories ?? menu;
  const [active, setActive] = useState<string>('All');
  const cats = ['All', ...sourceMenu.map((c) => c.title)];
  const categories = active === 'All' ? sourceMenu : sourceMenu.filter((c) => c.title === active);

  return (
    <div>
      {/* Category chips */}
      <div className="sticky top-[74px] z-20 -mx-7 mb-10 border-b border-cocoa/10 bg-cream/95 px-7 py-4 backdrop-blur-sm">
        <div className="flex flex-wrap gap-2.5">
          {cats.map((cat) => {
            const on = cat === active;
            return (
              <button
                key={cat}
                type="button"
                onClick={() => setActive(cat)}
                className={`rounded-full border-2 px-4 py-2 text-[14px] font-semibold transition-all hover:-translate-y-px ${
                  on
                    ? 'border-palm bg-palm text-cream shadow-md'
                    : 'border-cocoa/20 bg-white text-cocoa/70 hover:border-palm hover:text-palm'
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
          className="space-y-12"
        >
          {categories.map((cat) => (
            <section key={cat.id} id={cat.id} className="scroll-mt-40">
              {/* Section header */}
              <div className="mb-6">
                <h2 className="font-display text-[32px] font-extrabold leading-tight tracking-tight text-cocoa">
                  {cat.title}
                </h2>
                <p className="mt-1.5 max-w-[660px] text-[16px] text-cocoa/55">{cat.blurb}</p>
                <div className="mt-3.5 h-[3px] w-[46px] rounded-full bg-gradient-to-r from-gold to-gold/50" />
              </div>

              {/* Cards grid */}
              <div className="grid gap-[22px] sm:grid-cols-2 lg:grid-cols-3">
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

  // Protein/swallow note — pulled from description if it contains "Add a protein" or "Served with a swallow"
  const optionsNote = dish.description.includes('Add a protein from Sides')
    ? 'Add a protein from Sides — grilled chicken, turkey, mackerel, or beef'
    : dish.description.includes('Served with one swallow') || dish.description.includes('Served with a swallow')
    ? 'Served with a swallow — pounded yam or eba'
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
      className="group flex flex-col overflow-hidden rounded-[20px] border bg-white shadow-sm transition-all duration-300 hover:-translate-y-[7px] hover:border-gold/50 hover:shadow-lg"
      style={{ borderColor: 'rgba(225,227,219,0.6)' }}
    >
      {/* Image */}
      <div className="relative h-[172px] overflow-hidden bg-[#eef0ea]">
        <DishImage
          src={dish.image}
          alt={dish.name}
          className="h-full w-full transition-transform duration-500 group-hover:scale-[1.06]"
        />
        {isPopular && (
          <span className="absolute left-3 top-3 rounded-full bg-gold px-3 py-1 text-[12px] font-semibold text-cocoa">
            Popular
          </span>
        )}
        {heat && (
          <span className="absolute right-3 top-3 rounded-full bg-black/60 px-2.5 py-1 text-[11px] font-semibold tracking-[0.02em] text-white backdrop-blur-sm">
            {heat}
          </span>
        )}
      </div>

      {/* Body */}
      <div className="flex flex-1 flex-col gap-2 p-[18px_20px]">
        <div className="flex items-baseline justify-between gap-3">
          <h3 className="font-display text-[18px] font-bold text-cocoa">{dish.name}</h3>
          {dish.price && (
            <span className="shrink-0 font-display text-[15px] font-bold text-palm">
              {dish.price}
            </span>
          )}
        </div>

        <p className="flex-1 text-[13.5px] leading-[1.5] text-cocoa/55">{displayDesc}</p>

        {optionsNote && (
          <div className="rounded-[6px] bg-[#faecec] px-3 py-1.5 text-[12px] text-palm">
            {optionsNote}
          </div>
        )}

        <a
          href={orderOnline}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-1.5 rounded-full bg-gold py-2.5 text-center text-[14px] font-semibold text-cocoa shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md active:scale-95"
        >
          Order
        </a>
      </div>
    </motion.article>
  );
}
