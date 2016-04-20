# Open Maps - Federal Geospatial Platform Harvester
The Open Government Secretariat's (OGS) Open Maps (OM) harvester pulling from the Federal Geospatial Platform (FGP) developed and maintained at Statistics Canada (StatCan).

![Harvester - FGP - Diagram](https://raw.githubusercontent.com/open-data/harvester-FGP/master/docs/Harvest%20Diagram.png)

## harvest_hnap.py
Extract *HNAP* XML from the CSW source.  Prints xml out to be piped to another command or to a file.

```
./harvest_hnap.py > hnap.xml
or
./harvest_hnap.py | parsing_command
```

Presently extracts everything but will eventually extract a window of data (e.g.: metadata records updated in the last two weeks).  The alternate time filtering request available and commended out in the script.

This process runs in a few seconds depending on network latency.

## hnap2cc-json.py
Converts *HNAP* XML file to a *Common Core* mapped CKAN compliant JSON Lines file.  Accepts streamed in or file path as an argument and prints out JSON Lines output.

```
./harvest_hnap.py | ./hnap2json.py > CommonCore_CKAN.jsonl
or
cat hnap.xml | ./hnap2json.py > CommonCore_CKAN.jsonl
or
./hnap2json.py hnap.xml > CommonCore_CKAN.jsonl 
```

This process runs in a couple seconds.

## Import to CKAN
Uploading the JSON Lines file has been tested with the [ckanapi CLI](https://github.com/ckan/ckanapi)

```
ckanapi load datasets -I CommonCore_CKAN.jsonl -r http://target.ckan.instance.ca/ -a <user api key>
```

This process runs, depending on how much data is being pushed, in under 20 seconds.

## Timing
Since each of these commands totalled run in under a minute this process could safely cycle every 5 minutes but considering how the GeoNetwork uploads in batches (and other departments might too) we should be more careful.

From a process standpoint, for R1 daily or weekly is reasonable.  We’ll start assuming weekly till we hear otherwise.