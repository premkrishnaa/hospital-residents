#!bin/bash

array=( 1000 2000 4000 8000 16000 32000 )

for students in "${array[@]}"
do
	courses=$(($students/6))
	#courses=250
	lq=3
	hq=12
	for i in {1..10};
	do
		#echo python3 generate_instance_seat.py $students $courses $lq $hq $students-$courses-$lq-$hq/inst$i
		#python3 generate_instance_seat.py $students $courses $lq $hq $students-$courses-$lq-$hq/inst$i 
		echo python3 test.py ../matchup/experiments/$students-$courses-$lq-$hq/inst$i
		python3 test.py ../matchup/experiments/$students-$courses-$lq-$hq/inst$i 	
	done
done
