'use client';

import { useMemo, useState } from 'react';
import type { ReactNode } from 'react';
import type { MenuCategory } from '@/data/menu';

type MenuSource = 'supabase' | 'static-fallback';

type Props = {
  categories: MenuCategory[];
  source: MenuSource;
};

type SaveState = 'idle' | 'saving' | 'saved' | 'error';

export function AdminMenuEditor({ categories, source }: Props) {
  const editableItems = useMemo(
    () => categories.flatMap((category) => category.items.map((item) => ({ ...item, categoryTitle: category.title }))),
    [categories],
  );
  const [adminSecret, setAdminSecret] = useState('');
  const [selectedId, setSelectedId] = useState(editableItems.find((item) => item.id)?.id ?? '');
  const selectedItem = editableItems.find((item) => item.id === selectedId) ?? editableItems[0];
  const [form, setForm] = useState({
    name: selectedItem?.name ?? '',
    description: selectedItem?.description ?? '',
    price_label: selectedItem?.price ?? '',
    image_url: selectedItem?.image ?? '',
    is_available: true,
    is_featured: selectedItem?.tags?.includes('popular') ?? false,
  });
  const [saveState, setSaveState] = useState<SaveState>('idle');
  const [message, setMessage] = useState('');

  function selectItem(itemId: string) {
    const item = editableItems.find((candidate) => candidate.id === itemId);
    setSelectedId(itemId);
    setForm({
      name: item?.name ?? '',
      description: item?.description ?? '',
      price_label: item?.price ?? '',
      image_url: item?.image ?? '',
      is_available: true,
      is_featured: item?.tags?.includes('popular') ?? false,
    });
    setSaveState('idle');
    setMessage('');
  }

  async function saveItem() {
    if (!selectedId) {
      setSaveState('error');
      setMessage('This item cannot be edited until Supabase is connected and seeded.');
      return;
    }

    setSaveState('saving');
    setMessage('Saving menu item...');

    const response = await fetch('/api/admin/menu', {
      method: 'PATCH',
      headers: {
        'content-type': 'application/json',
        'x-admin-api-secret': adminSecret,
      },
      body: JSON.stringify({
        itemId: selectedId,
        updates: {
          name: form.name.trim(),
          description: form.description.trim(),
          price_label: form.price_label.trim() || null,
          image_url: form.image_url.trim() || null,
          is_available: form.is_available,
          is_featured: form.is_featured,
        },
      }),
    });

    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
      setSaveState('error');
      setMessage(payload.error ?? 'Save failed.');
      return;
    }

    setSaveState('saved');
    setMessage(`Saved: ${payload.item?.name ?? form.name}`);
  }

  const canEdit = source === 'supabase' && Boolean(selectedId);

  return (
    <div className="grid gap-6 lg:grid-cols-[0.9fr_1.4fr]">
      <div className="rounded-3xl border border-cocoa/10 bg-cream/60 p-4">
        <div className="mb-3 flex items-center justify-between gap-3">
          <h3 className="font-display text-xl font-bold text-cocoa">Menu items</h3>
          <span className="rounded-full bg-white px-3 py-1 text-xs font-semibold text-cocoa/65">{editableItems.length} items</span>
        </div>
        <div className="max-h-[34rem] space-y-2 overflow-auto pr-1">
          {editableItems.map((item) => (
            <button
              key={`${item.categoryTitle}-${item.name}`}
              type="button"
              onClick={() => item.id && selectItem(item.id)}
              disabled={!item.id}
              className={`w-full rounded-2xl border p-3 text-left transition ${
                item.id === selectedId
                  ? 'border-palm bg-white shadow-sm'
                  : 'border-cocoa/10 bg-white/70 hover:border-gold/60 disabled:cursor-not-allowed disabled:opacity-60'
              }`}
            >
              <span className="block text-xs uppercase tracking-[0.14em] text-cocoa/45">{item.categoryTitle}</span>
              <span className="mt-1 block font-semibold text-cocoa">{item.name}</span>
              <span className="mt-1 block text-sm text-cocoa/60">{item.price ?? 'No price'}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="rounded-3xl border border-cocoa/10 bg-white p-5 shadow-sm">
        <div className="mb-5 rounded-2xl bg-gold/10 p-4 text-sm leading-relaxed text-cocoa/70">
          {canEdit
            ? 'Supabase is connected. Enter the server admin secret to update menu items.'
            : 'Editor UI is ready, but writes stay disabled until Supabase is connected and seeded. The public site remains on the safe static menu.'}
        </div>

        <label className="block text-sm font-semibold text-cocoa" htmlFor="admin-secret">
          Admin secret
        </label>
        <input
          id="admin-secret"
          type="password"
          value={adminSecret}
          onChange={(event) => setAdminSecret(event.target.value)}
          placeholder="Paste ADMIN_API_SECRET for this save session"
          className="mt-2 w-full rounded-2xl border border-cocoa/15 px-4 py-3 text-sm outline-none focus:border-palm"
        />

        <div className="mt-5 grid gap-4">
          <Field label="Dish name">
            <input
              value={form.name}
              onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))}
              className="w-full rounded-2xl border border-cocoa/15 px-4 py-3 text-sm outline-none focus:border-palm"
            />
          </Field>
          <Field label="Price label">
            <input
              value={form.price_label}
              onChange={(event) => setForm((current) => ({ ...current, price_label: event.target.value }))}
              placeholder="Example: 2,500 Ft"
              className="w-full rounded-2xl border border-cocoa/15 px-4 py-3 text-sm outline-none focus:border-palm"
            />
          </Field>
          <Field label="Description">
            <textarea
              value={form.description}
              onChange={(event) => setForm((current) => ({ ...current, description: event.target.value }))}
              rows={6}
              className="w-full rounded-2xl border border-cocoa/15 px-4 py-3 text-sm leading-relaxed outline-none focus:border-palm"
            />
          </Field>
          <Field label="Image URL or path">
            <input
              value={form.image_url}
              onChange={(event) => setForm((current) => ({ ...current, image_url: event.target.value }))}
              placeholder="/images/legacy/example.png"
              className="w-full rounded-2xl border border-cocoa/15 px-4 py-3 text-sm outline-none focus:border-palm"
            />
          </Field>

          <div className="grid gap-3 sm:grid-cols-2">
            <label className="flex items-center gap-3 rounded-2xl border border-cocoa/10 p-4 text-sm font-semibold text-cocoa">
              <input
                type="checkbox"
                checked={form.is_available}
                onChange={(event) => setForm((current) => ({ ...current, is_available: event.target.checked }))}
              />
              Available on menu
            </label>
            <label className="flex items-center gap-3 rounded-2xl border border-cocoa/10 p-4 text-sm font-semibold text-cocoa">
              <input
                type="checkbox"
                checked={form.is_featured}
                onChange={(event) => setForm((current) => ({ ...current, is_featured: event.target.checked }))}
              />
              Featured/popular
            </label>
          </div>
        </div>

        <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center">
          <button
            type="button"
            onClick={saveItem}
            disabled={!canEdit || !adminSecret || saveState === 'saving'}
            className="btn-primary disabled:cursor-not-allowed disabled:opacity-50"
          >
            {saveState === 'saving' ? 'Saving...' : 'Save item'}
          </button>
          {message ? <p className={`text-sm ${saveState === 'error' ? 'text-red-700' : 'text-cocoa/65'}`}>{message}</p> : null}
        </div>
      </div>
    </div>
  );
}

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm font-semibold text-cocoa">{label}</span>
      {children}
    </label>
  );
}
