create table if not exists genre(
	id serial primary key,
	name varchar(30) not null unique
	);

create table if not exists executor(
	id serial primary key,
	name varchar(200) not null
	);

create table if not exists album(
	id serial primary key,
	name varchar(250) not null,
	year_of_release integer check(year_of_release > 0)
	);

create table if not exists track(
	id serial primary key,
	name varchar(250) not null,
	duration integer check(duration > 0),
	id_album integer references album(id)
	);

create table if not exists collection(
	id serial primary key,
	name varchar(250) not null,
	year_of_release integer check(year_of_release > 0)
	);

create table if not exists genre_executor(
	id_genre integer references genre(id),
	id_executor integer references executor(id),
	constraint genre_executor_pk primary key (id_genre, id_executor)
	);

create table if not exists executor_album(
	id_executor integer references executor(id),
	id_album integer references album(id),
	constraint executor_album_pk primary key (id_executor, id_album)
	);
	
create table if not exists collection_track(
	id_collection integer references collection(id),
	id_track integer references track(id),
	constraint collection_track_pk primary key (id_collection, id_track)
	);
