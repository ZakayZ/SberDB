create schema if not exists mh;

create table if not exists mh.champion
(
    champion_id integer PRIMARY KEY,
    champion_nm varchar(50) NOT NULL
);

create table if not exists mh.server
(
    server_id integer PRIMARY KEY,
    server_nm varchar(50) NOT NULL
);

create table if not exists mh.item
(
    item_id   integer PRIMARY KEY,
    item_nm   varchar(50) NOT NULL,
    item_cost integer     NOT NULL
);

create table if not exists mh.itemlist
(
    itemlist_id integer,
    slot_num    integer CHECK (slot_num BETWEEN 1 AND 6),
    item_id     integer,
    PRIMARY KEY (itemlist_id, slot_num),
    FOREIGN KEY (item_id) references mh.item (item_id) on DELETE SET NULL
);

create table if not exists mh.queue
(
    queue_id integer PRIMARY KEY,
    queue_nm varchar(100) NOT NULL
);

create table if not exists mh.user
(
    user_id   integer PRIMARY KEY,
    user_nm   varchar(50) NOT NULL,
    server_id integer,
    FOREIGN KEY (server_id) references mh.server (server_id) on DELETE SET NULL
);

create table if not exists mh.rating
(
    user_id           integer,
    league_points_cnt integer CHECK (league_points_cnt >= 0) DEFAULT 0,
    FOREIGN KEY (user_id) references mh.user (user_id) on DELETE SET NULL
);

create table if not exists mh.rating_history
(
    user_id           integer,
    league_points_cnt integer CHECK (league_points_cnt >= 0) DEFAULT 0,
    update_ddtm       timestamp NOT NULL,
    FOREIGN KEY (user_id) references mh.server (server_id) on DELETE SET NULL
);

create table if not exists mh.match
(
    match_id              integer PRIMARY KEY,
    server_id             integer,
    queue_id              integer,
    start_dttm            timestamp NOT NULL,
    duration_sec          interval  NOT NULL,
    blue_team_victory_flg boolean   NOT NULL,
    FOREIGN KEY (server_id) references mh.server (server_id) on DELETE SET NULL,
    FOREIGN KEY (queue_id) references mh.queue (queue_id) on DELETE SET NULL
);


-- this abomination is due to postgres incapability to implement match partial functionality!!!!!!
create table if not exists mh.itemlist_padding
(
    itemlist_id   integer PRIMARY KEY
);

create table if not exists mh.summoner
(
    match_id      integer,
    user_id       integer,
    champion_id   integer,
    itemlist_id   integer,
    kill_cnt      integer CHECK (kill_cnt >= 0)              DEFAULT 0,
    death_cnt     integer CHECK (death_cnt >= 0)             DEFAULT 0,
    assist_cnt    integer CHECK (assist_cnt >= 0)            DEFAULT 0,
    creep_stat    integer CHECK (creep_stat >= 0)            DEFAULT 0,
    level_cnt     integer CHECK (level_cnt BETWEEN 1 AND 18) DEFAULT 1,
    blue_team_flg boolean NOT NULL,
    FOREIGN KEY (match_id) references mh.match (match_id) on DELETE SET NULL,
    FOREIGN KEY (user_id) references mh.user (user_id) on DELETE SET NULL,
    FOREIGN KEY (champion_id) references mh.champion (champion_id) on DELETE SET NULL,
    FOREIGN KEY (itemlist_id) references mh.itemlist_padding (itemlist_id) on DELETE SET NULL
--     FOREIGN KEY (itemlist_id) references mh.itemlist (itemlist_id) match partial on DELETE SET NULL
);
