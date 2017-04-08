USE mabi;

DROP Table IF EXISTS `Item`;
CREATE TABLE `Item` (
	`id` int not null auto_increment PRIMARY KEY ,
	`item_id` varchar(255) NOT NULL,
	`name` varchar(255) NOT NULL
);

DROP Table IF EXISTS `Affix`;
CREATE TABLE `Affix` (
	`id` int not null auto_increment PRIMARY KEY,
	`affix_id` varchar(255) not null,
	`name` VARCHAR(255) NOT NULL
);

DROP Table IF EXISTS `Manual`;
CREATE TABLE `Manual` (
	`id` int not null auto_increment PRIMARY KEY,
	`name` varchar(255) not null,
	`manual_id` varchar(255) not null
);

DROP Table IF EXISTS `monster`;
CREATE TABLE `monster` (
	`id` int not null auto_increment PRIMARY KEY,
	`monster_id`varchar(255) not null,
	`desc`varchar(255) not null,
	`name`varchar(255) not null
);

DROP Table IF EXISTS `Drop Table`;
CREATE TABLE `Drop Table` (
	`id` int not null auto_increment PRIMARY KEY,
	`monster_id`varchar(255) not null,
	`drop_tier`varchar(255) not null,
	`probability`int default 0,
	`item_id`varchar(255),
	`manual_id`varchar(255),
	`prefix_id`varchar(255),
	`suffix_id`varchar(255)
);

DROP Table IF EXISTS `monster_drop`;
CREATE TABLE `monster_drop` (
	`id` int not null auto_increment PRIMARY KEY,
	`monster_id`varchar(255) not null, 
	`drop_one`varchar(255) not null,
	`drop_two`varchar(255) not null,
	`drop_three`varchar(255) not null
);