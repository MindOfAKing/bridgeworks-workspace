-- Wedding RSVP storage.
-- Run once in the Supabase SQL editor.
--
-- Row level security is on with no policies, so anon and authenticated roles
-- cannot read or write. Every insert goes through the server using the
-- service role key, which bypasses RLS. The guest list is never exposed
-- to the browser.

create table if not exists public.rsvps (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  guest_name text not null,
  email text,
  attending boolean not null,
  party_size integer not null default 1,
  party_names text,
  at_ceremony boolean not null default false,
  at_reception boolean not null default false,
  dietary text,
  message text
);

create index if not exists rsvps_created_at_idx on public.rsvps (created_at desc);

alter table public.rsvps enable row level security;

-- Resubmissions are stored as new rows, so count the latest row per guest:
--   with latest as (
--     select distinct on (lower(guest_name)) *
--     from public.rsvps
--     order by lower(guest_name), created_at desc
--   )
--   select count(*) filter (where attending) as yes,
--          count(*) filter (where not attending) as no,
--          coalesce(sum(party_size) filter (where attending), 0) as heads
--   from latest;
