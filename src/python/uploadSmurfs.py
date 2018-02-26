from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy
import csv
import configparser
import mysql.connector

def main():
	config = configparser.ConfigParser()
	config.read('settings.ini')
	riotapi.set_api_key(config.get('LoL API','key'))
	riotapi.set_load_policy(LoadPolicy.lazy)
	riotapi.print_calls(False)

	#list of LoL regions sorted by popularity
	regions = ['NA','EUNE','EUW','KR','LAN','JP','OCE','LAS','TR','RU','PBE']
	cnx = mysql.connector.connect(user=config.get('DB','username'),password=config.get('DB','password'),host=config.get('DB','host'),database=config.get('DB','database'))
	cursor = cnx.cursor()
	queryAcct = "SELECT summonerID FROM Accounts WHERE summonerID = {}"
	insertAcct = "INSERT INTO Accounts (IGN,summonerID,region) VALUES ('{}','{}','{}')"
	insertSmurf = 'INSERT INTO Smurfs (primaryName,smurfID) VALUES ("{}",{})'
	with open('smurfs.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			for region in regions:
				riotapi.set_region(region)
				try:
					#execute api call
					print("IGN:{}\tRegion:{}".format(row['SmurfName'].ljust(20),region))
					summoner = riotapi.get_summoner_by_name(row['SmurfName'])
					if summoner is not None:
						insertSmurfStmt = insertSmurf.format(row['PlayerName'])
						print(insertSmurfStmt)
						cursor.execute(insertSmurfStmt)
						queryAcctStmt = queryAcct.format(summoner.id)
						print(queryAcctStmt)
						cursor.execute(queryAcctStmt)
						needToInsert = True
						for summonerID in cursor:
							if summonerID == summoner.id:
								needToInsert = False
						if needToInsert == True:
							insertAcctStmt = insertAcct.format(row['SmurfName'],summoner.id,region)
							print(insertAcctStmt)
							cursor.execute(insertAcctStmt)
						break
				except Exception as e:
					continue
	
if __name__ == "__main__":
	main()
