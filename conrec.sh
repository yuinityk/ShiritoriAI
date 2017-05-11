echo "input difficulty:e,n,h"
read dif

if [ "${dif}" = "e" ]; then
  dff="easy"
elif [ "${dif}" = "n" ]; then
  dff="normal"
elif [ "${dif}" = "h" ]; then
  dff="hard"
else
  echo 'invalid character'
  exit 1
fi
echo $dff

start=`ls ./recorded/$dff/ -1 | wc -l`
start=`expr $start + 1`
echo $start
echo "input last number"
read  end
for i in `seq $(( start )) $(( end ))`
do
  arr=( `head -n $i dic_$dff.csv | tail -n 1 | tr -s ',' ' '`)
  echo $i ${arr[1]}
  #arecord -f dat -D hw:2,0 -c 1 ./recorded/$dff/${arr[1]}.wav
done
