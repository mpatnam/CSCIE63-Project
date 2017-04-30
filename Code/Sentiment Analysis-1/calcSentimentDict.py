import pandas as pd
import re
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

# read in twitter data and sentiment dictionary from files
data_path = 'H:/Course Docs/Big Data/Final Project/StockTwits.20170425.131745.csv'
dict_path = 'H:/Course Docs/Big Data/Final Project/LoughranMcDonald_MasterDictionary_2014.xlsx'
export_path = 'H:/Course Docs/Big Data/Final Project/output.csv'
df_data = pd.read_csv(data_path)
df_dict = pd.read_excel(dict_path)

# create positive and negative dictionaries
fin_pos = df_dict['Word'][df_dict['Positive'] != 0].tolist()
fin_neg = df_dict['Word'][df_dict['Negative'] != 0].tolist()

# compute sentiment (bullish/bearish) for each twitter using dictionary
messages_list = df_data.Body.tolist()
dict_scores = []
for message in messages_list:
    letters_only = re.sub("[^a-zA-Z]",  " ",  message)
    letters_only = letters_only.upper()
    words = letters_only.split()
    pos_score = sum([(word in fin_pos) for word in words])
    neg_score = sum([(word in fin_neg) for word in words])
    if pos_score - neg_score < 0:
        dict_scores.append('Bearish')
    elif pos_score - neg_score > 0:
        dict_scores.append('Bullish')
    else:
        dict_scores.append('None')

# TODO: apply tf.idf to give proper weight to each word

# write to file
act_scores = df_data['Sentiment'].tolist()
output = pd.DataFrame({'Predicted': dict_scores, 'Actual': act_scores, 'Message': messages_list})
output.to_csv(export_path, index=False)

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

