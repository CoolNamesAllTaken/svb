#!/bin/bash
 
# Script adapted from here: https://community.godaddy.com/s/question/0D53t00006VmU0qCAF/dynamic-dns-updates
# First go to GoDaddy developer site to create a developer account and get your key and secret
#
# https://developer.godaddy.com/getstarted
# Be aware that there are 2 types of key and secret - one for the test server and one for the production server
# Get a key and secret for the production server
# 
# Update the first 4 variables with your information

source $(dirname "$0")/../.env.birdbox
name="@"     # name of A record to update
 
headers="Authorization: sso-key $GODADDY_API_KEY:$GODADDY_API_SECRET"
 
echo $headers

for domain in "${DOMAINS[@]}"; do
	echo "Updating server IP for $domain"
	request_url="https://api.godaddy.com/v1/domains/$domain/records/A/$name"
	echo -e "\tREQUEST_URL: $request_url"
	result=$(curl -s -X GET -H "$headers" $request_url)
	
	dnsIp=$(echo $result | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b")
	echo -e "\tdnsIp:" $dnsIp
	
	# Get public ip address there are several websites that can do this.
	ret=$(curl -s GET "http://ipinfo.io/json")
	currentIp=$(echo $ret | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b")
	echo -e "\tcurrentIp:" $currentIp
	
	if [ $dnsIp != $currentIp ];
	then
		echo -e "\tIps are not equal"
		request='[{"data":"'$currentIp'","ttl":3600}]'
		echo -e "\tREQUEST:"
		echo -e "\t$request"
		nresult=$(curl -i -s -X PUT \
			-H "$headers" \
			-H "Content-Type: application/json" \
			-d $request $request_url)
		echo -e "\tRESULT:"
		echo -e "\t$nresult"
	fi
done