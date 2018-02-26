from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy
import csv

def main():
	config = configparser.ConfigParser()
	config.read('settings.ini')
    riotapi.set_api_key(config.get('LoL API','key'))
    riotapi.set_load_policy(LoadPolicy.lazy)
    riotapi.print_calls(False)
    fields = ['summonerID','IGN','region']

    #list of LoL regions sorted by popularity
    regions = ['NA','EUNE','EUW','KR','LAN','JP','OCE','LAS','TR','RU','PBE']
    results = {}
    i=0
    with open('pros.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            i = i+1
            #try every region
            for region in regions:
                riotapi.set_region(region)
                try:
                    #execute api call
                    summoner = riotapi.get_summoner_by_name(row['IGN'])
                    if summoner:
                        print("Num:{}\tIGN:{}\tID:{}\tRegion:{}".format(str(i).ljust(4),row['IGN'].ljust(20),str(summoner.id).ljust(10),region.ljust(4)))
                        #save results to a dictionary
                        results[row['IGN']] = summoner.id,region
                        break
                except Exception as e:
                    print("Num:{}\tIGN:{}\tError:{}\tRegion:{}".format(str(i).ljust(4),row['IGN'].ljust(20),str(e)[22:25],region.ljust(4)))
                    continue
    #save results to a csv
    with open('summoners.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=fields,extrasaction='ignore',dialect='excel')
        for k,v in results.items():
            writer.writerow({'summonerID':k,'IGN':v[0],'region':v[1]})
if __name__ == "__main__":
    main()
