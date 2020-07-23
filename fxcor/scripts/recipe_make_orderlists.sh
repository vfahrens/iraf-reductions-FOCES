#!/bin/bash

fname="*_ods_fred.fits"
for j in `echo $fname`
do
    for i in {1..84..1}
    do
	let k=i+64
	echo $j[$i] >> fxcor_ord$k.lis
    done
done
