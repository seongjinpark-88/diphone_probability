'''
calculate overall/transitional probability
argv[1]: WarnerMcQueenCutler_RawData_withoutFL.txt
'''

import sys
import dill
from collections import defaultdict

def ddict():
	return defaultdict(ddict)

# 1. Read data file

with open(sys.argv[1], 'r') as f:
	data = f.readlines()

# 2. Creat dict for each gate

g1 = defaultdict(int)
g2 = defaultdict(int)
g3 = defaultdict(int)
g4 = defaultdict(int)
g5 = defaultdict(int)
g6 = defaultdict(int)

mono_gate_dicts = [g1, g2, g3, g4, g5, g6]

dg1 = defaultdict(lambda: defaultdict(int))
dg2 = defaultdict(lambda: defaultdict(int))
dg3 = defaultdict(lambda: defaultdict(int))
dg4 = defaultdict(lambda: defaultdict(int))
dg5 = defaultdict(lambda: defaultdict(int))
dg6 = defaultdict(lambda: defaultdict(int))

di_gate_dicts = [dg1, dg2, dg3, dg4, dg5, dg6]

mono_gate_diphs = defaultdict(lambda: defaultdict(int))
di_gate_diphs = defaultdict(lambda: defaultdict(int))

# 3. Loop through line by line

for i in range(1, len(data)):
	line = data[i].rstrip()

	# 4. split the columns
	items = line.split("\t")
	diphone_name = items[2]
	gate = int(items[6])
	ans1 = items[10]
	ans2 = items[11]
	resp1 = items[12]
	resp2 = items[13]
	seg1Acc = items[14]
	seg2Acc = items[15]

	if ans2 != "F" and ans2 != "L" and ans1 != "F" and ans2 != "L":

		# 5. add freqeucncy
		dict_idx = gate - 1
		gate_key = "g%s" % gate
		
		## 5.1 monophone
		mono_gate_dicts[dict_idx][resp2] += 1
		mono_gate_dicts[dict_idx]['total_mono'] += 1
		### Add key for later use
		mono_gate_diphs[gate_key][ans2] += 1
		
		## 5.2 diphone
		if ans1 == resp1:
			diph_key = "%s-%s" % (ans1, ans2)
			di_gate_dicts[dict_idx][resp1][resp2] += 1
			di_gate_dicts[dict_idx][resp1]['total'] += 1
			### Add key for later use
			di_gate_diphs[gate_key][diph_key] += 1


diphone_keys = {}
diphone_keys['monophone'] = mono_gate_diphs
diphone_keys['diphone'] = di_gate_diphs

from pprint import pprint
pprint(di_gate_diphs["g2"])
pprint(di_gate_dicts[0])
	
diphone_data = {}
diphone_data['monophone'] = mono_gate_dicts
diphone_data['diphone'] = di_gate_dicts

with open("../data/prob_data/keys.pk", 'wb') as output:
	dill.dump(diphone_keys, output)

with open("../data/prob_data/data.pk", 'wb') as output:
	dill.dump(diphone_data, output)


