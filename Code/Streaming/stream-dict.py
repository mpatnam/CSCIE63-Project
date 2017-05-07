from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import Preprocess as pp
import pandas as pd

sc = SparkContext(appName="SparkStreamingScoreDictionary") 
ssc = StreamingContext(sc, 9)
filestream = ssc.textFileStream("hdfs:///user/cloudera/sentiment/input")

DICTIONARY = 'Harvard'

if DICTIONARY == 'Financial':
    # use financial dictionary
    dict_path = '/home/cloudera/LoughranMcDonald_MasterDictionary_2014.xlsx'
    df_dict = pd.read_excel(dict_path)
    fin_pos = df_dict['Word'][df_dict['Positive'] != 0].tolist()
    fin_neg = df_dict['Word'][df_dict['Negative'] != 0].tolist()

elif DICTIONARY == 'Harvard':
    # use harvard dictionary
    dict_path = '/home/cloudera/inquirerbasic.xls'
    df_dict = pd.read_excel(dict_path)
    fin_pos = df_dict[df_dict['Positiv'] == 'Positiv'].index.tolist()
    fin_neg = df_dict[df_dict['Negativ'] == 'Negativ'].index.tolist()
else:
    raise Exception('Error: Improper dictionary chosen.')


def calc_score(message):
  words = message.upper().split()
  pos_count = sum([(word in fin_pos) for word in words])
  neg_count = sum([(word in fin_neg) for word in words])
  if pos_count + neg_count != 0:
    return 1.0*(pos_count - neg_count) / (pos_count + neg_count)
  else:
    return 0


from datetime import datetime
def parseTweet(line):
  s = line.split(",")
  try:
      if len(s[3])!=20:
        raise Exception('Wrong date format')
      if s[1]!='AAPL' and s[1]!='FB' and s[1]!='TSLA':
        raise Exception('Wrong ticker')
      # clean up message
      clean_text = pp.lemmatize(pp.tag_and_remove(pp.remove_features(pp.remove_stops(s[4]))))
      score = calc_score(clean_text)
      tweet_time = datetime.strptime(s[3][:10]+' '+s[3][11:19], "%Y-%m-%d %H:%M:%S")
      print(tweet_time)
      print(score)
      return [{"time": tweet_time, "tweetId": long(s[0]), "ticker": s[1],"Body": s[4], "sentiment_tag": s[5], "score": score}]
  except Exception as err:
      print("Wrong line format (%s): " % line)
      return []

orders = filestream.flatMap(parseTweet)
from operator import add
sentimentPerTicker = orders.map(lambda o: (o['ticker'], o['score'])).reduceByKey(add)
sentimentPerTicker.repartition(1).saveAsTextFiles("hdfs:///user/cloudera/output/output", "txt")

ssc.start()
ssc.awaitTermination()
# ssc.stop(False)
