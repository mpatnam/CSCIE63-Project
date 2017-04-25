# write tweets to a csv file
import urllib.request, json
import os
import sys

pwd=os.getcwd()
file=pwd+"\\data\\Tweets.20170424.csv"
writer = open(file, 'w')
writer.write('ID,Symbol,CreateTime,Body,Sentiment\n')

stocks=["AAPL", "TSLA", "FB", "TWTR"]
#stocks=["AAPL"]
rows=0

try:
    for stock in stocks:
        url="https://api.stocktwits.com/api/2/streams/symbol/"+stock+".json"
        with urllib.request.urlopen(url) as urlobj:
            json_data = json.loads(urlobj.read().decode())
            for message in json_data['messages']:
                #print('    {0},{1},{2},{3}'.format(message['id'], symbol['symbol'], message['created_at'], message['body']))
                # replace ',' with '#' as output is csv file
                # replace unprintable chars with unicode chars
                adj_body=message['body'].replace(",","#").encode(sys.stdout.encoding, errors='replace')
                sentiment="None"
                if message['entities']['sentiment']:
                    sentiment=message['entities']['sentiment']['basic']
                # build the csv row
                row=str(message['id'])+","+stock+","+message['created_at']+","+str(adj_body)+","+sentiment+"\n"
                print(row)
                writer.write(row)
                rows=rows+1
            
finally:
    writer.close()
            
print("Written {0} rows to file: {1}".format(rows, file))

