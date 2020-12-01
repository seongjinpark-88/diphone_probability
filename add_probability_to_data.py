'''
Add probability to existing file
argv[1]: conversion.txt
argv[2]: WarnerMcQueenCutler_RawData_withoutFL.txt
'''

import sys
import pickle
import dill
from collections import defaultdict

prob_dict = pickle.load(open("../data/prob_data/prob_dictionary_v2.pk", 'rb'))

mono_dict = prob_dict['monophone']
diphone_dict = prob_dict['diphone']

### Create dictionary to convert response to diphone, and be to diphone

with open(sys.argv[1], 'r') as f:
	data = f.readlines()

conv = {}
r2d = {}
feat = {}

for i in range(1, len(data)):
	line = data[i].rstrip()

	ipa, cmu, be, diphone, resp, voc, man = line.split("\t")

	if be != "":
		conv[be] = diphone
		r2d[resp] = diphone

	feat[diphone] = defaultdict(dict)
	feat[diphone]["voc"] = voc
	feat[diphone]["man"] = man

r2d["X"] = "X"
r2d["x"] = "^"

### Create dictionary for probabilities 
prob = {}

for k in sorted(list(mono_dict.keys())):
	monoph_prob = mono_dict[k] / mono_dict['total_monophone']

	if k in conv:
		k = conv[k]

		prob[k] = monoph_prob

for k in sorted(list(diphone_dict.keys())):
	# print(k)
	k_check = k.replace("-", "")
	if (k_check.islower()) and (k != "total_diphone"):
			seg1, seg2 = k.split("-")
			diphone_prob = diphone_dict[k] / diphone_dict['total_diphone']
			try:
				seg1 = conv[seg1]
				seg2 = conv[seg2]
				diphone_key = "%s-%s" % (seg1, seg2)
				prob[diphone_key] = diphone_prob / prob[seg1]
			except:
				next

# print(prob)

### Load response data
response_keys = dill.load(open('../data/prob_data/keys.pk', 'rb'))
monophone_keys = response_keys['monophone']
diphone_keys = response_keys['diphone']

response_data = dill.load(open('../data/prob_data/data.pk', 'rb'))
monophone_gate_list = response_data['monophone']
diphone_gate_list = response_data['diphone']


### Working on datafile
overall_header = "Gate\tseg2\toverallProb\trespProb\tVOC\tMAN\n"
transit_header = "Gate\tseg1\tseg2\tdiphone\trespFreq\ttranProb\trespProb\tVOC\tMAN\n"

#### Monophone datafile

with open("../data/overallProbBuckeye.txt", "w") as outfile:
	outfile.write(overall_header)

	# Loop through gates
	for gate in monophone_keys.keys():

		tmp_dict = defaultdict(dict)
		# Loop through second segment
		for ans2 in monophone_keys[gate].keys():
			gate_idx = int(gate[-1]) - 1
			gate_dict = monophone_gate_list[gate_idx]
			seg2 = r2d[ans2]
			try: 
				overall_prob = prob[seg2]
			except:
				overall_prob = 1 / mono_dict['total_monophone']

			resp_prob = gate_dict[ans2] / gate_dict['total_mono']

			if resp_prob <= 0:
				resp_prob = 1 / gate_dict['total_mono']

			tmp_dict[seg2]['prob'] = overall_prob

			try:
				tmp_dict[seg2]['resp'] += resp_prob
			except:
				tmp_dict[seg2]['resp'] = resp_prob
			# except:
			# 	resp_prob = 1 / gate_dict['total_mono']

		for seg2 in list(tmp_dict.keys()):
			result = "%s\t%s\t%s\t%s\t%s\t%s\n" % (gate, seg2, tmp_dict[seg2]['prob'], tmp_dict[seg2]['resp'], feat[seg2]['voc'], feat[seg2]['man'])
			outfile.write(result)

# from pprint import pprint
# pprint(diphone_keys["g1"])
# pprint(diphone_gate_list[0]['b'])
# exit()
# print(r2d["ch"])
# exit()

with open("../data/transitionalProbBuckeye.txt", "w") as outfile:
	outfile.write(transit_header)
	for gate in diphone_keys.keys():
		for diphone in diphone_keys[gate].keys():
			# print(diphone)
			ans1, ans2 = diphone.split("-")
			gate_idx = int(gate[-1]) - 1
			gate_dict = diphone_gate_list[gate_idx]
			seg1 = r2d[ans1]
			# print(seg1, gate_dict[ans1])
			for ans2 in list(gate_dict[ans1].keys()):
				if ans2 != 'total':
					# print(gate, seg1, ans1, ans2)
					if ans2 in r2d:
						seg2 = r2d[ans2]
						diphone_seq = "%s-%s" % (seg1, seg2)
						try:
							transit_prob = prob[diphone_seq]
						except:
							transit_prob = (1 / diphone_dict['total_diphone']) / prob[seg1]
						try:
							resp_prob = gate_dict[ans1][ans2] / gate_dict[ans1]['total']
						except:
							resp_prob = 1 / gate_dict[ans1]['total']

						if resp_prob <= 0:
							resp_prob = 1 / gate_dict[ans1]['total']

						result = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (gate, seg1, seg2, diphone_seq, gate_dict[ans1][ans2], transit_prob, resp_prob, feat[seg2]['voc'], feat[seg2]['man'])
						# print(result)
						# exit()
						outfile.write(result)
