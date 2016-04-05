#!/usr/local/bin/python
import argparse
import re
import pprint

pp = pprint.PrettyPrinter(indent=2)

parser = argparse.ArgumentParser(description="Process Fortigate configuration \
	and create communication matrix excel sheet.")
parser.add_argument('-f', action='store',
                   metavar='<configuration-file>',
                   help='path to configuration file',
                   required=True)

args = parser.parse_args()
CONFIGFILE = vars(args)['f']
print ("Parsing Configuration File: %s" % CONFIGFILE)

try:
	fullconfigstr = open(CONFIGFILE, 'r').read()
except:
	print("Error reading config file: %s" % CONFIGFILE)

fullconfiglines = fullconfigstr.splitlines()

allpolicies = fullconfiglines[fullconfiglines.index('config firewall policy')+1:]
allpolicies = allpolicies[:allpolicies.index('end')]

policydict = dict()

for line in allpolicies:
	try:
		if line.strip().startswith('edit'):
			policyid = re.match(r'edit (\d*)', line.strip()).groups()[0]
			policydict[policyid] = dict()
		elif line.strip() != 'next' and line.strip().startswith('set'):
			key, val = re.match(r'^set (\S*) (.+)$', line.strip()).groups()
			policydict[policyid][key] = val
	except:
		print "Error on line: %s" % line
		raise

print ("Total policies: %d" % len(policydict.keys()))


for pid in policydict.keys():
	for key in policydict[pid]:
		if key == 'service' or key == 'srcaddr' or key == 'dstaddr':
			policydict[pid][key] = policydict[pid][key].replace('" "', '","').replace('"', '')
			if key == 'service':
				policydict[pid][key] = policydict[pid][key].replace('_', '-')
			policydict[pid][key] = policydict[pid][key].split(',')
	pp.pprint(policydict[pid])
