from __future__ import print_function
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy
from cassiopeia.type.api.exception import APIError
from mysql.connector import errorcode
from cassiopeia.type.api.store import SQLAlchemyDB
from random import shuffle
import mysql.connector
import operator
import datetime
import configparser
import time
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
	

def auto_retry(api_call_method):
	""" A decorator to automatically retry 500s (Service Unavailable) and skip 400s (Bad Request) or 404s (Not Found). """
	def call_wrapper(*args, **kwargs):
		try:
			return api_call_method(*args, **kwargs)
		except APIError as error:
			# Try Again Once
			if error.error_code in [500, 429, 503]:
				if error.error_code in [429]:
					time.sleep(10)
				elif error.error_code in [503]:
					time.sleep(60)
				pass
				try:
					print("Got a 500, trying again...")
					return api_call_method(*args, **kwargs)
				except APIError as another_error:
					if another_error.error_code in [500, 400, 404]:
						pass
					else:
						raise another_error

			# Skip
			elif error.error_code in [400, 404]:
				print("Got a 400 or 404")
				pass
			
			# Fatal
			else:
				raise error
	return call_wrapper

def getMaxRuneStat(runes):
	runeStats = {
		'ability_power': 0,
		'ability_power_per_level': 0,
		'armor': 0,
		'armor_penetration': 0,
		'armor_penetration_per_level': 0,
		'armor_per_level': 0,
		'attack_damage': 0,
		'attack_damage_per_level': 0,
		'attack_speed': 0,
		'block': 0,
		'cooldown_reduction': 0,
		'cooldown_reduction_per_level': 0,
		'critical_strike_chance': 0,
		'critical_strike_chance_per_level': 0,
		'critical_strike_damage': 0,
		'critical_strike_damage_per_level': 0,
		'dodge_chance': 0,
		'dodge_chance_per_level': 0,
		'energy': 0,
		'energy_per_level': 0,
		'energy_regen': 0,
		'energy_regen_per_level': 0,
		'gold_per_ten': 0,
		'health': 0,
		'health_per_level': 0,
		'health_regen': 0,
		'health_regen_per_level': 0,
		'life_steal': 0,
		'magic_penetration': 0,
		'magic_penetration_per_level': 0,
		'magic_resist': 0,
		'magic_resist_per_level': 0,
		'mana': 0,
		'mana_per_level': 0,
		'mana_regen': 0,
		'mana_regen_per_level': 0,
		'movespeed': 0,
		'movespeed_per_level': 0,
		'percent_ability_power': 0,
		'percent_armor': 0,
		'percent_armor_penetration': 0,
		'percent_armor_penetration_per_level': 0,
		'percent_attack_damage': 0,
		'percent_attack_speed': 0,
		'percent_attack_speed_per_level': 0,
		'percent_base_attack_damage': 0,
		'percent_base_health_regen': 0,
		'percent_base_mana_regen': 0,
		'percent_block': 0,
		'percent_bonus_armor_penetration': 0,
		'percent_bonus_health': 0,
		'percent_critical_strike_damage': 0,
		'percent_health': 0,
		'percent_health_regen': 0,
		'percent_magic_pen_per_level': 0,
		'percent_magic_penetration': 0,
		'percent_magic_resist': 0,
		'percent_mana': 0,
		'percent_mana_regen': 0,
		'percent_movespeed': 0,
		'percent_movespeed_per_level': 0,
		'percent_time_dead': 0,
		'percent_time_dead_per_level': 0,
		'percent_xp_bonus': 0,
		'spell_vamp': 0,
		'tenacity': 0,
		'time_dead': 0,
		'time_dead_per_level': 0,
		'xp_bonus': 0
	}
	for rune in runes:
		if rune is not None:
			stats = rune.stats
			if stats is not None:
				runeStats['ability_power'] += stats.ability_power
				runeStats['ability_power_per_level'] += stats.ability_power_per_level
				runeStats['armor'] += stats.armor
				runeStats['armor_penetration'] += stats.armor_penetration
				runeStats['armor_penetration_per_level'] += stats.armor_penetration_per_level
				runeStats['armor_per_level'] += stats.armor_per_level
				runeStats['attack_damage'] += stats.attack_damage
				runeStats['attack_damage_per_level'] += stats.attack_damage_per_level
				runeStats['attack_speed'] += stats.attack_speed
				runeStats['block'] += stats.block
				runeStats['cooldown_reduction'] += stats.cooldown_reduction
				runeStats['cooldown_reduction_per_level'] += stats.cooldown_reduction_per_level
				runeStats['critical_strike_chance'] += stats.critical_strike_chance
				runeStats['critical_strike_chance_per_level'] += stats.critical_strike_chance_per_level
				runeStats['critical_strike_damage'] += stats.critical_strike_damage
				runeStats['critical_strike_damage_per_level'] += stats.critical_strike_damage_per_level
				runeStats['dodge_chance'] += stats.dodge_chance
				runeStats['dodge_chance_per_level'] += stats.dodge_chance_per_level
				runeStats['energy'] += stats.energy
				runeStats['energy_per_level'] += stats.energy_per_level
				runeStats['energy_regen'] += stats.energy_regen
				runeStats['energy_regen_per_level'] += stats.energy_regen_per_level
				runeStats['gold_per_ten'] += stats.gold_per_ten
				runeStats['health'] += stats.health
				runeStats['health_per_level'] += stats.health_per_level
				runeStats['health_regen'] += stats.health_regen
				runeStats['health_regen_per_level'] += stats.health_regen_per_level
				runeStats['life_steal'] += stats.life_steal
				runeStats['magic_penetration'] += stats.magic_penetration
				runeStats['magic_penetration_per_level'] += stats.magic_penetration_per_level
				runeStats['magic_resist'] += stats.magic_resist
				runeStats['magic_resist_per_level'] += stats.magic_resist_per_level
				runeStats['mana'] += stats.mana
				runeStats['mana_per_level'] += stats.mana_per_level
				runeStats['mana_regen'] += stats.mana_regen
				runeStats['mana_regen_per_level'] += stats.mana_regen_per_level
				runeStats['movespeed'] += stats.movespeed
				runeStats['movespeed_per_level'] += stats.movespeed_per_level
				runeStats['percent_ability_power'] += stats.percent_ability_power
				runeStats['percent_armor'] += stats.percent_armor
				runeStats['percent_armor_penetration'] += stats.percent_armor_penetration
				runeStats['percent_armor_penetration_per_level'] += stats.percent_armor_penetration_per_level
				runeStats['percent_attack_damage'] += stats.percent_attack_damage
				runeStats['percent_attack_speed'] += stats.percent_attack_speed
				runeStats['percent_attack_speed_per_level'] += stats.percent_attack_speed_per_level
				runeStats['percent_base_attack_damage'] += stats.percent_base_attack_damage
				runeStats['percent_base_health_regen'] += stats.percent_base_health_regen
				runeStats['percent_base_mana_regen'] += stats.percent_base_mana_regen
				runeStats['percent_block'] += stats.percent_block
				runeStats['percent_bonus_armor_penetration'] += stats.percent_bonus_armor_penetration
				runeStats['percent_bonus_health'] += stats.percent_bonus_health
				runeStats['percent_critical_strike_damage'] += stats.percent_critical_strike_damage
				runeStats['percent_health'] += stats.percent_health
				runeStats['percent_health_regen'] += stats.percent_health_regen
				runeStats['percent_magic_pen_per_level'] += stats.percent_magic_pen_per_level
				runeStats['percent_magic_penetration'] += stats.percent_magic_penetration
				runeStats['percent_magic_resist'] += stats.percent_magic_resist
				runeStats['percent_mana'] += stats.percent_mana
				runeStats['percent_mana_regen'] += stats.percent_mana_regen
				runeStats['percent_movespeed'] += stats.percent_movespeed
				runeStats['percent_movespeed_per_level'] += stats.percent_movespeed_per_level
				runeStats['percent_time_dead'] += stats.percent_time_dead
				runeStats['percent_time_dead_per_level'] += stats.percent_time_dead_per_level
				runeStats['percent_xp_bonus'] += stats.percent_xp_bonus
				runeStats['spell_vamp'] += stats.spell_vamp
				runeStats['tenacity'] += stats.tenacity
				runeStats['time_dead'] += stats.time_dead
				runeStats['time_dead_per_level'] += stats.time_dead_per_level
				runeStats['xp_bonus'] += stats.xp_bonus
	return max(runeStats.items(), key=operator.itemgetter(1))[0]
		
def setRiotAPIAutoRetry(riotapi):
	riotapi.get_challenger = auto_retry(riotapi.get_challenger)
	riotapi.get_champion_by_id = auto_retry(riotapi.get_champion_by_id)
	riotapi.get_champion_by_name = auto_retry(riotapi.get_champion_by_name)
	riotapi.get_champion_masteries = auto_retry(riotapi.get_champion_masteries)
	riotapi.get_champion_mastery = auto_retry(riotapi.get_champion_mastery)
	riotapi.get_champion_mastery_score = auto_retry(riotapi.get_champion_mastery_score)
	riotapi.get_champions = auto_retry(riotapi.get_champions)
	riotapi.get_champions_by_name = auto_retry(riotapi.get_champions_by_name)
	riotapi.get_current_game = auto_retry(riotapi.get_current_game)
	riotapi.get_featured_games = auto_retry(riotapi.get_featured_games)
	riotapi.get_item = auto_retry(riotapi.get_item)
	riotapi.get_items = auto_retry(riotapi.get_items)
	riotapi.get_language_strings = auto_retry(riotapi.get_language_strings)
	riotapi.get_languages = auto_retry(riotapi.get_languages)
	riotapi.get_league_entries_by_summoner = auto_retry(riotapi.get_league_entries_by_summoner)
	riotapi.get_league_entries_by_team = auto_retry(riotapi.get_league_entries_by_team)
	riotapi.get_leagues_by_summoner = auto_retry(riotapi.get_leagues_by_summoner)
	riotapi.get_leagues_by_team = auto_retry(riotapi.get_leagues_by_team)
	riotapi.get_map_information = auto_retry(riotapi.get_map_information)
	riotapi.get_master = auto_retry(riotapi.get_master)
	riotapi.get_masteries = auto_retry(riotapi.get_masteries)
	riotapi.get_mastery_pages = auto_retry(riotapi.get_mastery_pages)
	riotapi.get_match = auto_retry(riotapi.get_match)
	riotapi.get_match_list = auto_retry(riotapi.get_match_list)
	riotapi.get_matches = auto_retry(riotapi.get_matches)
	riotapi.get_ranked_stats = auto_retry(riotapi.get_ranked_stats)
	riotapi.get_realm = auto_retry(riotapi.get_realm)
	riotapi.get_requests_count = auto_retry(riotapi.get_requests_count)
	riotapi.get_rune = auto_retry(riotapi.get_rune)
	riotapi.get_rune_pages = auto_retry(riotapi.get_rune_pages)
	riotapi.get_runes = auto_retry(riotapi.get_runes)
	riotapi.get_shard = auto_retry(riotapi.get_shard)
	riotapi.get_shards = auto_retry(riotapi.get_shards)
	riotapi.get_stats = auto_retry(riotapi.get_stats)
	riotapi.get_summoner_by_id = auto_retry(riotapi.get_summoner_by_id)
	riotapi.get_summoner_by_name = auto_retry(riotapi.get_summoner_by_name)
	riotapi.get_summoner_name = auto_retry(riotapi.get_summoner_name)
	riotapi.get_summoner_names = auto_retry(riotapi.get_summoner_names)
	riotapi.get_summoner_spell = auto_retry(riotapi.get_summoner_spell)
	riotapi.get_summoner_spells = auto_retry(riotapi.get_summoner_spells)
	riotapi.get_summoners_by_id = auto_retry(riotapi.get_summoners_by_id)
	riotapi.get_summoners_by_name = auto_retry(riotapi.get_summoners_by_name)
	riotapi.get_team = auto_retry(riotapi.get_team)
	riotapi.get_teams = auto_retry(riotapi.get_teams)
	riotapi.get_teams_by_summoner = auto_retry(riotapi.get_teams_by_summoner)
	riotapi.get_top_champion_masteries = auto_retry(riotapi.get_top_champion_masteries)
	riotapi.get_tournament_code = auto_retry(riotapi.get_tournament_code)
	riotapi.get_tournament_match_ids = auto_retry(riotapi.get_tournament_match_ids)
	riotapi.get_versions = auto_retry(riotapi.get_versions)
	return riotapi

def MMRToLeague(mmr):
	if mmr < 229: 
		return 'Bronze V'
	if mmr < 459: 
		return 'Bronze IV'
	if mmr < 689: 
		return 'Bronze III'
	if mmr < 919: 
		return 'Bronze II'
	if mmr < 1149: 
		return 'Bronze I'
	if mmr < 1219: 
		return 'Silver V'
	if mmr < 1289: 
		return 'Silver IV'
	if mmr < 1359: 
		return 'Silver III'
	if mmr < 1429: 
		return 'Silver II'
	if mmr < 1499: 
		return 'Silver I'
	if mmr < 1569: 
		return 'Gold V'
	if mmr < 1639: 
		return 'Gold IV'
	if mmr < 1709: 
		return 'Gold III'
	if mmr < 1779: 
		return 'Gold II'
	if mmr < 1849: 
		return 'Gold I'
	if mmr < 1919: 
		return 'Platinum V'
	if mmr < 1989: 
		return 'Platinum IV'
	if mmr < 2059: 
		return 'Platinum III'
	if mmr < 2129: 
		return 'Platinum II'
	if mmr < 2199: 
		return 'Platinum I'
	if mmr < 2269: 
		return 'Diamond V'
	if mmr < 2339: 
		return 'Diamond IV'
	if mmr < 2409: 
		return 'Diamond III'
	if mmr < 2479: 
		return 'Diamond II'
	if mmr < 2550: 
		return 'Diamond I'
	if mmr < 2915: 
		return 'Master 1'
	return 'Challenger 1'

def getFirstItems(timeline,participant):
	firstItems = []
	if timeline is not None:
		for frame in timeline.frames:
			for event in frame.events:
				if event.type.value == 'ITEM_PURCHASED' and event.participant.id == participant.id:
					if event.item is not None:
						firstItems.append(event.item.name)
					elif event.item_after is not None:
						firstItems.append(event.item_after.name)
				if len(firstItems) >= 3:
					return firstItems
	return firstItems
	
def main():
	config = configparser.ConfigParser()
	config.read('settings.ini')
	setRiotAPIAutoRetry(riotapi)
	riotapi.set_api_key(config.get('LoL API','key'))
	riotapi.set_load_policy(LoadPolicy.lazy)
	riotapi.print_calls(False)
	#db = SQLAlchemyDB("mysql+mysqlconnector", config.get('DB','host'), config.get('Riot DB','database'), config.get('DB','username'), config.get('DB','password'))
	#riotapi.set_data_store(db)
	try:
		cnx = mysql.connector.connect(user=config.get('DB','username'),password=config.get('DB','password'),host=config.get('DB','host'),database=config.get('DB','database'))
		cursor = cnx.cursor()
		queryAccounts = "SELECT summonerID,region FROM Accounts"
		cursor.execute(queryAccounts)
		summoners = set()
		summonerIDs = set()
		summonersList = []
		for account in cursor:
			acct = (account[0],account[1])
			summoners.add(acct)
			summonersList.append(acct)
			summonerIDs.add(account[0])
		shuffle(summonersList)

		insertMatches = ("INSERT INTO Matches "
						"(mapId,matchCreation,matchDuration,matchId,matchMode,matchType,queueType,season,region,"
						"player1a,player2a,player3a,player4a,player5a,player1b,player2b,player3b,player4b,player5b,avgGameMMR) "
						"VALUES ({},'{}','{}',{},'{}','{}','{}','{}','{}',{},{},{},{},{},{},{},{},{},{},'{}')")
		insertParticipant = ('INSERT INTO ParticipantStats '
							'(matchID,summonerID,assists,champLevel,deaths,firstBloodAssist,firstBloodKill,'
							'firstTowerAssist,firstTowerKill,goldEarned,lastItem0,lastItem1,lastItem2,lastItem3,'
							'lastItem4,lastItem5,lastItem6,kills,largestKillingSpree,magicDamageDealt,'
							'magicDamageDealtToChampions,magicDamageTaken,minionsKilled,physicalDamageDealt,'
							'physicalDamageDealtToChampions,physicalDamageTaken,totalDamageDealt,'
							'totalDamageDealtToChampions,totalDamageTaken,towerKills,trueDamageDealt,'
							'trueDamageDealtToChampions,trueDamageTaken,wardsPlaced,winner,role,lane,firstItem0,'
							'firstItem1,firstItem2,wardsDestroyed,championID,highestRuneValue) '
							'VALUES ({},{},{},{},{},{},{},{},{},{},"{}","{}","{}","{}","{}","{}","{}",{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},"{}","{}","{}","{}","{}",{},{},"{}")')
		summonerQuery = ("SELECT matchId FROM Matches WHERE player1a = '{}' or player2a = '{}' or player3a = '{}' "
						"or player4a = '{}' or player5a = '{}' or player1b = '{}' or player2b = '{}' or player3b = "
						"'{}' or player4b = '{}' or player5b = '{}'")
		queryParticipants = "SELECT summonerId FROM ParticipantStats WHERE matchId = '{}'"
		leagueToMMR = {'BRONZE':{'V':114,'IV':344,'III':574,'II':804,'I':1034},
			'SILVER':{'V':1184,'IV':1254,'III':1324,'II':1394,'I':1464},
			'GOLD':{'V':1534,'IV':1604,'III':1674,'II':1744,'I':1814},
			'PLATINUM':{'V':1884,'IV':1954,'III':2024,'II':2094,'I':2164},
			'DIAMOND':{'V':2234,'IV':2304,'III':2374,'II':2444,'I':2515},
			'MASTER':{'I':2733},
			'CHALLENGER':{'I':2939},
		}
		
		for summonerID, region in summonersList:
			riotapi.set_region(region)
			summonerQueryStmt = summonerQuery.format(summonerID,summonerID,summonerID,summonerID,summonerID,summonerID,summonerID,summonerID,summonerID,summonerID)
			print(summonerQueryStmt)
			cursor.execute(summonerQueryStmt)
			matches = set()
			for matchID in cursor:
				matches.add(matchID[0])
			summoner = riotapi.get_summoner_by_id(summonerID)
			matchList = summoner.match_list()
			if matchList is not None:
				for matchRef in matchList:
					match = matchRef.match()
					if match is not None:
						matchID = match.id
						if matchID not in matches:
							team1 = []
							team2 = []
							sumMMR = 0
							numParticipants = 0
							for teamMember in match.participants:
								if teamMember.summoner is not None:
									if teamMember.side.value == 100:
										team1.append(teamMember.summoner.id)
									else:
										team2.append(teamMember.summoner.id)
									memberLeague = riotapi.get_league_entries_by_summoner(teamMember.summoner)
									if memberLeague is not None:
										topLeague = None
										topMMR = 0
										for league in memberLeague:
											if leagueToMMR[league.tier.value][league.entries[0].division.value] > topMMR:
												topMMR = leagueToMMR[league.tier.value][league.entries[0].division.value]
												topLeague = league
										if topLeague.tier.value != 'UNRANKED':
											sumMMR += leagueToMMR[topLeague.tier.value][topLeague.entries[0].division.value]
											numParticipants += 1
							if numParticipants != 0:
								aveMMR = MMRToLeague(sumMMR/numParticipants)
							else:
								aveMMR = 'Unranked'
							team1.extend((0,0,0,0,0))
							team2.extend((0,0,0,0,0))
							insertMatchesStmt = insertMatches.format(match.map.value,match.creation,match.duration,match.id,match.mode.value,match.type.value,match.queue.value,match.season.value,match.region.value,team1[0],team1[1],team1[2],team1[3],team1[4],team2[0],team2[1],team2[2],team2[3],team2[4],aveMMR)
							print(insertMatchesStmt)
							cursor.execute(insertMatchesStmt)
						queryParticipantsStmt = queryParticipants.format(matchID)
						print(queryParticipantsStmt)
						cursor.execute(queryParticipantsStmt)
						participants = set()
						for participant in cursor:
							participants.add(participant[0])
						for participant in match.participants:
							thisSummoner = participant.summoner
							if thisSummoner is not None:
								thisSummonerID = thisSummoner.id
								if thisSummonerID in summonerIDs and thisSummonerID not in participants:
									pStats = participant.stats
									firstItems = getFirstItems(match.timeline,participant)
									firstItems.extend(("","",""))
									maxRuneStat = getMaxRuneStat(participant.runes)
									insertParticipantStmt = insertParticipant.format(match.id, thisSummonerID, pStats.assists, pStats.champion_level,pStats.deaths, pStats.first_blood_assist, pStats.first_blood, pStats.first_inhibitor_assist, pStats.first_inhibitor, pStats.gold_earned, pStats.item0, pStats.item1, pStats.item2, pStats.item3, pStats.item4, pStats.item5, pStats.item6, pStats.kills, pStats.largest_killing_spree, pStats.magic_damage_dealt, pStats.magic_damage_dealt_to_champions, pStats.magic_damage_taken, pStats.minion_kills, pStats.physical_damage_dealt, pStats.physical_damage_dealt_to_champions, pStats.physical_damage_taken, pStats.true_damage_dealt, pStats.true_damage_dealt_to_champions, pStats.true_damage_taken, pStats.inhibitor_kills, pStats.true_damage_dealt, pStats.true_damage_dealt_to_champions, pStats.true_damage_taken,	 pStats.vision_wards_bought, pStats.win, participant.timeline.role.value,participant.timeline.lane.value, firstItems[0],firstItems[1],firstItems[2],pStats.ward_kills,participant.champion.id,maxRuneStat)
									print(insertParticipantStmt)
									cursor.execute(insertParticipantStmt)
								
		cursor.close()
		cnx.close()
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			eprint("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			eprint("Database does not exist")
		else:
			eprint("Statement: {}\nError {}".format(cursor.statement,err))
		sys.exit(1)
	#db.close()
		
if __name__ == "__main__":
	main()
