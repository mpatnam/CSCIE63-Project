import pandas as pd
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import Preprocess as pp


# calculate the signal from text in cleaned message
def calc_(message):
    words = message.upper().split()
    pos_count = sum([(word in fin_pos) for word in words])
    neg_count = sum([(word in fin_neg) for word in words])
    if pos_count > neg_count:
        return 'Bullish'
    elif neg_count > pos_count:
        return 'Bearish'
    else:
        return 'None'

# read in twitter data and sentiment dictionary from files
data_path = 'H:/Course Docs/Big Data/Final Project/Data/StockTwits/StockTwits.20170425.131745.csv'
dict_path = 'H:/Course Docs/Big Data/Final Project/Docs/LoughranMcDonald_MasterDictionary_2014.xlsx'
export_path = 'H:/Course Docs/Big Data/Final Project/Results/Sentiment Analysis-1/test_dict_output.csv'
df_data = pd.read_csv(data_path)
df_dict = pd.read_excel(dict_path)

# create positive and negative dictionaries
fin_pos = df_dict['Word'][df_dict['Positive'] != 0].tolist()
fin_neg = df_dict['Word'][df_dict['Negative'] != 0].tolist()

# clean up data
# TODO: How should we treat re-tweets?
# dedupe important since alot of the tweets only differed by url's and RT mentions
#df_data.drop_duplicates(subset=['Body', 'Sentiment'], inplace=1)
# remove stop words to reduce dimensionality
df_data["stop_text"] = df_data["Body"].apply(pp.remove_stops)
# remove other non essential words, think of it as my personal stop word list
df_data["feat_text"] = df_data["stop_text"].apply(pp.remove_features)
# tag the words remaining and keep only Nouns, Verbs and Adjectives
df_data["tagged_text"] = df_data["feat_text"].apply(pp.tag_and_remove)
# lemmatization of remaining words to reduce dimensionality & boost measures
df_data["text"] = df_data["tagged_text"].apply(pp.lemmatize)
# select only the columns we care about
df_data = df_data[['ID', 'Symbol', 'text', 'Sentiment']]

# compute sentiment (bullish/bearish) for each twitter using dictionary
messages_list = df_data.text.tolist()
dict_scores = []
for message in messages_list:
    words = message.upper().split()
    pos_score = sum([(word in fin_pos) for word in words])
    neg_score = sum([(word in fin_neg) for word in words])
    if pos_score - neg_score < 0:
        dict_scores.append('Bearish')
    elif pos_score - neg_score > 0:
        dict_scores.append('Bullish')
    else:
        dict_scores.append('None')

# write to file
act_scores = df_data['Sentiment'].tolist()
output = pd.DataFrame({'Predicted': dict_scores, 'Actual': act_scores, 'Tweet': messages_list})
output[['Predicted', 'Actual', 'Tweet']].to_csv(export_path, index=False)

# plot confusion matrix
cnf_matrix = confusion_matrix(y_true=act_scores, y_pred=dict_scores, labels=['Bearish', 'Bullish', 'None'])
plt.imshow(cnf_matrix, cmap='binary', interpolation='None')
plt.show()

# create data summary table
table_totals = pd.crosstab(pd.Series(act_scores), pd.Series(dict_scores), rownames=['True'], colnames=['Predicted'], margins=True)
pd.options.display.float_format = '{:.2f}'.format
table_perc = pd.crosstab(pd.Series(act_scores), pd.Series(dict_scores), rownames=['True'], colnames=['Predicted']).apply(lambda r: r/r.sum(), axis=1)
print table_totals
print table_perc

