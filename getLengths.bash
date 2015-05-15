if [[ $1 -eq '' ]] ; then
    echo 'Specifiy an ID.'
    exit 1
fi

temp1=$(mktemp)
temp2=$(mktemp)

wget -O $temp1 "https://genomevolution.org/coge/FeatList.pl?dsgid=${1}&ftid=4;gstid=1"

<$temp1 sed 's/,//g' | sed 's/<div.*div>//g' | sed 's/<input[^>]*>//g' > $temp2
<$temp2 grep -e '</\?TABLE\|</\?TD\|</\?TR' | sed 's/^[\ \t]*//g' | tr -d '\n' | sed 's/<\/TR[^>]*>/\n/g'  | sed 's/<\/\?\(TABLE\|TR\)[^>]*>//g' | sed 's/^<T[DH][^>]*>\|<\/\?T[DH][^>]*>$//g' | sed 's/<\/T[DH][^>]*><T[DH][^>]*>/,/g' > $temp1
<$temp1 cut -d, -f4,8 | sed -r 's/^([^,]*),([^,]*)$/{"name":"\1","length":"\2"},/g' > $temp2

echo '{'
echo "\"id\":\"$1\","
echo '"lengths":['
head -n-1 $temp2
tail -n1 $temp2 | sed 's/},/}/g'
echo ']'
echo '}'

rm $temp1 $temp2
