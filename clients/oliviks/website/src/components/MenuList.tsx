'use client';

import { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { Check, Flame, Plus, SlidersHorizontal } from 'lucide-react';
import { menu, type Dish, type DishOptionGroup, type MenuCategory } from '@/data/menu';
import { useOrder, type OrderItemOption } from '@/context/OrderContext';
import { DishImage } from './DishImage';

export function MenuList({ categories: providedCategories }: { categories?: MenuCategory[] }) {
  const sourceMenu = providedCategories ?? menu;
  const [active, setActive] = useState<string>('all');
  const { addItem } = useOrder();
  const categories = active === 'all' ? sourceMenu : sourceMenu.filter((c) => c.id === active);

  return (
    <div>
      <div className="sticky top-24 z-30 -mx-5 mb-12 border-y border-cocoa/10 bg-cream/95 px-5 py-4 shadow-sm backdrop-blur sm:-mx-8 sm:px-8">
        <p className="sr-only">Category chips</p>
        <div className="mx-auto flex max-w-5xl gap-2 overflow-x-auto pb-1">
          <FilterButton id="all" label="All" active={active} onClick={setActive} />
          {sourceMenu.map((c) => (
            <FilterButton key={c.id} id={c.id} label={c.title} active={active} onClick={setActive} />
          ))}
        </div>
      </div>

      <div className="space-y-16">
        {categories.map((cat) => (
          <section key={cat.id} id={cat.id} className="scroll-mt-40">
            <div className="mb-7 flex flex-col gap-2 border-b border-cocoa/10 pb-5 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <p className="eyebrow">Menu section</p>
                <h2 className="mt-2 font-display text-3xl font-bold text-cocoa sm:text-4xl">{cat.title}</h2>
              </div>
              <p className="max-w-xl text-sm leading-relaxed text-cocoa/60 sm:text-right">{cat.blurb}</p>
            </div>
            <div className="grid gap-7 sm:grid-cols-2 lg:grid-cols-3">
              {cat.items.map((dish, i) => (
                <MenuCard key={dish.name} dish={dish} category={cat.title} delay={(i % 3) * 0.06} onAdd={addItem} />
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}

function MenuCard({
  dish,
  category,
  delay,
  onAdd,
}: {
  dish: Dish;
  category: string;
  delay: number;
  onAdd: (dish: Dish, category: string, options?: OrderItemOption[]) => void;
}) {
  const [selections, setSelections] = useState<Record<string, string>>(() => initialSelections(dish.optionGroups));
  const selectedOptions = useMemo(
    () => buildSelectedOptions(dish.optionGroups, selections),
    [dish.optionGroups, selections],
  );
  const hasOptions = Boolean(dish.optionGroups?.length);

  return (
    <motion.article
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-40px' }}
      transition={{ duration: 0.4, delay }}
      className="menu-card group flex overflow-hidden rounded-[1.75rem] border border-cocoa/10 bg-white shadow-sm ring-1 ring-transparent transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:ring-gold/25"
    >
      <div className="flex w-full flex-col">
        <div className="relative overflow-hidden">
          <DishImage src={dish.image} alt={dish.name} className="h-52 w-full transition-transform duration-500 group-hover:scale-105" />
          <div className="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-cocoa/65 to-transparent" />
          <div className="absolute left-4 top-4 flex flex-wrap gap-2">
            {dish.tags?.includes('popular') && (
              <span className="inline-flex items-center gap-1 rounded-full bg-gold px-3 py-1 text-xs font-bold text-cocoa shadow-sm">
                <Flame size={13} /> Popular
              </span>
            )}
            {hasOptions && (
              <span className="rounded-full bg-white/90 px-3 py-1 text-xs font-bold text-cocoa shadow-sm">Customizable</span>
            )}
          </div>
          {dish.price && (
            <span className="absolute bottom-4 right-4 rounded-full bg-cream px-4 py-2 text-sm font-bold text-palm shadow-lg">
              {dish.price}
            </span>
          )}
        </div>

        <div className="flex flex-1 flex-col p-5">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.18em] text-palm">{category}</p>
            <h3 className="mt-2 font-display text-xl font-bold text-cocoa">{dish.name}</h3>
            <p className="mt-2 text-sm leading-relaxed text-cocoa/70">{dish.description}</p>
          </div>

          {hasOptions && (
            <div className="customize-panel mt-5 rounded-3xl border border-gold/35 bg-gradient-to-br from-gold/15 to-cream p-4">
              <p className="mb-3 flex items-center gap-2 text-xs font-bold uppercase tracking-[0.16em] text-cocoa/70">
                <SlidersHorizontal size={14} aria-hidden="true" />
                Customize your plate
              </p>
              <div className="space-y-3">
                {dish.optionGroups?.map((group) => (
                  <OptionSelector
                    key={group.id}
                    group={group}
                    value={selections[group.id] ?? ''}
                    onChange={(value) => setSelections((current) => ({ ...current, [group.id]: value }))}
                  />
                ))}
              </div>
            </div>
          )}

          <div className="order-card-footer mt-auto pt-5">
            {hasOptions && <p className="mb-3 text-xs font-medium text-cocoa/55">Customize first, then send direct.</p>}
            <button
              type="button"
              onClick={() => onAdd(dish, category, selectedOptions)}
              className="inline-flex w-full items-center justify-center gap-2 rounded-full bg-cocoa px-4 py-3 text-sm font-bold text-cream shadow-sm transition-all hover:bg-palm hover:shadow-md focus:outline-none focus:ring-2 focus:ring-gold focus:ring-offset-2 active:scale-[0.98]"
            >
              <Plus size={17} aria-hidden="true" />
              {hasOptions ? 'Add customized order' : 'Add to order'}
            </button>
          </div>
        </div>
      </div>
    </motion.article>
  );
}

function OptionSelector({
  group,
  value,
  onChange,
}: {
  group: DishOptionGroup;
  value: string;
  onChange: (value: string) => void;
}) {
  if (group.type === 'boolean') {
    const checked = value === group.options[0]?.label;
    return (
      <label className="option-control flex cursor-pointer items-center justify-between gap-3 rounded-2xl border border-cocoa/10 bg-white px-3 py-3 text-sm text-cocoa shadow-sm transition-colors hover:border-gold/70">
        <span>
          <span className="block font-semibold">{group.label}</span>
          {group.options[0]?.priceNote && (
            <span className="block text-xs leading-relaxed text-cocoa/55">{group.options[0].priceNote}</span>
          )}
        </span>
        <span className={`grid h-6 w-6 place-items-center rounded-full border ${checked ? 'border-gold bg-gold text-cocoa' : 'border-cocoa/20 bg-cream text-transparent'}`}>
          <Check size={15} />
        </span>
        <input
          type="checkbox"
          checked={checked}
          onChange={(event) => onChange(event.target.checked ? group.options[0]?.label ?? 'Yes' : '')}
          className="sr-only accent-gold"
        />
      </label>
    );
  }

  return (
    <label className="option-control block text-sm text-cocoa">
      <span className="mb-1.5 block font-semibold">{group.label}</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="w-full rounded-2xl border border-cocoa/10 bg-white px-3 py-3 text-sm font-medium text-cocoa shadow-sm outline-none transition-colors focus:border-palm focus:ring-2 focus:ring-gold/40 accent-gold"
      >
        {group.options.map((option) => (
          <option key={option.label} value={option.label}>
            {formatOptionLabel(option)}
          </option>
        ))}
      </select>
    </label>
  );
}

function initialSelections(groups: DishOptionGroup[] = []) {
  return Object.fromEntries(
    groups.map((group) => [group.id, group.type === 'single' ? group.options[0]?.label ?? '' : '']),
  );
}

function buildSelectedOptions(groups: DishOptionGroup[] = [], selections: Record<string, string>): OrderItemOption[] {
  return groups
    .map((group) => {
      const value = selections[group.id] ?? '';
      const selectedOption = group.options.find((option) => option.label === value);

      return {
        groupId: group.id,
        groupLabel: group.label,
        value,
        priceNote: selectedOption?.priceNote,
        unitPriceFt: selectedOption?.unitPriceFt,
      };
    })
    .filter((option) => option.value);
}

function formatOptionLabel(option: { label: string; priceNote?: string }) {
  return option.priceNote ? `${option.label} — ${option.priceNote}` : option.label;
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
      type="button"
      onClick={() => onClick(id)}
      className={`shrink-0 rounded-full px-4 py-2 text-sm font-bold transition-all ${
        isActive ? 'bg-cocoa text-cream shadow-md' : 'border border-cocoa/15 bg-white text-cocoa/70 hover:border-palm hover:text-palm'
      }`}
    >
      {label}
    </button>
  );
}
