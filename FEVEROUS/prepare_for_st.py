
import json
# prepare data for self training
input_f = open("data/train_for_eval_0509.verdict.jsonl")
out_f = open("train_st_iter0/train.jsonl",'w')
header = {"id": "", "claim": "", "label": "", "evidence": "", "annotator_operations": ""}
out_f.write(json.dumps(header)+"\n")
line = input_f.readline()
line = input_f.readline()
while line:
    line = json.loads(line)
    line["label"] = line["predicted_label"]
    out_f.write(json.dumps(line)+"\n")
    line = input_f.readline()
# print(line)
out_f.close()