for i in {060..150..1}
do
  echo $i
  name1="*_ods_ord"
  name2="_A_*.fits"
  echo $name1$i$name2
  for j in `ls $name1$i$name2`
  do
    echo $j >> fxcor_ord$i.lis
  done
done