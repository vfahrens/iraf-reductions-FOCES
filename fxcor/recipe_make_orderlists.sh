for i in {060..150..1}; do
  echo $i
  name=*_ord$i_*_A_*.fits
  echo $name
  for j in `ls *_ord$i_*_A_*.fits`; do
    echo $j >> fxcor_ord$i.lis;
done