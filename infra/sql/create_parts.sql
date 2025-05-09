
create table public.parts (
  part_id      text primary key,
  name         text not null,
  domain       text check (domain in ('MECH','CIVIL','MAT','ENV','ELEC')) not null,
  grade_min    smallint not null,
  grade_max    smallint not null,
  voltage      numeric,
  risk_notes   text,
  spec         text,
  source_hint  text
);
alter table public.parts
  enable row level security;

create policy "Allow read only"
  on public.parts
  for select
  using (true);
