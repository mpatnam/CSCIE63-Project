import pandas as pd
import Preprocess as pp

DICTIONARY = 'Harvard'


# calculates a sentiment score between -1 and +1 based on counting words in positive and negative financial dictionary
def calc_score(message):
    words = message.upper().split()
    pos_count = sum([(word in fin_pos) for word in words])
    neg_count = sum([(word in fin_neg) for word in words])
    if pos_count + neg_count != 0:
        return 1.0*(pos_count - neg_count) / (pos_count + neg_count)
    else:
        return 0

# read in twitter data and sentiment dictionary from files
data_path = 'H:/Course Docs/Big Data/Final Project/Data/StockTwits/AAPL.20170430.191643.csv'
export_path = 'H:/Course Docs/Big Data/Final Project/Results/Sentiment Analysis-1/test_dict_one_output.csv'
df_data = pd.read_csv(data_path)
original_count = len(df_data)

if DICTIONARY == 'Financial':
    # use financial dictionary
    dict_path = 'H:/Course Docs/Big Data/Final Project/Docs/LoughranMcDonald_MasterDictionary_2014.xlsx'
    df_dict = pd.read_excel(dict_path)
    fin_pos = df_dict['Word'][df_dict['Positive'] != 0].tolist()
    fin_neg = df_dict['Word'][df_dict['Negative'] != 0].tolist()

elif DICTIONARY == 'Harvard':
    # use harvard dictionary
    dict_path = 'H:/Course Docs/Big Data/Final Project/Docs/inquirerbasic.xls'
    df_dict = pd.read_excel(dict_path)
    fin_pos = df_dict[df_dict['Positiv'] == 'Positiv'].index.tolist()
    fin_neg = df_dict[df_dict['Negativ'] == 'Negativ'].index.tolist()
else:
    print 'Error: Improper dictionary chosen.'

# use only AAPL March 28th
df_data = df_data[(df_data['Date'] == '2017-03-28')]

# clean up data
# remove stop words to reduce dimensionality
df_data["stop_text"] = df_data["Body"].apply(pp.remove_stops)
# remove other non essential words, think of it as my personal stop word list
df_data["feat_text"] = df_data["stop_text"].apply(pp.remove_features)
# tag the words remaining and keep only Nouns, Verbs and Adjectives
df_data["tagged_text"] = df_data["feat_text"].apply(pp.tag_and_remove)
# lemmatization of remaining words to reduce dimensionality & boost measures
df_data["text"] = df_data["tagged_text"].apply(pp.lemmatize)
# select only the columns we care about

df_data['Score'] = df_data['text'].apply(calc_score)
x = df_data[['Date', 'Score']].groupby(['Date'])

df_data[['ID', 'Symbol', 'Date', 'CreateTime', 'Body', 'Sentiment', 'text', 'Score']].to_csv(export_path, index=False)

simple_agg = x.sum() / x.count()
weighted_agg = x.sum() / (len(df_data)/len(x))
print 'Simple Agg = Sum(Scores_d) / Count(Scores_d)'
print simple_agg.values[0][0]
print 'Weighted Agg = Sum(Scores_d) * / (Count(TweetsAllDays)/Count(Days))'
print weighted_agg.values[0][0]
