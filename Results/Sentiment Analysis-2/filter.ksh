# filter holidays from csv file
# date format: YYYY-mm-dd

set -x

grep -v -e '3/[45]/2017' -e '3/1[12]/2017' -e '3/1[89]/2017' -e '3/2[56]/2017' -e '4/[12]/2017' -e  '4/[89]/2017' -e '4/1[456]/2017' -e '4/2[23]/2017' -e '4/29/2017' -e '4/30/2017' $1  > $1.tmp

mv $1.tmp $1
