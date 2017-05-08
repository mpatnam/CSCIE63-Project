import pandas as pd
import Preprocess as pp

# Set dictionary to 'Harvard' or 'Financial'
DICTIONARY = 'Financial'


# calculates a sentiment score between -1 and +1 based on counting words in positive and negative financial dictionary
def calc_score(message):
    words = message.upper().split()
    pos_count = sum([(word in fin_pos) for word in words])
    neg_count = sum([(word in fin_neg) for word in words])
    if pos_count + neg_count != 0:
        return 1.0*(pos_count - neg_count) / (pos_count + neg_count)
    else:
        return 0

# read in sentiment dictionary from files
tickers = ['AAPL', 'FB', 'TSLA']
data_paths = ['H:/Course Docs/Big Data/Final Project/Data/StockTwits/AAPL.20170430.191643.csv',
              'H:/Course Docs/Big Data/Final Project/Data/StockTwits/FB.20170502.024702.csv',
              'H:/Course Docs/Big Data/Final Project/Data/StockTwits/TSLA.20170501.033001.csv']
export_path1 = 'H:/Course Docs/Big Data/Final Project/Results/Sentiment Analysis-1/dict_output_simple.'
export_path2 = 'H:/Course Docs/Big Data/Final Project/Results/Sentiment Analysis-1/dict_output_weighted.'

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

# read in data from files
for ticker, data_path in zip(tickers, data_paths):
    df_data = pd.read_csv(data_path)

    # clean up data
    # remove stop words to reduce dimensionality
    df_data["stop_text"] = df_data["Body"].apply(pp.remove_stops)
    # remove other non essential words, think of it as my personal stop word list
    df_data["feat_text"] = df_data["stop_text"].apply(pp.remove_features)
    # tag the words remaining and keep only Nouns, Verbs and Adjectives
    df_data["tagged_text"] = df_data["feat_text"].apply(pp.tag_and_remove)
    # lemmatization of remaining words to reduce dimensionality & boost measures
    df_data["text"] = df_data["tagged_text"].apply(pp.lemmatize)

    # calculate sentiment score using dictionary
    df_data['sentiment_score'] = df_data['text'].apply(calc_score)
    x = df_data[['Date', 'sentiment_score']].groupby(['Date'])
    simple_agg = x.sum() / x.count()
    simple_agg.to_csv(export_path1+ticker+'.'+DICTIONARY+'.csv', index=True)

    weighted_agg = x.sum() / (len(df_data)/len(x))
    weighted_agg.to_csv(export_path2+ticker+'.'+DICTIONARY+'.csv', index=True)
