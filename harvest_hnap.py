#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CSW metadata extraction
# Output of this script is parsed by another into OGDMES-CKAN JSON.

# CMAJ: Shamlessly pillaged Ross Thompson's test script
# CMAJ: EC's (Mark Shaw, D. Sampson) XML Filters
# CMAJ: Tom Kralidis attempted to modernise our use of OWSLib
# CMAJ: Assembled by Chris Majewski @ StatCan

# CSW issues go to        : fgp-pgf@nrcan-rncan.gc.ca
# Metadata issues go to   : fgp-pgf@nrcan-rncan.gc.ca
# Open Data issues got to : open-ouvert@tbs-sct.gc.ca

# Called by OWSlib but may be requried if if a proxy is required
# No harm calling it early
import urllib2
# Requirement - OWSLib
# This script was writen to use OD's for of OWSLib
# > git clone https://github.com/open-data/OWSLib
# > cd /location/you/cloned/into
# > sudo python setup.py install
from owslib.csw import CatalogueServiceWeb
# Importing from a harvester.ini file
import os.path

# Connection variables
csw_url = 'csw.open.canada.ca/geonetwork/srv/csw'
csw_user = None
csw_passwd = None

proxy_protocol = None
proxy_url = None
proxy_user = None
proxy_passwd = None

# Or read from a .ini file
harvester_file = 'harvester.ini'
if os.path.isfile(harvester_file):
    from ConfigParser import ConfigParser

    ini_config = ConfigParser()

    ini_config.read(harvester_file)

    csw_url = ini_config.get('csw', 'url')
    if ini_config.has_option('csw', 'username'):
        csw_user = ini_config.get('csw', 'username')
        csw_passwd = ini_config.get('csw', 'password')

    proxy_protocol = ini_config.get('proxy', 'protocol')
    proxy_url = ini_config.get('proxy', 'url')
    proxy_user = ini_config.get('proxy', 'username')
    proxy_passwd = ini_config.get('proxy', 'password')

# If your supplying a proxy
if proxy_url:
    # And your using authentication
    if proxy_user and proxy_passwd:
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, proxy_url, proxy_user, proxy_passwd)
        proxy_auth_handler = urllib2.ProxyBasicAuthHandler(password_mgr)
    # or even if your not
    else:
        proxy_auth_handler = urllib2.ProxyHandler({proxy_protocol: proxy_url})

    opener = urllib2.build_opener(proxy_auth_handler)
    urllib2.install_opener(opener)

# Fetch the data
# csw = CatalogueServiceWeb(
#   'http://csw_user:csw_pass@csw_url/geonetwork/srv/csw')
if csw_user and csw_passwd:
    csw = CatalogueServiceWeb(
        'http://'+csw_url,
        username=csw_user,
        password=csw_passwd,
        timeout=20)
else:
    csw = CatalogueServiceWeb('http://'+csw_url, timeout=20)

# Filter records into latest updates
#
# Sorry Tom K., we'll be more modern ASAWC.  For now it's good ol' Kitchen Sink
#
# from owslib.fes import PropertyIsGreaterThanOrEqualTo
# modified = PropertyIsGreaterThanOrEqualTo('apiso:Modified', '2015-04-04')
# csw.getrecords2(constraints=[modified])
#
# Kitchen Sink is the valid HNAP, we need HNAP for R1 to debug issues
# This filter was supplied by EC, the CSW service technical lead
csw.getrecords2(format='xml', xml="""<?xml version="1.0"?>
<csw:GetRecords
    xmlns:csw="http://www.opengis.net/cat/csw/2.0.2"
    service="CSW"
    version="2.0.2"
    resultType="results"
    outputSchema="csw:IsoRecord">
    <csw:Query
        typeNames="gmd:MD_Metadata">
        <csw:ElementSetName>full</csw:ElementSetName>
        <csw:Constraint
            version="1.1.0">
            <Filter
                xmlns="http://www.opengis.net/ogc"
                xmlns:gml="http://www.opengis.net/gml"/>
        </csw:Constraint>
    </csw:Query>
</csw:GetRecords>
""")

# When we move to Tom K's filter we can use results in an R2 unified harvester
# print csw.results
# for rec in csw.records:
#    print '* '+csw.records[rec].title
#  Till then we need to collect and dump the response from the CSW
print csw.response

# #### END

# #### Storage
# FGP supplied filters ( Apply "since X" when possible )
# <csw:GetRecords
#   xmlns:csw="http://www.opengis.net/cat/csw/2.0.2"
#   service="CSW" version="2.0.2"
#   resultType="results"
#   outputSchema="csw:IsoRecord">
# 	<csw:Query
#       xmlns:gmd="http://www.isotc211.org/2005/gmd"
#       typeNames="gmd:MD_Metadata">
# 		<csw:Constraint version="1.1.0">
# 			<Filter
#               xmlns="http://www.opengis.net/ogc"
#               xmlns:gml="http://www.opengis.net/gml">
# 				<PropertyIsGreaterThanOrEqualTo>
# 					<PropertyName>Modified</PropertyName>
# 					<Literal>2015-04-04</Literal>
# 				</PropertyIsGreaterThanOrEqualTo>
# 			</Filter>
# 		</csw:Constraint>
# 	</csw:Query>
# </csw:GetRecords>
#
# <?xml version="1.0"?>
# <csw:GetRecords
#   xmlns:csw="http://www.opengis.net/cat/csw/2.0.2"
#   service="CSW"
#   version="2.0.2"
#   resultType="results"
#   outputSchema="csw:IsoRecord">
#   <csw:Query
#       typeNames="gmd:MD_Metadata">
#       <csw:Constraint
#           version="1.1.0">
#                <Filter
#                   xmlns="http://www.opengis.net/ogc"
#                   xmlns:gml="http://www.opengis.net/gml">
#                <And>
#                   <PropertyIsGreaterThanOrEqualTo>
#                   <PropertyName>Modified</PropertyName>
#                       <Literal>2015-04-04</Literal>
#                   </PropertyIsGreaterThanOrEqualTo>
#                   <PropertyIsLessThanOrEqualTo>
#                   <PropertyName>Modified</PropertyName>
#                       <Literal>2015-04-07T23:59:59</Literal>
#                   </PropertyIsLessThanOrEqualTo>
#                </And>
#                </Filter>
#        </csw:Constraint>
#    </csw:Query>
# </csw:GetRecords>
