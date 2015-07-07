# Open Maps - Federal Geospatial Platform Harvester
The Open Government Secretariat's (OGS) Open Maps (OM) harvester pulling from the Federal Geospatial Platform (FGP) developed and maintained at Statistics Canada (StatCan).

![Harvester - FGP - Diagram](https://raw.githubusercontent.com/open-data/harvester-FGP/master/docs/Harvest%20Diagram.png)

## harvest_hnap.py
Extract HNAP XML from the CSW source.  Prints xml out to be piped to another command or to a file.

Presently extracts everything but will eventually extract a window of data (e.g.: metadata records updated in the last two weeks).

This process runs in a few seconds depending on network latency.

## hnap2ogdmes.py
Converts HNAP XML file to an OGDMES mapped CKAN compliant JSON Lines file.

This process runs in a couple seconds.

## Import to CKAN
Uploading the JSON Lines file has been tested with [ckanapi CLI](https://github.com/ckan/ckanapi)