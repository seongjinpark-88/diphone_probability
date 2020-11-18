'''
calculate overall/transitional probability
argv[1]: WarnerMcQueenCutler_RawData_withoutFL.txt
'''

import sys
from collections import defaultdict

def ddict():
	return defaultdict(ddict)

# 1. Read data file

with open(sys.argv[1], 'r') as f:
	data = f.readlines()

# 2. Creat dict for each gate

g1 = defaultdict(dict)
g2 = defaultdict(dict)
g3 = defaultdict(dict)
g4 = defaultdict(dict)
g5 = defaultdict(dict)
g6 = defaultdict(dict)

mono_gate_dicts = [g1, g2, g3, g4, g5, g6]

dg1 = ddict()
dg2 = ddict()
dg3 = ddict()
dg4 = ddict()
dg5 = ddict()
dg6 = ddict()

di_gate_dicts = [dg1, dg2, dg3, dg4, dg5, dg6]

mono_gate_diphs = defaultdict(dict)
di_gate_diphs = defaultdict(dict)

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

	# 5. add freqeucncy
	dict_idx = gate - 1
	gate_key = "g%s" % gate
	
	## 5.1 monophone
	mono_gate_dicts[dict_idx][resp2] += 1
	mono_gate_dicts[dict_idx]['total_mono'] += 1
	mono_gate_diphs[gate_key][ans2] += 1
	
	## 5.2 diphone
	if int(seg1Acc) == 1:
		diph_key = "%s-%s" % (ans1, ans2)
		di_gate_dicts[dict_idx][resp1][resp2] += 1
		di_gate_dicts[dict_idx][resp1]['total'] += 1
		di_gate_diphs[gate_key][diph_key] += 1

	




