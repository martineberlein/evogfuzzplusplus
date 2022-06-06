RUN=1
MAX=11
SUBJECTS=(Rhino)

rm -rf "../experiment-results"
mkdir "../experiment-results"

for subject in "${SUBJECTS[@]}"
do
	echo "$subject"
	mkdir "../experiment-results/$subject"
	while [ $RUN -lt $MAX ]
	do
		echo "output: $RUN"
		mkdir "../experiment-results/$subject/Iteration-$RUN"
		timeout 600 python3 evogfuzz.py --output ../experiment-results/$subject/Iteration-$RUN  --target ../subjects/$subject/subject_driver.py -n
		true $(( RUN++ ))
	done
	RUN=1
done
