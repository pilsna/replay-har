#!/usr/bin/env python
"""
Parse a HAR (HTTP Archive) and return URLs which resulted in a given HTTP response code
HAR Spec: http://groups.google.com/group/http-archive-specification/web/har-1-2-spec
Copyleft 2010 Ian Gallagher <crash@neg9.org>
 
Example usage: ./har_response_urls.py foo.har 404
"""
 
import json, urllib2, time, sys, glob, logging
from log import configuration

 
def loadUrl(url, file):
	logger.debug("loading a new url......")
	logger.debug(url)
	logger.debug(file)
	start_time = time.time()
	handler = urllib2.urlopen(url)
	size = handler.read().__sizeof__()
	end_time = time.time()
	logger.debug("start time: %0.3f" % start_time)
	logger.debug("end time: %0.3f" % end_time)
	time_diff = end_time - start_time
	line = "%d, %d, %0.3f, %s\n" % (handler.getcode(), size, time_diff, url)
	file.write(line)
	logger.debug(line)
	handler.close()  
	

def readHAR(har_file):
	# Read HAR archive (skip over binary header if present - Fiddler2 exports contain this)
	har_data = open(har_file, 'rb').read()
	skip = 3 if '\xef\xbb\xbf' == har_data[:3] else 0

	har = json.loads(har_data[skip:])
	matching_entries = har['log']['entries']
	matching_urls = set(map(lambda x: x['request']['url'], matching_entries))
	log_file = "%s-result.csv" % har_file
	with open(log_file, "w") as file:
		file.write("http code, size in bytes, time in s, url\n")
		for url in matching_urls:
			try:
				loadUrl(url, file)				
			except Exception, e:
				logger.exception(e)
				
if '__main__' == __name__:
	logger = configuration("http", "./logs", logging.DEBUG).create()

	har_files = glob.glob("data/*.har")
	logger.info(har_files)
	for har_file in har_files:
		try:
			logger.info("Starting read from file %s" % har_file)
			readHAR(har_file)
			logger.info("Stopped read from file %s" % har_file)
		except Exception, e:
			logger.exception(e)
	logger.info("Programmet er afsluttet.")
