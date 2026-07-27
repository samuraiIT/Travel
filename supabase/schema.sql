-- Optional persistence layer. Prepared from current Supabase RLS guidance.
-- Not deployed: the connected Supabase account had no projects on 2026-07-25.

create extension if not exists pgcrypto;

create table if not exists public.travel_items (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  trip_key text not null,
  travel_date date not null,
  item_key text not null,
  status text not null check (status in ('Confirmed', 'Book', 'Backup')),
  payload jsonb not null default '{}'::jsonb,
  source_url text,
  verified_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (user_id, trip_key, item_key)
);

alter table public.travel_items enable row level security;

create policy "travel_items_select_own"
on public.travel_items for select
to authenticated
using ((select auth.uid()) = user_id);

create policy "travel_items_insert_own"
on public.travel_items for insert
to authenticated
with check ((select auth.uid()) = user_id);

create policy "travel_items_update_own"
on public.travel_items for update
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "travel_items_delete_own"
on public.travel_items for delete
to authenticated
using ((select auth.uid()) = user_id);

create index if not exists travel_items_trip_date_idx
on public.travel_items (user_id, trip_key, travel_date);
