create table if not exists users
(
    chat_id   bigint            not null
        constraint users_pk
            primary key,
    "username"  text,
    full_name text,
    id        serial            not null
);

alter table users
    owner to postgres;

create unique index if not exists users_id_uindex
    on users (id);

create table if not exists senders
(
    username  text,
    city_a text,
    city_b text,
    send_date date,
    id        serial            not null primary key
);

alter table senders
    owner to postgres;

create unique index if not exists senders_id_uindex
    on senders (id);

create table if not exists takers
(
    username  text,
    city_a text,
    city_b text,
    take_date date,
    id        serial            not null primary key
);

alter table takers
    owner to postgres;

create unique index if not exists takers_id_uindex
    on takers (id);