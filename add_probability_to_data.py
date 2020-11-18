'''
Add probability to existing file
argv[1]: prob_dictionary_v2.pk
argv[2]: conversion.txt
argv[3]: WarnerMcQueenCutler_RawData_withoutFL.txt
'''

import sys
import pickle
from collections import defaultdict

prob_dict = pickle.load(open(argv[1], 'rb'))

mono_dict = prob_dict['monophone']
diphone_dict = prob_dict['diphone']

### Create dictionary to convert response to diphone, and be to diphone

with open(sys.argv[2], 'r') as f:
	data = f.readlines()

conv = {}
r2d = {}
feat = {}

for i in range(1, len(data)):
	line = data[i].rstrip()

	ipa, cmu, be, diphone, resp, voc, man = line.split("\t")

	if be != "":
		conv[diphone] = be
		r2d[resp] = be

	feat[diphone] = defaultdict(dict)
	feat[diphone]["voc"] = voc
	feat[diphone]["man"] = man

### Create dictionary for probabilities 
prob = {}

for k in sorted(list(mono_dict.keys())):
	monoph_prob = mono_dict[k] / mono_dict['total_monophone']

	if k in conv:
		k = conv[k]

	prob[k] = monoph_prob

for k in sorted(list(diphone_dict.keys())):
	seg1, seg2 = k.split("-")
	diphone_prob = diphone_dict[k] / diphone_dict['total_diphone']
	seg1 = conv[seg1]
	seg2 = conv[seg2]
	diphone_key = "%s-%s" % (seg1, seg2)
	prob[diphone_key] = diphone_prob / prob[seg1]


### Working on datafile

with open(sys.argv[3], "r") as f:
	data = f.readlines()

header = data[0].rstrip()

overall_header = "Gate\tseg2\toverallProb\trespProb\tVOC\tMAN\n"
transit_header = "Gate\tseg1\tseg2\tdiphone\trespFreq\ttranProb\trespProb\tVOC\tMAN\n"
