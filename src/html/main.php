<!DOCTYPE html>
<html><head><title>League of Legends Database Thing</title><link rel="stylesheet" type="text/css" href="style.css"></head>
<center><h1>League of Legends Pro Database</h1></center>
<div id="cont">
<div style="overflow-x:auto;">
        <table>
        <thead>
            <tr>
				<td>matchID</td>
				<td>summonerID</td>
				<td>assists</td>
				<td>champLevel</td>
				<td>deaths</td>
				<td>firstBloodAssists</td>
				<td>firstBloodKill</td>
				<td>firstTowerAssists</td>
				<td>firstTowerKill</td>
				<td>goldEarned</td>
				<td>lastItem0</td>
				<td>lastItem1</td>
				<td>lastItem2</td>
				<td>lastItem3</td>
				<td>lastItem4</td>
				<td>lastItem5</td>
				<td>lastItem6</td>
				<td>kills</td>
				<td>largestKillingSpree</td>
				<td>magicDamageDealt</td>
				<td>magicDamageDealtToChampions</td>
				<td>magicDamageTaken</td>
				<td>minionsKilled</td>
				<td>physicalDamageDealt</td>
				<td>physicalDamageDealtToChampions</td>
				<td>physicalDamageTaken</td>
				<td>totalDamageDealt</td>
				<td>totalDamageDealtToChampions</td>
				<td>totalDamageTaken</td>
				<td>towerKills</td>
				<td>trueDamageDealtToChampions</td>
				<td> trueDamageTaken</td>
				<td>wardsPlaced</td>
				<td>winner</td>
				<td>role</td>
				<td>firstItem0</td>
				<td>firstItem1</td>
				<td>firstItem2</td>
				<td>wardsDestroyed</td>
				<td>championID</td>
				<td>highestRuneValue</td>
				<td>lane</td>
            </tr>
        </thead>
        <tbody>
			<?php
			$servername = "69.147.233.138:3306";
			$username = "web";
			$password = "gitgud";
			$dbname = "league";

			// Create connection
			$conn = new mysqli($servername, $username, $password, $dbname);
			// Check connection
			if (!$conn) {
				die("Connection failed: " . mysqli_connect_error());
			} 

			$sql = "SELECT * FROM participantstats limit 5";
			$result = mysqli_query($conn, $sql);

			if (mysqli_num_rows($result) > 0) {
				// output data of each row
				while($row = mysqli_fetch_assoc($result)) {
					?>
					<tr>
						<td><?php echo $row['matchID'];?></td>
						<td><?php echo $row['summonerID'];?></td>
						<td><?php echo $row['assists'];?></td>
						<td><?php echo $row['champLevel'];?></td>
						<td><?php echo $row['deaths'];?></td>
						<td><?php echo $row['firstBloodAssists'];?></td>
						<td><?php echo $row['firstBloodKill'];?></td>
						<td><?php echo $row['firstTowerAssists'];?></td>
						<td><?php echo $row['firstTowerKill'];?></td>
						<td><?php echo $row['goldEarned'];?></td>
						<td><?php echo $row['lastItem0'];?></td>
						<td><?php echo $row['lastItem1'];?></td>
						<td><?php echo $row['lastItem2'];?></td>
						<td><?php echo $row['lastItem3'];?></td>
						<td><?php echo $row['lastItem4'];?></td>
						<td><?php echo $row['lastItem5'];?></td>
						<td><?php echo $row['lastItem6'];?></td>
						<td><?php echo $row['kills'];?></td>
						<td><?php echo $row['largestKillingSpree'];?></td>
						<td><?php echo $row['magicDamageDealt'];?></td>
						<td><?php echo $row['magicDamageDealtToChampions'];?></td>
						<td><?php echo $row['magicDamageTaken'];?></td>
						<td><?php echo $row['minionsKilled'];?></td>
						<td><?php echo $row['physicalDamageDealt'];?></td>
						<td><?php echo $row['physicalDamageDealtToChampions'];?></td>
						<td><?php echo $row['physicalDamageTaken'];?></td>
						<td><?php echo $row['totalDamageDealt'];?></td>
						<td><?php echo $row['totalDamageDealtToChampions'];?></td>
						<td><?php echo $row['totalDamageTaken'];?></td>
						<td><?php echo $row['towerKills'];?></td>
						<td><?php echo $row['trueDamageDealtToChampions'];?></td>
						<td><?php echo $row[' trueDamageTaken'];?></td>
						<td><?php echo $row['wardsPlaced'];?></td>
						<td><?php echo $row['winner'];?></td>
						<td><?php echo $row['role'];?></td>
						<td><?php echo $row['firstItem0'];?></td>
						<td><?php echo $row['firstItem1'];?></td>
						<td><?php echo $row['firstItem2'];?></td>
						<td><?php echo $row['wardsDestroyed'];?></td>
						<td><?php echo $row['championID'];?></td>
						<td><?php echo $row['highestRuneValue'];?></td>
						<td><?php echo $row['lane'];?></td>
					</tr>
					<?php
				}
			} else {
				echo "0 results";
			}
			mysqli_close($conn);
			?>
		</tbody>
		</table>
</div>
</div>
<br>
<hr>
<div id = "info">
	<center><p class="info">This website was created for educational use for the study of Database Management Systems &copy 2018. All rights reserved. Patent Pending.</p></center>
</div>
</div>
</body>
</html>