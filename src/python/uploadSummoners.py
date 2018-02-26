import csv
import mysql.connector

def main():
	try:
		cnx = mysql.connector.connect(user='donaldsa18',password='donaldsa18',host='egr4',database='donaldsa18')
		cursor = cnx.cursor()
		insertStmt = "INSERT INTO Accounts (IGN,summonerID,region) VALUES ('{}','{}','{}')"
		with open('summoners.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				if len(row) == 3:
					sqlCmd = insertStmt.format(row['IGN'],row['summonerID'],row['Region'])
					print(sqlCmd)
					cursor.execute(sqlCmd)
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