
import json
# prepare data for eval
input_f = open("data/train.jsonl")
out_f = open("data/train_for_eval_0509.jsonl",'w')
header = {"id": "", "claim": "", "label": "", "evidence": "", "annotator_operations": ""}
out_f.write(json.dumps(header)+"\n")
line = input_f.readline()
line = input_f.readline()
while line:
    line = json.loads(line)
    line["predicted_evidence"] = line["evidence"][0]["content"]
    out_f.write(json.dumps(line)+"\n")
    line = input_f.readline()
# print(line)
out_f.close()
