rwfn_inp="reopped_both.w"
fstr="DF3"

declare -A orb_names=( [1]="s" [2]="p" [3]="d" [4]="f" [5]="g" )
declare -A orb_nums=( ["s"]=1 ["p"]=2 ["d"]=3 ["f"]=4 ["g"]=5 )
nuc_charge=$(head -n2 isodata | tail -n1)
echo "Using fstr: "$fstr
echo "Using rwfn: "$rwfn_inp
echo "Current nuclear charge:" ${nuc_charge:0:9}
read -p "Continue..."
while true; do

    init_nuc=$(head -n2 isodata | tail -n1)

    sed -i "12s/.*/${rwfn_inp}/" batch_input_creator/rwfnestimate_input2

    read -p "Which orbitals would you like to optimise? (Hint: use 3* to optimise 3s,3p,...) (Type 'n' to exit) :" optimisation

    if [[ "$optimisation" == "n" ]]
    then
	echo "Exiting program now..."
	exit 0
    fi

    old_fstr=$fstr
    builder=""
    others_str=${optimisation##*>}
    if [[ "$optimisation" == *">"* ]]; then

	core_str=${optimisation:0:1}
	check_expand_str=${optimisation:1:1}
	echo $check_expand_str

	if [[ $check_expand_str == ">" ]]; then
	    for i in $(seq 1 $core_str); do builder=$builder" "$i*; done

	else
	    for i in $(seq 1 $core_str); do
		for j in $(seq 1 $i); do
		    if [[ "$j" -gt ${orb_nums[$check_expand_str]} ]]; then
			continue
		    fi
		    builder=$builder" "$i${orb_names[$j]}*
		done

	    done


	fi


    fi
    fstr=${fstr}_${optimisation// /}

    echo $builder$others_str

    echo "Current nuclear charge:" $(head -n2 isodata | tail -n1)
    read -p "Nuc decrease mode?: " nuc_decrease_mode

    if [[ "$nuc_decrease_mode" == "y" ]]; then
	read -p "What should the nuclear charge decrease by?: " negator
	myvar=$(sed '2!d' isodata)
	final=$(echo "$myvar - $negator" | bc -l)
	sed -i "2s/.*/   ${final}/" isodata
	final_str=${final:1:3}
    fi

    nam_myvar=$(sed '2!d' isodata)
    nog=103
    nam_final=$(echo "$nam_myvar - $nog" | bc -l)
    result=$(echo "scale=7; $nam_final == 0" | bc)
    if [ "$(echo "$nam_final != 0" | bc -l)" -eq 1 ]; then
	final=$(echo "$nam_myvar - 0.0" | bc -l)
	nam_final_str=${final:2:3}
	fstr=${fstr}N${nam_final_str/./}
	echo $fstr
    fi

    sed -i "24s/.*/${builder}${others_str}/" batch_input_creator/rmcdhf_input2
    sed -i "14s/.*/"n"/" batch_input_creator/rwfnestimate_input2
    rwfnestimate < batch_input_creator/rwfnestimate_input2 |& tee logs/reop/rwfnestimate_${fstr}
    read -p "Change optimised estimates? (y): " est_ans

    if [[ "$est_ans" == "y" ]]; then
	KeepValue="y"
	expanded_optimisation=$optimisation

	echo "HI"
	echo $expanded_optimisation
	while [[ ${expanded_optimisation} =~ ..\* ]]; do
	    matched_text="${BASH_REMATCH[0]}"
	    matched_text2=${matched_text::-1}
	    subs="${matched_text2}- ${matched_text2}"
	    expanded_optimisation=$(echo "$expanded_optimisation" | sed "s/..\*/${subs}/")
	    expanded_optimisation="${expanded_optimisation#*$matched_text}"
	done


	while [[ ${KeepValue} == "y" ]]; do

	    head -n18 batch_input_creator/rwfnestimate_input2 > tmp_rwfnest
	    mv tmp_rwfnest batch_input_creator/rwfnestimate_input2
	    echo "$expanded_optimisation"
	    for i in ${expanded_optimisation[@]};
	    do
		read -p "Describe the Z increase for $i: " Zinc
		echo $Zinc
		echo $Zinc >> batch_input_creator/rwfnestimate_input2 

	    done

	    echo n >> batch_input_creator/rwfnestimate_input2 

	    sed -i "14s/.*/y/" batch_input_creator/rwfnestimate_input2
	    sed -i "15s/.*/${builder}${others_str}/" batch_input_creator/rwfnestimate_input2
	    #sed -i "15s/.*/7p-/" batch_input_creator/rwfnestimate_input2
	    rwfnestimate < batch_input_creator/rwfnestimate_input2 |& tee logs/reop/rwfnestimate_${fstr}
	    read -p "Change values again? (y): " KeepValue

	done
    fi


    #mpirun -np ${CORES} rmcdhf_mpi < batch_input_creator/rmcdhf_input2 |& tee logs/rmcdhf_${layer}_${fstr}
    rmcdhf < batch_input_creator/rmcdhf_input2 |& tee logs/reop/rmcdhf_${fstr}

    echo "Done"
    tac logs/reop/rmcdhf_${fstr} | awk '!flag; /Self/{flag = 1};' | tac | head -n 50
    grep "Iteration number " logs/reop/rmcdhf_${fstr} | tail -1

    echo $fstr
    read -p "Did the calculation succeed? : " success
    if [[ "$success" != "y" ]]
    then
	rm logs/reop/rmcdhf_${fstr}
	rm logs/reop/rwfnestimate_${fstr}
	sed -i "2s/.*/${init_nuc}/" isodata
	fstr=$old_fstr
    else
	echo $fstr
	cp isodata previous_inputs/reop/isodata_${fstr}
	cp batch_input_creator/rmcdhf_input2 previous_inputs/reop/rmcdhf_${fstr}
	cp batch_input_creator/rwfnestimate_input2 previous_inputs/reop/rwfnest_${fstr}
	cp rwfn.out rwfn_out_${fstr}
	rwfn_inp=rwfn_out_${fstr}
    fi
done
