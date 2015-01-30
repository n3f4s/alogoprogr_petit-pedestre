#!/bin/bash


cmd="poooserver.py -P 9876 -B 2048 --speed 1 --roomsize 2"
if (( $# > 0 )); then
	if [[ $1 == "server" ]]; then
		echo -e 'Starting poooserver'
	elif [[ $1 == "--help" ]]; then
		echo -e "usage : "
		echo -e "\tlaunch [server]             Lance le serveur"
		echo -e "\tlaunch bot [pte] [joueur]   Lance le client avec pte comme point d'entré et joueur le nom du joueur, il faut mettre soit les deux paramêtres (pour bot), soit aucun. Si aucun paramêtre n'est renseigné (mis à part bot), il sera demandé de séléctionner le point d'entré ainsi que le nom du joueur"
		echo
		echo -e "exemples : "
		echo -e "\tlaunch                      Lance le serveur"
		echo -e "\tlaunch server               Lance le serveur"
		echo -e "\tlaunch bot                  Lance un client, le nom du joueur ainsi que le point d'entré seront demandé"
		echo -e "\tlaunch bot test jean        Lance un client avec comme point d'entré test.py et comme nom de joueur jean"
		echo -e "\tlaunch bot test.py jean     Lance un client avec comme point d'entré test.py et comme nom de joueur jean"
		exit 0
	elif [[ $1 == "bot" ]]; then
		if (( $# >= 3 )); then
			cmd="pooobot.py -s :9876 -b $(basename $2 .py) $3"
		else
			list_src=""
			for src in ./*.py
			do
				list_src="$list_src $src"
			done
			select entry_point in $list_src
			do
				tmp=$(basename $entry_point .py)
				read -p "Entrez le nom du joueur : " player
				cmd="pooobot.py -s :9876 -b $tmp $player"
				break
			done
		fi
		echo -e 'Starting pooobot'
	else
		echo -e "usage : "
		echo -e "\tlaunch [server]             Lance le serveur"
		echo -e "\tlaunch bot [pte] [joueur]   Lance le client avec pte comme point d'entré et joueur le nom du joueur, il faut mettre soit les deux paramêtres (pour bot), soit aucun. Si aucun paramêtre n'est renseigné (mis à part bot), il sera demandé de séléctionner le point d'entré ainsi que le nom du joueur"
		echo
		echo -e "exemples : "
		echo -e "\tlaunch                      Lance le serveur"
		echo -e "\tlaunch server               Lance le serveur"
		echo -e "\tlaunch bot                  Lance un client, le nom du joueur ainsi que le point d'entré seront demandé"
		echo -e "\tlaunch bot test jean        Lance un client avec comme point d'entré test.py et comme nom de joueur jean"
		echo -e "\tlaunch bot test.py jean     Lance un client avec comme point d'entré test.py et comme nom de joueur jean"
		exit -1
	fi
fi
python3 $cmd
pypid=$!
trap '{ kill -SIGINT $pypid; killall python3; exit -1; }' SIGINT
echo
echo -e "Finished"
