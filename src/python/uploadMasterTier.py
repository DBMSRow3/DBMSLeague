from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy
import mysql.connector

def main():
	config = configparser.ConfigParser()
	config.read('settings.ini')
	riotapi.set_api_key(config.get('LoL API','key'))
	riotapi.set_load_policy(LoadPolicy.lazy)
	riotapi.print_calls(False)
	regions = ['NA','EUNE','EUW','KR','LAN','JP','OCE','LAS','TR','RU','PBE']
	
	try:
		cnx = mysql.connector.connect(user=config.get('DB','username'),password=config.get('DB','password'),host=config.get('DB','host'),database=config.get('DB','database'))
		cursor = cnx.cursor()
		insertAcct = "INSERT INTO Accounts (IGN,summonerID,region) VALUES ('{}',{},'{}')"
		for region in regions:
			riotapi.set_region(region)
			league = riotapi.get_master()
			for entry in league.entries:
				summoner = entry.summoner
				insertAcctStmt = insertAcct.format(summoner.name,summoner.id,region)
				cursor.execute(insertAcctStmt)
	except mysql.connector.Error as e:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	cnx.close()
if __name__ == "__main__":
    main()