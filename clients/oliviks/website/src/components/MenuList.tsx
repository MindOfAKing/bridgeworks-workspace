'use client';

import { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { Plus, SlidersHorizontal } from 'lucide-react';
import { menu, type Dish, type DishOptionGroup } from '@/data/menu';
import { useOrder, type OrderItemOption } from '@/context/OrderContext';
import { DishImage } from './DishImage';

export function MenuList() {
  const [active, setActive] = useState<string>('all');
  const { addItem } = useOrder();
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
      className="group overflow-hidden rounded-2xl border border-cocoa/10 bg-white shadow-sm transition-shadow hover:shadow-md"
    >
      <DishImage src={dish.image} alt={dish.name} className="h-44 w-full" />
      <div className="flex min-h-[15rem] flex-col p-5">
        <div className="flex items-start justify-between gap-3">
          <h3 className="font-display text-lg font-semibold text-cocoa">{dish.name}</h3>
          {dish.price && <span className="shrink-0 text-right font-semibold text-palm">{dish.price}</span>}
        </div>
        <p className="mt-2 text-sm leading-relaxed text-cocoa/70">{dish.description}</p>
        {dish.tags?.includes('popular') && (
          <span className="mt-3 inline-block w-fit rounded-full bg-gold/20 px-3 py-1 text-xs font-semibold text-leaf">
            Popular
          </span>
        )}

        {hasOptions && (
          <div className="mt-4 rounded-2xl border border-gold/30 bg-gold/10 p-3">
            <p className="mb-3 flex items-center gap-2 text-xs font-bold uppercase tracking-[0.16em] text-cocoa/65">
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

        <button
          type="button"
          onClick={() => onAdd(dish, category, selectedOptions)}
          className="mt-auto inline-flex w-full items-center justify-center gap-2 rounded-full bg-cocoa px-4 py-3 text-sm font-semibold text-cream transition-colors hover:bg-palm focus:outline-none focus:ring-2 focus:ring-gold focus:ring-offset-2"
        >
          <Plus size={17} aria-hidden="true" />
          {hasOptions ? 'Add customized order' : 'Order'}
        </button>
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
    return (
      <label className="flex items-center justify-between gap-3 rounded-xl bg-white/70 px-3 py-2 text-sm text-cocoa">
        <span>
          <span className="block">{group.label}</span>
          {group.options[0]?.priceNote && (
            <span className="block text-xs text-cocoa/55">{group.options[0].priceNote}</span>
          )}
        </span>
        <input
          type="checkbox"
          checked={value === group.options[0]?.label}
          onChange={(event) => onChange(event.target.checked ? group.options[0]?.label ?? 'Yes' : '')}
          className="h-4 w-4 accent-palm"
        />
      </label>
    );
  }

  return (
    <label className="block text-sm text-cocoa">
      <span className="mb-1 block font-semibold">{group.label}</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="w-full rounded-xl border border-cocoa/10 bg-white px-3 py-2 text-sm text-cocoa outline-none transition-colors focus:border-palm focus:ring-2 focus:ring-gold/40"
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
      onClick={() => onClick(id)}
      className={`rounded-full px-4 py-2 text-sm font-medium transition-all ${
        isActive ? 'bg-palm text-cream' : 'border border-cocoa/15 text-cocoa/70 hover:border-palm hover:text-palm'
      }`}
    >
      {label}
    </button>
  );
}
