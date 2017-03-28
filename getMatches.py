from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy
import mysql.connector
try:
	cnx = mysql.connector.connect(user='username',password='password',host='localhost',database='lol')
	cursor = cnx.cursor()
	query = ("SELECT summonerID,region FROM summoners")
	cursor.execute(query)
	summoners = []
	for (summonerID) in cursor:
		summoners.append(summonerID[0],summonerID[1])
	shuffle(summoners)
	for summonerID, region in summoners:
		query = ("SELECT MatchReference FROM matches where p1a = '%s' or p2a = '%s' or p3a = '%s' or p4a = '%s' or p5a = '%s' or p1b = '%s' or p2b = '%s' or p3b = '%s' or p4b = '%s' or p5b = '%s'")
		cursor.execute(query,summonerID,summonerID,summonerID,summonerID,summonerID,summonerID,summonerID,summonerID,summonerID)
		summoner = riotapi.get_summoner_by_id(summonerID)
		matchList = summoner.match_list()
		for i, matchRef in enumerate(match_list):
			match = matchRef.match()
			insert = ("INSERT INTO matches "
					"(matchId,mapId,matchCreation,matchDuration,matchType,queueType,season,region,p1a,p2a,p3a,p4a,p5a,p1b,p2b,p3b,p4b,p5b)"
					"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
			
			
			teams = match.teams
			for participant in match.participants:
				teams[participant.summoner_id] = participant.teamId
			team1ID = teams[0].teamId
			team2ID = teams[1].teamId
			team1 = []
			team2 = []
			for pID,tID in teams.items():
				if tID = team1ID:
					team1.append(pID)
				if tID = team2ID:
					team2.append(pID)
			for i in range(0,5-len(team1)):
				team1.append(None)
			for i in range(0,5-len(team2)):
				team2.append(None)
			cursor.execute(insert,match.matchId,match.mapId,match.matchCreation,match.matchDuration,match.matchType,match.queueType,match.season,match.region,team1[0],team1[1],team1[2],team1[3],team1[4],team2[0],team2[1],team2[2],team2[3],team2[4])
			for participant in match.participants:
				if participant.summoner_id in summoners:
					insert = ("INSERT INTO ParticipantStats"	"(matchId,summonerId,championId,assists,champLevel,combatPlayerScore,deaths,doubleKills,firstBloodAssist,firstBloodKill,firstInhibitorAssist,firstInhibitorKill,firstTowerAssist,firstTowerKill,goldEarned,goldSpent,inhibitorKills,item0,item1,item2,item3,item4,item5,item6,killingSprees,kills,largestCriticalStrike,largestKillingSpree,largestMultiKill,magicDamageDealt,magicDamageDealtToChampions,magicDamageTaken,minionsKilled,neutralMinionsKilled,neutralMinionsKilledEnemyJungle,neutralMinionsKilledTeamJungle,nodeCapture,nodeCaptureAssist,nodeNeutralize,nodeNeutralizeAssist,objectivePlayerScore,pentaKills,physicalDamageDealt,physicalDamageDealtToChampions,physicalDamageTaken,,sightWardsBoughtInGame,teamObjective,totalDamageDealt,totalDamageDealtToChampions,totalDamageTaken,totalHeal,totalPlayerScore,totalScoreRank,totalTimeCrowdControlDealt,totalUnitsHealed,towerKills,tripleKills,trueDamageDealt,trueDamageDealtToChampions,trueDamageTaken,unrealKills,visionWardsBoughtInGame,wardsKilled,wardsPlaced,winner)"
					"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
					pStsts = participant.stats
					cursor.execute(insert, match.matchId, participant.summoner_id, participant.championId, pStats.assists, pStats.champLevel, pStats.combatPlayerScore, pStats.deaths, pStats.doubleKills, pStats.firstBloodAssist, pStats.firstBloodKill, pStats.firstInhibitorAssist, pStats.firstInhibitorKill, pStats.firstTowerAssist, pStats.firstTowerKill, pStats.goldEarned, pStats.goldSpent, pStats.inhibitorKills, pStats.item0, pStats.item1, pStats.item2, pStats.item3, pStats.item4, pStats.item5, pStats.item6, pStats.killingSprees, pStats.kills, pStats.largestCriticalStrike, pStats.largestKillingSpree, pStats.largestMultiKill, pStats.magicDamageDealt, pStats.magicDamageDealtToChampions, pStats.magicDamageTaken, pStats.minionsKilled, pStats.neutralMinionsKilled, pStats.neutralMinionsKilledEnemyJungle, pStats.neutralMinionsKilledTeamJungle, pStats.nodeCapture, pStats.nodeCaptureAssist, pStats.nodeNeutralize, pStats.nodeNeutralizeAssist, pStats.objectivePlayerScore, pStats.pentaKills, pStats.physicalDamageDealt, pStats.physicalDamageDealtToChampions, pStats.physicalDamageTaken, pStats.quadraKills, pStats.sightWardsBoughtInGame, pStats.teamObjective, pStats.totalDamageDealt, pStats.totalDamageDealtToChampions, pStats.totalDamageTaken, pStats.totalHeal, pStats.totalPlayerScore, pStats.totalScoreRank, pStats.totalTimeCrowdControlDealt, pStats.totalUnitsHealed, pStats.towerKills, pStats.tripleKills, pStats.trueDamageDealt, pStats.trueDamageDealtToChampions, pStats.trueDamageTaken, pStats.unrealKills, pStats.visionWardsBoughtInGame, pStats.wardsKilled, pStats.wardsPlaced, pStats.winner)
					#insert stats here
					
	cursor.close()
	cnx.close()
except mysql.connector.Error as e:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
else:
	cnx.close()
