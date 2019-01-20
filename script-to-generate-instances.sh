#!bin/bash

array=( 2000 10000 30000 100000 300000 1000000 )

for students in "${array[@]}"
do
	courses=$(($students/5))
	lq=3
	hq=12
	for i in {1..10};
	do
		echo python3 generate_instance_seat.py $students $courses $lq $hq $students-$courses-$lq-$hq/inst$i
		python3 generate_instance_seat.py $students $courses $lq $hq $students-$courses-$lq-$hq/inst$i 
	done
done
