                                             Spark near real-time Sentiment Analysis
                                        Mohan K. Patnam, C.N. Chen, Bruno Janota (CSCI E-63)
________________________________________________________________________________________________________________________________________

Motivation: This project studies whether social media feeds focused towards stock market and concerning companies, are a suitable data source for forecasting the volatility in the underlying stock prices. In particular, we focus on StockTwits.com which is a popular social media platform where real investors, traders and general public alike express their opinion on companies and their performance in the form of tweets. We begin this project by providing a generic approach to download historical tweets for the chosen stocks for a chosen period. We then introduce couple of models to calculate social sentiment score using Bag-of-Words (dictionary) approach and Naive-Bayes classifier. We apply basic text processing techniques to preprocess tweets and help build these models. We further perform regression analysis to see if social sentiment can serve as a leading indicator to predict underlying changes in stock prices. We demonstrate an ability to sense the market pulse or sentiment using a near real-time stream of tweets. Our quest here is to help answer a fundamental question on whether social sentiment matters for stock market performance.

Project Phases
This project is divided into 4 phases. The first phase of the project focussed on data download and wrangling into a suitable format for further processing. We collected historical tweets for chosen stocks for a period of two months from www.StockTwits.com using their restful API. As per our research on investopedia.com, there are few stocks that are very popular on stocktwits platform (Most followed stocks in stocktwits.com). We chose 3 such stocks for our sentiment analysis in this project - AAPL, FB, and TSLA. We also collected historical stock prices (close price, traded volume) for the same stocks for the same period from Yahoo! Finance (http://finance.yahoo.com).. The second phase of the project aims to build couple of models to predict the social sentiment in the form of a weighted score. We use this score to categorize the social sentiment of a tweet into one of the 3 categories - Bullish (positive), Neutral (none) and Bearish (negative). The first model is based on bag-of-words approach using couple of financial dictionaries to guide the lookup of keywords in the tweet and further derive the score. The second model is based on a probabilistic approach using Naive-Bayes Classifier. We train the model first using training-set data and use the test-set data to predict the score. We provide confusion matrix for both approaches to highlight the accuracy of respective models. The third phase of the project aims to build a regression model by using an aggregate daily sentiment score as a predictor of stock close price. We use GradientDescentOptimizer to train the regression model first and then use the test-data to predict stock close prices. We document model results and accuracy in the form of Tensor board summaries (loss) and computing graph.

Sources
Investopedia - Most followed stocks in stocktwits.com
StockTwits API - https://stocktwits.com/developers/docs
Yahoo! Finance for historical stock prices - AAPL Historical Prices
Bloomberg for Intraday prices - ??
Dictionary sources - ??
Naive Bayes Classifier - ??

API and Tools
Python 3.5 on Windows-10 64-bit machine and Linux (Cloudera VM) platform
IDE - PyCharm and IPython Notebook
Packages - numpy, tensorflow, matplotlib, urllib, json, ……
StockTwits RESTful API
Tensorboard API
