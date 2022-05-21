create table boswatch
(
	id int auto_increment primary key,
	packetTimestamp timestamp default now() not null,
	packetMode enum('fms', 'pocsag', 'zvei', 'msg') not null,
	pocsag_ric char(7) default null,
	pocsag_subric enum('1', '2', '3', '4') default null,
	pocsag_subricText enum('a', 'b', 'c', 'd') default null,
	pocsag_message text default null,
	pocsag_bitrate enum('512', '1200', '2400') default null,
	zvei_tone char(5) default null,
	fms_fms char(8) default null,
	fms_service varchar(255) default null,
	fms_country varchar(255) default null,
	fms_location varchar(255) default null,
	fms_vehicle varchar(255) default null,
	fms_status char(1) default null,
	fms_direction char(1) default null,
	fms_directionText tinytext default null,
	fms_tacticalInfo char(3) default null,
	serverName varchar(255) not null,
	serverVersion varchar(100) not null,
	serverBuildDate varchar(255) not null,
	serverBranch varchar(255) not null,
	clientName varchar(255) not null,
	clientIP varchar(255) not null,
	clientVersion varchar(100) not null,
	clientBuildDate varchar(255) not null,
	clientBranch varchar(255) not null,
	inputSource varchar(30) not null,
	frequency varchar(30) not null
);
create unique index boswatch_id_uindex
	on boswatch (id);

