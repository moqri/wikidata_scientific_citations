while read name; do    
	echo -e "\n$name" >> out.txt
	curl --header "Authorization: Token YOURTOKEN" tools.wmflabs.org/fatameh/token/pmc/add/PMC$name >> out.txt 
done < pmc.txt

