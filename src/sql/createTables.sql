use donaldsa18;
#drop table Item;
#drop table Rune;
#drop table SummonerSpell;
#drop table Mastery;
#drop table ParticipantStats;
#drop table Matches;
create table Item (
	id int not null,
    name varchar(255),
    description varchar(255),
    primary key(id)
);
create table Rune (
	id int not null,
    name varchar(255),
    description varchar(255),
    primary key(id)
);
create table SummonerSpell (
	id int not null,
    name varchar(255),
    description varchar(255),
    primary key(id)
);
create table Mastery (
	id int not null,
    name varchar(255),
    description varchar(255),
    masteryTree varchar(255),
    primary key(id)
);
create table ParticipantStats (
	matchID bigint not null,
	summonerID bigint not null,
	assists	bigint,
	champLevel	bigint,
	deaths	bigint,
	firstBloodAssist	boolean,
	firstBloodKill	boolean,
	firstTowerAssist	boolean,
	firstTowerKill	boolean,
	goldEarned	bigint,
	lastItem0	bigint,
	lastItem1	bigint,
	lastItem2	bigint,
	lastItem3	bigint,
	lastItem4	bigint,
	lastItem5	bigint,
	lastItem6	bigint,
	kills	bigint,
	largestKillingSpree	bigint,
	magicDamageDealt	bigint,
	magicDamageDealtToChampions	bigint,
	magicDamageTaken	bigint,
	minionsKilled	bigint,
	physicalDamageDealt	bigint,
	physicalDamageDealtToChampions	bigint,
	physicalDamageTaken	bigint,
	totalDamageDealt	bigint,
	totalDamageDealtToChampions	bigint,
	totalDamageTaken	bigint,
	towerKills	bigint,
	trueDamageDealt	bigint,
	trueDamageDealtToChampions	bigint,
	trueDamageTaken	bigint,
	wardsPlaced	bigint,
	winner	boolean,
	role	varchar(255),
	spell1Id	int,
	spell2Id	int,
	firstItem0	bigint,
	firstItem1	bigint,
	firstItem2	bigint,
	wardsDestroyed	bigint,
	firstMasteryIDLearned	int,
	championID	int,
	highestRuneValue	varchar(255),
    primary key(matchID,summonerID)
);
create table Matches (
	mapId	int,
	matchCreation	bigint,
	matchDuration	bigint,
	matchId	bigint not null,
	matchMode	varchar(255),
	matchType	varchar(255),
	queueType	varchar(255),
	region	varchar(255),
	season	varchar(255),
	player1a	bigint,
	player2a	bigint,
	player3a	bigint,
	player4a	bigint,
	player5a	bigint,
	player1b	bigint,
	player2b	bigint,
	player3b	bigint,
	player4b	bigint,
	player5b	bigint,
	avgGameMMR	varchar(255),
    primary key(matchID)
);