'''
calculate monophone and diphone probability from Buckeye corpus.
need one system argument: dir for buckeye corpus
'''

import os, sys
import pickle
from collections import defaultdict

def phone_conversion(phn):
	if phn == "en":
		return "n"
	elif phn == "em":
		return "m"
	elif phn == "eng":
		return "ng"
	elif phn == "el":
		return "l"
	elif phn == "hh":
		return "h"
	elif phn == "nx":
		return "n"
	elif phn == "tq":
		return "t"
	else:
		return phn


buckeye_path = sys.argv[1]
speaker_list = os.listdir(buckeye_path)

mono_dict = defaultdict(int)
di_dict = defaultdict(int)

for spk in speaker_list:
	print("WORKING ON SPEAKER ", spk)
	spk_path = os.path.join(buckeye_path, spk)

	phone_files = [os.path.join(spk_path, phn) for phn in os.listdir(spk_path) if phn.endswith(".phones")]

	for phone in phone_files:
		with open(phone, "r") as f:
			data = f.readlines()

		for i in range(9, len(data)):
			line = data[i].lstrip().rstrip()
			items = line.split()
			try:
				phn = items[2]
			except:
				phn = "EMPTY"
			phn = phn.replace(";", "")

			if "+" in phn:
				phn, _ = phn.split("+")

			if (phn != "eng") and (len(phn) == 3) and (phn.islower()):
				next_phn = phone_conversion(phn[-1])
				phn = phone_conversion(phn[:2])
				mono_dict[phn] += 1
				mono_dict[next_phn] += 1
				mono_dict["total_monophone"] += 2

				diphone = "%s-%s" % (phn, next_phn)

				di_dict[diphone] += 1
				di_dict["total_diphone"] += 1

			else:
				phn = phone_conversion(phn)
				mono_dict[phn] += 1
				mono_dict["total_monophone"] += 1

				if i + 1 < len(data):
					# print(data[i+1])
					next_line = data[i+1].lstrip().rstrip()
					next_items = next_line.split()
					try:
						next_phn = phone_conversion(next_items[2])
					except:
						next_phn = "EMPTY"
					next_phn = next_phn.replace(";", "")

					diphone = "%s-%s" % (phn, next_phn)
					di_dict[diphone] += 1
					di_dict["total_diphone"] += 1

for k in sorted(list(mono_dict.keys())):
	print(k, '\t', mono_dict[k])

prob_dict = {}
prob_dict["monophone"] = mono_dict
prob_dict["diphone"] = di_dict

with open('prob_dictionary_v2.pk', 'wb') as output:
	pickle.dump(prob_dict, output)


