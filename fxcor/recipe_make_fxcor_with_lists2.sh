#!/bin/bash
for i in {060..150..1}
do
  echo $i
  name1="fxcor_ord"
  name2=".lis"
  for j in `ls $name1$i$name2`
  do
    echo "fxcor @"$j "20190903_0104_FOC1903_SCC2_ods_ord"$i"_A_lin_IRAF.fits" >> fxcor_with_lists.cl
  done
done