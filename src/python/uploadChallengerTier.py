from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy
from cassiopeia.type.api.exception import APIError
import mysql.connector
import configparser
from mysql.connector import errorcode
from random import shuffle
import unicodedata

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
	
def main():
	config = configparser.ConfigParser()
	config.read('settings.ini')
	riotapi.set_api_key(config.get('LoL API','key'))
	riotapi.set_load_policy(LoadPolicy.lazy)
	riotapi.print_calls(False)
	regions = ['NA','EUNE','EUW','KR','LAN','JP','OCE','LAS','TR','RU']
	setRiotAPIAutoRetry(riotapi)
	try:
		cnx = mysql.connector.connect(user=config.get('DB','username'),password=config.get('DB','password'),host=config.get('DB','host'),database=config.get('DB','database'))
		cursor = cnx.cursor()
		insertAcct = "INSERT INTO Accounts (IGN,summonerID,region) VALUES ('{}',{},'{}')"
		queryAcct = "SELECT summonerID,region FROM Accounts"
		cursor.execute(queryAcct)
		accounts = set()
		for row in cursor:
			accounts.add((row[0],row[1]))
		for region in regions:
			riotapi.set_region(region)
			league = riotapi.get_challenger()
			entries = league.entries
			shuffle(entries)
			for entry in entries:
				summoner = entry.summoner
				try:
					if (summoner.id,region) not in accounts:
						insertAcctStmt = insertAcct.format(str(summoner.name),summoner.id,region)
						print(insertAcctStmt)
						cursor.execute(insertAcctStmt)
					else:
						print("Skipping {} because alreadfy in DB".format(str(summoner.name)))
				except UnicodeEncodeError as err:
					print("Skipping {} due to unicode".format(unicodedata.normalize('NFKD',summoner.name).encode('ascii','ignore')))
					pass
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	cnx.close()
if __name__ == "__main__":
    main()