-- Oliviks Kitchen client-editable CMS schema
-- Run this in the Supabase SQL editor after creating the project.

create extension if not exists pgcrypto;

create table if not exists public.menu_categories (
  id text primary key,
  title text not null,
  blurb text not null default '',
  sort_order integer not null default 0,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.menu_items (
  id uuid primary key default gen_random_uuid(),
  category_id text not null references public.menu_categories(id) on delete cascade,
  name text not null,
  description text not null default '',
  price_label text,
  unit_price_ft integer,
  image_url text,
  tags text[] not null default '{}',
  is_available boolean not null default true,
  is_featured boolean not null default false,
  sort_order integer not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.menu_option_groups (
  id uuid primary key default gen_random_uuid(),
  item_id uuid not null references public.menu_items(id) on delete cascade,
  group_key text not null,
  label text not null,
  type text not null check (type in ('single', 'boolean')),
  is_required boolean not null default false,
  sort_order integer not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.menu_options (
  id uuid primary key default gen_random_uuid(),
  group_id uuid not null references public.menu_option_groups(id) on delete cascade,
  label text not null,
  price_note text,
  unit_price_ft integer,
  sort_order integer not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.site_settings (
  key text primary key,
  value jsonb not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

insert into public.site_settings(key, value)
values
  ('admin_allowed_emails', '["olivikskitchen@gmail.com"]'::jsonb),
  ('cms_mode', '{"fallback":"static-menu-if-supabase-unavailable"}'::jsonb)
on conflict (key) do nothing;

alter table public.menu_categories enable row level security;
alter table public.menu_items enable row level security;
alter table public.menu_option_groups enable row level security;
alter table public.menu_options enable row level security;
alter table public.site_settings enable row level security;

-- Public read policies for active menu data. Writes are intended through Next.js
-- server routes using SUPABASE_SERVICE_ROLE_KEY after admin auth is configured.
do $$
begin
  if not exists (select 1 from pg_policies where schemaname = 'public' and tablename = 'menu_categories' and policyname = 'public read active menu categories') then
    create policy "public read active menu categories" on public.menu_categories for select using (is_active = true);
  end if;
  if not exists (select 1 from pg_policies where schemaname = 'public' and tablename = 'menu_items' and policyname = 'public read available menu items') then
    create policy "public read available menu items" on public.menu_items for select using (is_available = true);
  end if;
  if not exists (select 1 from pg_policies where schemaname = 'public' and tablename = 'menu_option_groups' and policyname = 'public read option groups') then
    create policy "public read option groups" on public.menu_option_groups for select using (true);
  end if;
  if not exists (select 1 from pg_policies where schemaname = 'public' and tablename = 'menu_options' and policyname = 'public read options') then
    create policy "public read options" on public.menu_options for select using (true);
  end if;
end $$;
