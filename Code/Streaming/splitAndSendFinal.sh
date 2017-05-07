split -l 100 StockTwits.20170328.csv chunk

for f in `ls chunk*`; do

   if [ "$2" == "local" ]; then
      mv $f $1
   else
              hadoop fs -put $f sentiment/staging
              hadoop fs -mv sentiment/staging/$f sentiment/input
              rm -f $f
       fi
       sleep 10
done
