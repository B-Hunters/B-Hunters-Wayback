#!/bin/sh
domain=$1
targetfile=$2

waymore -i $domain -oU $targetfile -mode U
waybackurls $domain | anew $targetfile 
gau $domain | anew $targetfile 
