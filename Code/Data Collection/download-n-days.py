# download tweets from stocktwits
import urllib.request, json
import os
import sys
from datetime import datetime
import time

# fetch date and seq for csv file purpose
today_str=datetime.today().strftime('%Y%m%d')
seq=datetime.today().strftime('%H%M%S')

#data_dir=os.getcwd()
data_dir="C:\\Users\\mpatnam\\Documents\\GitHub\\CSCIE63\\CSCIE63-Big-Data-Analytics\\Project\\CSCIE63-Project\\Data"

#stocks=["AAPL", "TSLA", "FB", "TWTR"]
stocks=["TWTR"]

# Download control parameters
#tot_batches=3
tot_days=63               # desired days       
max_requests_per_hour=200 #StockTwits limit
sleep_time=60*60          #sec
progress_output_rows=30   #rows

# iterate for all stocks
for stock in stocks:
    try:
        rows_written=0
        cur_days=0
        cur_date=datetime.now().date()
        file=data_dir+"\\"+stock+"."+today_str+"."+seq+".csv"
        writer = open(file, 'w')
        writer.write('ID,Symbol,Date,CreateTime,Body,Sentiment\n')
        url="https://api.stocktwits.com/api/2/streams/symbol/"+stock+".json"
        print('[{0}]: ---------------------------{1}------------------------------'.format(datetime.now(), stock))
        print(url)
        
        with urllib.request.urlopen(url) as urlobj:
            json_data = json.loads(urlobj.read().decode())
            symbol=json_data['symbol']
            cursor=json_data['cursor']
            more=cursor['more']
            since=cursor['since']
            maxid=cursor['max']
            cur_batch=0
            
            while more and cur_days < tot_days:
                print('batch:{0} {1},{2},{3},{4},{5}'.format(cur_batch, cur_date, stock, more, since, maxid))
                for message in json_data['messages']:
                    #
                    # fetch interested columns - id, stock create_time, body, sentiment
                    #
                    # tweet ID 
                    tweet_id=message['id']
                    #
                    # Adjust body text
                    #     replace ',' with '#' as output is csv file
                    #     replace unprintable chars with unicode chars
                    body_adj=message['body'].replace(",","#").encode(sys.stdout.encoding, errors='replace')
                    #
                    # sentiment (optional)
                    #
                    sentiment="None"
                    if message['entities']['sentiment']:
                        sentiment=message['entities']['sentiment']['basic']
                    #
                    # create time
                    #
                    tweet_time=message['created_at']
                    tweet_time_obj = datetime.strptime(tweet_time, '%Y-%m-%dT%H:%M:%SZ')
                    tweet_date=tweet_time_obj.date()
                                
                    # check for date boundaries
                    if cur_date != tweet_date:
                        cur_date = tweet_date
                        cur_days = cur_days+1
                        #print('    {0}'.format(str(cur_date)))
                    
                    # show the progress with occassional output to console
                    if rows_written % progress_output_rows == 0:
                        print('    {0},{1},{2},{3},{4},{5},{6}'.format(cur_batch, cur_date, tweet_id, stock, tweet_time, body_adj, sentiment))
                   
                    # Write the row to the csv file
                    row=str(tweet_id)+","+stock+","+str(cur_date)+","+tweet_time+","+str(body_adj)+","+sentiment+"\n"
                    writer.write(row)
                    rows_written=rows_written+1
                
                # move to the next iteration
                cur_batch=cur_batch+1
                if cur_batch % max_requests_per_hour == 0:
                    # sleep for one hour
                    print("\n[{0}]: StockTwits max-batch-per-hour reached, sleeping for {1} sec\n".format(datetime.now(), sleep_time))
                    time.sleep(sleep_time) #sec

                    
                time.sleep(1) #sec
                url="https://api.stocktwits.com/api/2/streams/symbol/"+stock+".json?max="+str(maxid)
                urlobj2=urllib.request.urlopen(url)
                json_data = json.loads(urlobj2.read().decode())
                cursor=json_data['cursor']
                more=cursor['more']
                since=cursor['since']
                maxid=cursor['max']
    finally:
        writer.close()
        print("{0}: Written {1} days ({2} rows) worth of data to file: {3}".format(stock, cur_days, rows_written, file)) 
