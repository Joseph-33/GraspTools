if ! [ -z "$1" ]
then
	val=$1
else
	val=rcsfgen_input
fi

echo "Using: "$val
rcsfpreview < $val > conf_preview_tmp 2>&1

python my_conf_collector.py conf_preview_tmp $val
rm conf_preview_tmp
