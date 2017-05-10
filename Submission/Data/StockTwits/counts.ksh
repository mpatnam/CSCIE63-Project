# get the daily counts

#awk -F, '{print $3}' AAPL.20170430.191643.csv  | sort | uniq -c | grep -v ' Date' | sed 's/ 2017/,2017/' > AAPL.tweets.counts.csv
awk -F, '{print $3}' FB.20170502.024702.csv| sort | uniq -c | grep -v ' Date' | sed 's/ 2017/,2017/' > FB.tweets.counts.csv
awk -F, '{print $3}' TSLA.20170501.033001.csv| sort | uniq -c | grep -v ' Date' | sed 's/ 2017/,2017/' > TSLA.tweets.counts.csv

# filter holidays from csv file
# date format: YYYY-mm-dd

set -x
for FILE in AAPL.tweets.counts.csv FB.tweets.counts.csv TSLA.tweets.counts.csv
do
	grep -v -e '2017-03-0[45]' -e '2017-03-1[12]' -e '2017-03-1[89]' -e '2017-03-2[56]' -e '2017-04-0[12]' -e  '2017-04-0[89]' -e '2017-04-1[456]' -e '2017-04-2[23]' -e '2017-04-29' -e '2017-04-30' $FILE  > $FILE.tmp
	mv $FILE.tmp $FILE
done
