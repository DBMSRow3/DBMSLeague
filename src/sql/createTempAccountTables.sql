use donaldsa18;
START TRANSACTION;

CREATE TEMPORARY TABLE firstItemUsage AS 
    SELECT
        firstItem0 as firstItem, summonerID
    FROM
        ParticipantStats
	UNION ALL
    SELECT 
        firstItem1, summonerID
    FROM
        ParticipantStats
	UNION ALL
    SELECT 
        firstItem2, summonerID
    FROM
        ParticipantStats;
            

CREATE TEMPORARY TABLE firstItemCount AS
    SELECT 
        fiu.firstItem, COUNT(*) AS count, s.primaryName
    FROM
        firstItemUsage fiu
        JOIN SmurfAccounts s ON s.smurfID = fiu.summonerID
	WHERE fiu.firstItem != ''
    GROUP BY fiu.firstItem , s.primaryName
    ORDER BY count DESC;
    

CREATE TEMPORARY TABLE firstItem AS
    SELECT 
		i.id as firstItemID, count, fi.primaryName
	FROM
		firstItemCount fi
	JOIN Item i ON i.name = fi.firstItem
	GROUP BY fi.primaryName;
ALTER TABLE firstItem ADD INDEX(primaryName);


CREATE TEMPORARY TABLE lastItem0Count AS (
SELECT 
    lastItem0, COUNT(lastItem0) AS count, s.primaryName
FROM
    ParticipantStats p
	JOIN SmurfAccounts s ON s.smurfID = p.summonerID
GROUP BY lastItem0, s.primaryName
ORDER BY count DESC
);

CREATE TEMPORARY TABLE lastItem1Count AS (
SELECT 
    lastItem1, COUNT(lastItem1) AS count, s.primaryName
FROM
    ParticipantStats p
	JOIN SmurfAccounts s ON s.smurfID = p.summonerID
GROUP BY lastItem1, s.primaryName
ORDER BY count DESC
);

CREATE TEMPORARY TABLE lastItem2Count AS (
SELECT 
    lastItem2, COUNT(lastItem2) AS count, s.primaryName
FROM
    ParticipantStats p
	JOIN SmurfAccounts s ON s.smurfID = p.summonerID
GROUP BY lastItem2, s.primaryName
ORDER BY count DESC
);

CREATE TEMPORARY TABLE lastItem3Count AS (
SELECT 
    lastItem3, COUNT(lastItem3) AS count, s.primaryName
FROM
    ParticipantStats p
	JOIN SmurfAccounts s ON s.smurfID = p.summonerID
GROUP BY lastItem3, s.primaryName
ORDER BY count DESC
);

CREATE TEMPORARY TABLE lastItem4Count AS (
SELECT 
    lastItem4, COUNT(lastItem4) AS count, s.primaryName
FROM
    ParticipantStats p
	JOIN SmurfAccounts s ON s.smurfID = p.summonerID
GROUP BY lastItem4, s.primaryName
ORDER BY count DESC
);

CREATE TEMPORARY TABLE lastItem5Count AS (
SELECT 
    lastItem5, COUNT(lastItem5) AS count, s.primaryName
FROM
    ParticipantStats p
	JOIN SmurfAccounts s ON s.smurfID = p.summonerID
GROUP BY lastItem5, s.primaryName
ORDER BY count DESC
);

CREATE TEMPORARY TABLE lastItem6Count AS (
SELECT 
    lastItem6, COUNT(lastItem6) AS count, s.primaryName
FROM
    ParticipantStats p
	JOIN SmurfAccounts s ON s.smurfID = p.summonerID
GROUP BY lastItem6, s.primaryName
ORDER BY count DESC
);


CREATE TEMPORARY TABLE lastItem0 AS (SELECT 
        i.id AS lastItem0ID, li.primaryName
    FROM
        lastItem0Count li
            JOIN
        Item AS i ON i.name = lastItem0
    GROUP BY li.primaryName);

CREATE TEMPORARY TABLE lastItem1 AS (SELECT 
        i.id AS lastItem1ID, li.primaryName
    FROM
        lastItem1Count li
            JOIN
        Item AS i ON i.name = lastItem1
    GROUP BY li.primaryName);

CREATE TEMPORARY TABLE lastItem2 AS (SELECT 
        i.id AS lastItem2ID, li.primaryName
    FROM
        lastItem2Count li
            JOIN
        Item AS i ON i.name = lastItem2
    GROUP BY li.primaryName);

CREATE TEMPORARY TABLE lastItem3 AS (SELECT 
        i.id AS lastItem3ID, li.primaryName
    FROM
        lastItem3Count li
            JOIN
        Item AS i ON i.name = lastItem3
    GROUP BY li.primaryName);

CREATE TEMPORARY TABLE lastItem4 AS (SELECT 
        i.id AS lastItem4ID, li.primaryName
    FROM
        lastItem4Count li
            JOIN
        Item AS i ON i.name = lastItem4
    GROUP BY li.primaryName);

CREATE TEMPORARY TABLE lastItem5 AS (SELECT 
        i.id AS lastItem5ID, li.primaryName
    FROM
        lastItem5Count li
            JOIN
        Item AS i ON i.name = lastItem5
    GROUP BY li.primaryName);

CREATE TEMPORARY TABLE lastItem6 AS (SELECT 
        i.id AS lastItem6ID, li.primaryName
    FROM
        lastItem6Count li
            JOIN
        Item AS i ON i.name = lastItem6
    GROUP BY li.primaryName);
ALTER TABLE lastItem0 ADD INDEX(primaryName);
ALTER TABLE lastItem1 ADD INDEX(primaryName);
ALTER TABLE lastItem2 ADD INDEX(primaryName);
ALTER TABLE lastItem3 ADD INDEX(primaryName);
ALTER TABLE lastItem4 ADD INDEX(primaryName);
ALTER TABLE lastItem5 ADD INDEX(primaryName);
ALTER TABLE lastItem6 ADD INDEX(primaryName);

CREATE TEMPORARY TABLE LaneRoleCount AS (
SELECT 
	lane,
	role,
    s.primaryName,
    count(*) as count
FROM ParticipantStats p
	JOIN SmurfAccounts s ON s.smurfID = p.summonerID
GROUP BY lane,role,s.primaryName
ORDER BY count DESC
);


CREATE TEMPORARY TABLE LaneRole AS (
SELECT role,
    lane,
    primaryName
FROM
    LaneRoleCount 
GROUP BY primaryName);
ALTER TABLE LaneRole ADD INDEX(primaryName);


CREATE TEMPORARY TABLE AvgDPS AS (
SELECT s.primaryName,
	ROUND(AVG(totalDamageDealtToChampions)) as aveDamage,
    ROUND(AVG(TIME_TO_SEC(mat.matchDuration))) AS aveDuration
FROM ParticipantStats p
JOIN
	SmurfAccounts s ON s.smurfID = p.summonerID
JOIN
    Matches AS mat ON mat.matchId = p.matchId
GROUP BY s.primaryName);
ALTER TABLE AvgDPS ADD INDEX(primaryName);


CREATE TEMPORARY TABLE AggregatePlayerStats AS (
SELECT
	sm.primaryName,
	SUM(p.kills) / SUM(p.assists) AS k,
    SUM(p.deaths) / SUM(p.assists) AS d,
    ROUND(AVG(p.champLevel)) AS aveChampLevel,
    ROUND(AVG(p.goldEarned)) AS aveGold,
    MAX(p.largestKillingSpree) AS largestKillingSpree,
    AVG(p.wardsPlaced) AS aveWardsPlaced,
    AVG(p.minionsKilled) AS aveMinionsKilled,
    AVG(p.winner) AS winRatio,
    SUM(p.winner) AS totalWins,
    COUNT(p.summonerID) - SUM(p.winner) AS totalLosses,
    COUNT(p.summonerID) as totalMatches,
    AVG(towerKills) AS aveTowerKills
FROM ParticipantStats p
	JOIN
SmurfAccounts sm ON sm.smurfID = p.summonerID
GROUP BY sm.primaryName
);
ALTER TABLE AggregatePlayerStats ADD INDEX(primaryName);

CREATE TABLE SmurfAccountStats AS (
SELECT 
    sm.primaryName,
    aps.k,
    aps.d,
    aps.aveChampLevel,
    aps.aveGold,
    aps.largestKillingSpree,
    aps.aveWardsPlaced,
    aps.aveMinionsKilled,
    aps.winRatio,
    aps.totalWins,
    aps.totalLosses,
    aps.totalMatches,
    aps.aveTowerKills,
    (adps.aveDamage/adps.aveDuration) AS aveDPSToChampions,
    lr.role,
    lr.lane,
    sm.firstItemID AS firstItemID,
    i0.lastItem0ID AS lastItem0ID,
    i1.lastItem1ID AS lastItem1ID,
    i2.lastItem2ID AS lastItem2ID,
    i3.lastItem3ID AS lastItem3ID,
    i4.lastItem4ID AS lastItem4ID,
    i5.lastItem5ID AS lastItem5ID,
    i6.lastItem6ID AS lastItem6ID
FROM
    firstItem AS sm
        JOIN
    lastItem0 AS i0 ON i0.primaryName = sm.primaryName
        JOIN
    lastItem1 AS i1 ON i1.primaryName = sm.primaryName
        JOIN
    lastItem2 AS i2 ON i2.primaryName = sm.primaryName
        JOIN
    lastItem3 AS i3 ON i3.primaryName = sm.primaryName
        JOIN
    lastItem4 AS i4 ON i4.primaryName = sm.primaryName
        JOIN
    lastItem5 AS i5 ON i5.primaryName = sm.primaryName
        JOIN
    lastItem6 AS i6 ON i6.primaryName = sm.primaryName
        JOIN
    AvgDPS as adps ON adps.primaryName = sm.primaryName
        JOIN
    LaneRole AS lr ON lr.primaryName = sm.primaryName
		JOIN
	AggregatePlayerStats as aps ON aps.primaryName = sm.primaryName
GROUP BY sm.primaryName);
DROP TABLE firstItemUsage;
DROP TABLE firstItem;
DROP TABLE firstItemCount;
DROP TABLE AggregatePlayerStats;
DROP TABLE lastItem0Count;
DROP TABLE lastItem1Count;
DROP TABLE lastItem2Count;
DROP TABLE lastItem3Count;
DROP TABLE lastItem4Count;
DROP TABLE lastItem5Count;
DROP TABLE lastItem6Count;
DROP TABLE lastItem0;
DROP TABLE lastItem1;
DROP TABLE lastItem2;
DROP TABLE lastItem3;
DROP TABLE lastItem4;
DROP TABLE lastItem5;
DROP TABLE lastItem6;
DROP TABLE LaneRoleCount;
DROP TABLE LaneRole;
DROP TABLE AvgDPS;
COMMIT;