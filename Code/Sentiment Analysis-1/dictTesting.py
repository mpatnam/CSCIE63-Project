import pandas as pd
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import Preprocess as pp
import itertools
import numpy as np

# dictionary setting can either be 'Harvard' or 'Financial'
DICTIONARY = 'Financial'


# prints and plots the confusion matrix; normalization can be applied by setting `normalize=True`.
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    # set ticks
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    # handle normalization
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    print(cm)
    # add labels
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# calculate if message is bearish or bullish or neutral
def calc_sentiment(message):
    # make all letters upper case and split into words
    words = message.upper().split()
    # tabulate positive and negative word counts
    pos_count = sum([(word in fin_pos) for word in words])
    neg_count = sum([(word in fin_neg) for word in words])
    # return sentiment
    if pos_count > neg_count:
        return 'Bullish'
    elif neg_count > pos_count:
        return 'Bearish'
    else:
        return 'None'

# read in twitter data and sentiment dictionary from files
data_paths = ['H:/Course Docs/Big Data/Final Project/Data/StockTwits/AAPL.20170430.191643.csv',
              'H:/Course Docs/Big Data/Final Project/Data/StockTwits/FB.20170502.024702.csv',
              'H:/Course Docs/Big Data/Final Project/Data/StockTwits/TSLA.20170501.033001.csv']
# define export file path
export_path = 'H:/Course Docs/Big Data/Final Project/Results/Sentiment Analysis-1/test_dict_output.csv'

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
    raise Exception('Error: Improper dictionary chosen.')

# combine all raw data into one dataframe
df_data = pd.DataFrame()
for data_path in data_paths:
    if len(df_data) == 0:
        df_data = pd.read_csv(data_path)
    else:
        df_newfile = pd.read_csv(data_path)
        df_data = pd.concat([df_data, df_newfile])

# clean up messages using nltk
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

# calculate sentiment prediction using dictionary
df_data['Prediction'] = df_data['text'].apply(calc_sentiment)

# summarize tweet counts
print 'Total '+str(len(df_data))+' tweets'
print 'Actual None: '+str(len(df_data[df_data['Sentiment'] == 'None']))+' tweets'
print 'Predict None: '+str(len(df_data[df_data['Prediction'] == 'None']))+' tweets'
print 'Either None: '+str(len(df_data[((df_data['Sentiment'] == 'None')|(df_data['Prediction'] == 'None'))]))+' tweets'

# write to file
act_scores = df_data[((df_data['Sentiment'] != 'None')&(df_data['Prediction'] != 'None'))]['Sentiment'].tolist()
dict_scores = df_data[((df_data['Sentiment'] != 'None')&(df_data['Prediction'] != 'None'))]['Prediction'].tolist()
messages_list = df_data[((df_data['Sentiment'] != 'None')&(df_data['Prediction'] != 'None'))]['text'].tolist()
output = pd.DataFrame({'Predicted': dict_scores, 'Actual': act_scores, 'Tweet': messages_list})
output[['Predicted', 'Actual', 'Tweet']].to_csv(export_path, index=False)

# create data summary table
table_totals = pd.crosstab(pd.Series(act_scores), pd.Series(dict_scores), rownames=['True'], colnames=['Predicted'],
                           margins=True)
pd.options.display.float_format = '{:.2f}'.format
table_perc = pd.crosstab(pd.Series(act_scores), pd.Series(dict_scores),
                         rownames=['True'], colnames=['Predicted']).apply(lambda r: r/r.sum(), axis=1)
print table_totals
print table_perc

# compute and plot confusion matrix
cnf_matrix = confusion_matrix(y_true=act_scores, y_pred=dict_scores)
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=['Bearish', 'Bullish'], title='Confusion Matrix', normalize=True)
plt.show()
