drop table if exists entries;

drop table if exists main_table;
create table main_table (
  id integer primary key autoincrement,
  company text not null,
  email text not null,
  password text not null,
  rule text not null,
  first_name text not null,
  last_name text not null,
  patronymic text not null,
  tel_number text not null
);

drop table if exists chat_table;
create table chat_table (
  id integer primary key autoincrement,
  message text not null,
  user_id text not null,
  datte text not null,
  timme text not null,
  foreign key (user_id) references main_table (id)
);

--Таблица не верна, нужно сделать атрибут для КАЖДОГО поля в договоре
drop table if exists contract_table;
create table contract_table (
  id integer primary key autoincrement,
  user_id not null,
  --fields not null,
  date_create text not null,
  version text not null,
  date_last_change not null,
  foreign key (user_id) references main_table (id)
);

drop table if exists left_chats_table;
create table left_chats_table (
  id integer primary key autoincrement,
  userr text not null,
  last_message text not null,
  foreign key (userr) references main_table (id)
  foreign key (last_message) references chat_table (message)
);

drop table if exists dash_table;
create table dash_table (
  id integer primary key autoincrement,
  contract_number text not null,
  customer text not null,
  provider text not null,
  date_create text  not null,
  date_last_change text  not null,
  --остаток срока подписания будет генериться на месте
  status text not null,
  foreign key (date_last_change) references cotract_table (date_last_change),
  foreign key (date_create) references cotract_table (date_create)
);
