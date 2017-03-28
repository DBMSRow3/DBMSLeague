from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy
import csv

def main():
    riotapi.set_api_key('INSERT-API-KEY-HERE')
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
                        print(i,row['IGN'],':',summoner.id)
                        #save results to a dictionary
                        results[row['IGN']] = summoner.id,region
                        break
                except Exception as e:
                    print(i,row['IGN'],':',region,str(e)[:25])
                    continue
    #save results to a csv
    with open('summoners.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=fields,extrasaction='ignore',dialect='excel')
        for k,v in results.items():
            writer.writerow({'summonerID':k,'IGN':v[0],'region':v[1]})
if __name__ == "__main__":
    main()
