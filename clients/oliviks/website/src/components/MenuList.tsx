'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { menu } from '@/data/menu';
import { DishImage } from './DishImage';

export function MenuList() {
  const [active, setActive] = useState<string>('all');
  const categories = active === 'all' ? menu : menu.filter((c) => c.id === active);

  return (
    <div>
      <div className="mb-10 flex flex-wrap justify-center gap-2">
        <FilterButton id="all" label="All" active={active} onClick={setActive} />
        {menu.map((c) => (
          <FilterButton key={c.id} id={c.id} label={c.title} active={active} onClick={setActive} />
        ))}
      </div>

      <div className="space-y-16">
        {categories.map((cat) => (
          <section key={cat.id} id={cat.id} className="scroll-mt-24">
            <div className="mb-6">
              <h2 className="font-display text-2xl font-bold text-cocoa sm:text-3xl">{cat.title}</h2>
              <p className="mt-1 text-cocoa/60">{cat.blurb}</p>
            </div>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {cat.items.map((dish, i) => (
                <motion.article
                  key={dish.name}
                  initial={{ opacity: 0, y: 18 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: '-40px' }}
                  transition={{ duration: 0.4, delay: (i % 3) * 0.06 }}
                  className="group overflow-hidden rounded-2xl border border-cocoa/10 bg-white shadow-sm transition-shadow hover:shadow-md"
                >
                  <DishImage src={dish.image} alt={dish.name} className="h-44 w-full" />
                  <div className="p-5">
                    <div className="flex items-start justify-between gap-3">
                      <h3 className="font-display text-lg font-semibold text-cocoa">{dish.name}</h3>
                      {dish.price && <span className="shrink-0 font-semibold text-palm">{dish.price}</span>}
                    </div>
                    <p className="mt-2 text-sm leading-relaxed text-cocoa/70">{dish.description}</p>
                    {dish.tags?.includes('popular') && (
                      <span className="mt-3 inline-block rounded-full bg-gold/20 px-3 py-1 text-xs font-semibold text-leaf">
                        Popular
                      </span>
                    )}
                  </div>
                </motion.article>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}

function FilterButton({
  id,
  label,
  active,
  onClick,
}: {
  id: string;
  label: string;
  active: string;
  onClick: (id: string) => void;
}) {
  const isActive = active === id;
  return (
    <button
      onClick={() => onClick(id)}
      className={`rounded-full px-4 py-2 text-sm font-medium transition-all ${
        isActive ? 'bg-palm text-cream' : 'border border-cocoa/15 text-cocoa/70 hover:border-palm hover:text-palm'
      }`}
    >
      {label}
    </button>
  );
}
