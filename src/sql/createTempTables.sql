use donaldsa18;
START TRANSACTION;
#LOCK TABLES ParticipantStats WRITE, Accounts WRITE, Smurfs WRITE, Matches WRITE, Item WRITE;

CREATE TEMPORARY TABLE firstItemUsage AS 
    SELECT
        firstItem0 as firstItem, championID, summonerID
    FROM
        ParticipantStats
	UNION ALL
    SELECT 
        firstItem1, championID, summonerID
    FROM
        ParticipantStats
	UNION ALL
    SELECT 
        firstItem2, championID, summonerID
    FROM
        ParticipantStats;
            
CREATE TEMPORARY TABLE firstItemCount AS
    SELECT 
        firstItem, COUNT(*) AS count, summonerID, championID
    FROM
        firstItemUsage
	WHERE firstItem != ''
    GROUP BY firstItem , summonerID , championID
    ORDER BY count DESC;
    

CREATE TEMPORARY TABLE firstItem AS
    SELECT 
		i.id as firstItemID, count,summonerID,championID
	FROM
		firstItemCount fi
	JOIN Item i ON i.name = fi.firstItem
	GROUP BY summonerID,championID;
ALTER TABLE firstItem ADD INDEX(summonerID,championID);


CREATE TEMPORARY TABLE lastItem0Count AS (
SELECT 
    lastItem0, COUNT(lastItem0) AS count, summonerID, championID
FROM
    ParticipantStats
GROUP BY lastItem0 , summonerID , championID
ORDER BY count DESC
);

CREATE TEMPORARY TABLE lastItem1Count AS (
SELECT 
    lastItem1, COUNT(lastItem1) AS count, summonerID, championID
FROM
    ParticipantStats
GROUP BY lastItem1 , summonerID , championID
ORDER BY count DESC
);

CREATE TEMPORARY TABLE lastItem2Count AS (
SELECT 
    lastItem2, COUNT(lastItem2) AS count, summonerID, championID
FROM
    ParticipantStats
GROUP BY lastItem2 , summonerID , championID
ORDER BY count DESC
);

CREATE TEMPORARY TABLE lastItem3Count AS (
SELECT 
    lastItem3, COUNT(lastItem3) AS count, summonerID, championID
FROM
    ParticipantStats
GROUP BY lastItem3 , summonerID , championID
ORDER BY count DESC
);

CREATE TEMPORARY TABLE lastItem4Count AS (
SELECT 
    lastItem4, COUNT(lastItem4) AS count, summonerID, championID
FROM
    ParticipantStats
GROUP BY lastItem4 , summonerID , championID
ORDER BY count DESC
);

CREATE TEMPORARY TABLE lastItem5Count AS (
SELECT 
    lastItem5, COUNT(lastItem5) AS count, summonerID, championID
FROM
    ParticipantStats
GROUP BY lastItem5 , summonerID , championID
ORDER BY count DESC
);

CREATE TEMPORARY TABLE lastItem6Count AS (
SELECT lastItem6, COUNT(lastItem6) AS count, summonerID, championID FROM
    ParticipantStats
GROUP BY lastItem6 , summonerID , championID
ORDER BY count DESC);


CREATE TEMPORARY TABLE lastItem0 AS (SELECT 
        i0.id AS lastItem0ID, summonerID, championID
    FROM
        lastItem0Count li
            JOIN
        Item AS i0 ON i0.name = lastItem0
    GROUP BY li.summonerID, li.championID);

CREATE TEMPORARY TABLE lastItem1 AS (SELECT 
        i1.id AS lastItem1ID, summonerID, championID
    FROM
        lastItem1Count li
            JOIN
        Item AS i1 ON i1.name = lastItem1
    GROUP BY li.summonerID, li.championID);

CREATE TEMPORARY TABLE lastItem2 AS (SELECT 
        i2.id AS lastItem2ID, summonerID, championID
    FROM
        lastItem2Count li
            JOIN
        Item AS i2 ON i2.name = lastItem2
    GROUP BY li.summonerID, li.championID);

CREATE TEMPORARY TABLE lastItem3 AS (SELECT 
        i3.id AS lastItem3ID, summonerID, championID
    FROM
        lastItem3Count li
            JOIN
        Item AS i3 ON i3.name = lastItem3
    GROUP BY li.summonerID, li.championID);

CREATE TEMPORARY TABLE lastItem4 AS (SELECT 
        i4.id AS lastItem4ID, summonerID, championID
    FROM
        lastItem4Count li
            JOIN
        Item AS i4 ON i4.name = lastItem4
    GROUP BY li.summonerID, li.championID);

CREATE TEMPORARY TABLE lastItem5 AS (SELECT 
        i5.id AS lastItem5ID, summonerID, championID
    FROM
        lastItem5Count li
            JOIN
        Item AS i5 ON i5.name = lastItem5
    GROUP BY li.summonerID, li.championID);

CREATE TEMPORARY TABLE lastItem6 AS (SELECT 
        i6.id AS lastItem6ID, summonerID, championID
    FROM
        lastItem6Count li
            JOIN
        Item AS i6 ON i6.name = lastItem6
    GROUP BY li.summonerID, li.championID);
ALTER TABLE lastItem0 ADD INDEX(summonerID,championID);
ALTER TABLE lastItem1 ADD INDEX(summonerID,championID);
ALTER TABLE lastItem2 ADD INDEX(summonerID,championID);
ALTER TABLE lastItem3 ADD INDEX(summonerID,championID);
ALTER TABLE lastItem4 ADD INDEX(summonerID,championID);
ALTER TABLE lastItem5 ADD INDEX(summonerID,championID);
ALTER TABLE lastItem6 ADD INDEX(summonerID,championID);

CREATE TEMPORARY TABLE LaneRoleCount AS (
SELECT 
	lane,
	role,
    summonerID,
    championID,
    count(*) as count
FROM ParticipantStats
GROUP BY lane,role,summonerID,championID
ORDER BY count DESC
);


CREATE TEMPORARY TABLE LaneRole AS (
SELECT role,
    lane,
    summonerID,
    championID
    FROM
    LaneRoleCount 
     GROUP BY summonerID, championID);
ALTER TABLE LaneRole ADD INDEX(summonerID,championID);


CREATE TEMPORARY TABLE AvgDPS AS (
SELECT summonerID,
	championID,
	ROUND(AVG(totalDamageDealtToChampions)) as aveDamage,
    ROUND(AVG(TIME_TO_SEC(mat.matchDuration))) AS aveDuration
FROM ParticipantStats p
JOIN
    Matches AS mat ON mat.matchId = p.matchId
GROUP BY summonerID,championID);
ALTER TABLE AvgDPS ADD INDEX(summonerID,championID);

CREATE TEMPORARY TABLE AggregatePlayerStats AS (
SELECT
	sm.primaryName,
    p.summonerID,
    p.championID,
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
GROUP BY p.summonerID,p.championID
);
ALTER TABLE AggregatePlayerStats ADD INDEX(summonerID,championID);

CREATE TABLE ChampionStats AS (
SELECT 
    p.primaryName,
    p.championID,
    p.k,
    p.d,
    p.aveChampLevel,
    p.aveGold,
    p.largestKillingSpree,
    p.aveWardsPlaced,
    p.aveMinionsKilled,
    p.winRatio,
    p.totalWins,
    p.totalLosses,
    p.totalMatches,
    p.aveTowerKills,
    (adps.aveDamage/adps.aveDuration) AS aveDPSToChampions,
    lr.role,
    lr.lane,
    fi.firstItemID AS firstItemID,
    i0.lastItem0ID AS lastItem0ID,
    i1.lastItem1ID AS lastItem1ID,
    i2.lastItem2ID AS lastItem2ID,
    i3.lastItem3ID AS lastItem3ID,
    i4.lastItem4ID AS lastItem4ID,
    i5.lastItem5ID AS lastItem5ID,
    i6.lastItem6ID AS lastItem6ID
FROM
    AggregatePlayerStats as p
        JOIN
    firstItem AS fi ON fi.summonerID = p.summonerID 
		AND fi.championID = p.championID
        JOIN
    lastItem0 AS i0 ON i0.summonerID = p.summonerID
        AND i0.championID = p.championID
        JOIN
    lastItem1 AS i1 ON i1.summonerID = p.summonerID
        AND i1.championID = p.championID
        JOIN
    lastItem2 AS i2 ON i2.summonerID = p.summonerID
        AND i2.championID = p.championID
        JOIN
    lastItem3 AS i3 ON i3.summonerID = p.summonerID
        AND i3.championID = p.championID
        JOIN
    lastItem4 AS i4 ON i4.summonerID = p.summonerID
        AND i4.championID = p.championID
        JOIN
    lastItem5 AS i5 ON i5.summonerID = p.summonerID
        AND i5.championID = p.championID
        JOIN
    lastItem6 AS i6 ON i6.summonerID = p.summonerID
        AND i6.championID = p.championID
        JOIN
    AvgDPS as adps ON adps.summonerID = p.summonerID
		AND adps.championID = p.championID
        JOIN
    LaneRole AS lr ON lr.summonerID = p.summonerID
        AND lr.championID = p.championID
GROUP BY p.summonerID, p.championID);
DROP TABLE firstItemUsage;
DROP TABLE firstItem;
DROP TABLE firstItemCount;
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
DROP TABLE AggregatePlayerStats;
COMMIT;