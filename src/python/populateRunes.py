from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy
import csv
import urllib
import configparser
import mysql.connector

def main():
	config = configparser.ConfigParser()
	config.read('settings.ini')
	riotapi.set_api_key(config.get('LoL API','key'))
	riotapi.set_load_policy(LoadPolicy.lazy)
	riotapi.print_calls(False)
	riotapi.set_region('NA')
	try:
		cnx = mysql.connector.connect(user=config.get('DB','username'),password=config.get('DB','password'),host=config.get('DB','host'),database=config.get('DB','database'))
		cursor = cnx.cursor()
		insertRune = 'INSERT INTO Rune (id,name,description) VALUES ({},"{}","{}")'
		runes = riotapi.get_runes()
		for rune in runes:
			imageurl = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/img/rune/'+rune.image.link
			destPath = 'img/rune-'+str(rune.id)+'.png'
			try:
				urllib.urlretrieve(imageurl,destPath)
			except IOError as err:
				print("Error retreiving rune-"+str(rune.id)+'.png')
			insertRuneStmt = insertRune.format(rune.id,rune.name,rune.description)
			print(insertRuneStmt)
			cursor.execute(insertRuneStmt)
		
		cursor.close()
		cnx.close()
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cnx.close()
if __name__ == "__main__":
	main()
