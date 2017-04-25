# download tweets from stocktwits
import urllib.request, json
import os
import sys
import datetime
import time

# fetch date and seq for csv file purpose
today=datetime.datetime.today().strftime('%Y%m%d')
seq=datetime.datetime.today().strftime('%H%M%S')

#data_dir=os.getcwd()
data_dir="C:\\Users\\mpatnam\\Documents\\GitHub\\CSCIE63\\CSCIE63-Big-Data-Analytics\\Project\\CSCIE63-Project\\Data"
file=data_dir+"\\StockTwits."+today+"."+seq+".csv"
writer = open(file, 'w')
writer.write('ID,Symbol,CreateTime,Body,Sentiment\n')

stocks=["AAPL", "TSLA", "FB", "TWTR"]
#stocks=["AAPL"]
rows=0

try:
    for stock in stocks:
        url="https://api.stocktwits.com/api/2/streams/symbol/"+stock+".json"
        print('------------------------------------------------------------------------------')
        print(url)
        with urllib.request.urlopen(url) as urlobj:
            json_data = json.loads(urlobj.read().decode())
            #symbol=json_data['symbol']
            cursor=json_data['cursor']
            more=cursor['more']
            since=cursor['since']
            maxid=cursor['max']
            iter=0
            while more and iter < 48:
                #time.sleep(1) #sec
                print('iteration:{0} {1},{2},{3},{4}'.format(iter, stock, more, since, maxid))
                url="https://api.stocktwits.com/api/2/streams/symbol/"+stock+".json?max="+str(maxid)
                urlobj2=urllib.request.urlopen(url)
                json_data = json.loads(urlobj2.read().decode())
                #symbol=json_data['symbol']
                cursor=json_data['cursor']
                more=cursor['more']
                since=cursor['since']
                maxid=cursor['max']
                iter=iter+1
                for message in json_data['messages']:
                    # replace ',' with '#' as output is csv file
                    # replace unprintable chars with unicode chars
                    adj_body=message['body'].replace(",","#").encode(sys.stdout.encoding, errors='replace')
                    sentiment="None"
                    if message['entities']['sentiment']:
                        sentiment=message['entities']['sentiment']['basic']
                    if rows % 30 == 0:
                        print('    {0},{1},{2},{3},{4}'.format(message['id'], stock, message['created_at'], adj_body, sentiment))
                    # build the csv row
                    row=str(message['id'])+","+stock+","+message['created_at']+","+str(adj_body)+","+sentiment+"\n"
                    writer.write(row)
                    rows=rows+1
finally:
    writer.close()
            
print("Written {0} rows to file: {1}".format(rows, file)) 
