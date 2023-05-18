import re
import json
from re import RegexFlag

src_path = "examples/predict_train_uctr_iter_1_0205/generate-train.txt"
with open(src_path, "r", encoding="utf8") as generate_f:
    file_content = generate_f.read()

data = []
predict_outputs = re.findall("^D.+", file_content, RegexFlag.MULTILINE)
ground_outputs = re.findall("^T.+", file_content, RegexFlag.MULTILINE)
source_inputs = re.findall("^S.+", file_content, RegexFlag.MULTILINE)

succ_cnt = 0
noise_cnt = 0
duplicate_cnt = 0
question2pseudo_lable={}
print("len of al samples:",len(predict_outputs))
for predict, ground, source in zip(predict_outputs, ground_outputs, source_inputs):
    try:
        predict_id, predict_score, predict_clean = predict.split('\t')
        ground_id, ground_clean = ground.split('\t')
        source_id, source_clean = source.split('\t')
        assert predict_id[2:] == ground_id [2:]
        assert ground_id[2:] == source_id[2:]
        if float(predict_score) > -100:
            if source_clean.split("col :")[0].strip().lower() in question2pseudo_lable:
                # print(source_clean.split("col :")[0].strip().lower())
                duplicate_cnt += 1
                succ_cnt -= 1
                del question2pseudo_lable[source_clean.split("col :")[0].strip().lower()]
                continue
            succ_cnt += 1
            question2pseudo_lable[source_clean.split("col :")[0].strip().lower()] = predict_clean
            if predict_clean.lower().strip()!= ground_clean.lower().strip():
                noise_cnt += 1
    except Exception:
        print("An error occurred in source: {}".format(source))
        continue
with open("question2pseudo_label.json",'w') as f:
    f.write(json.dumps(question2pseudo_lable))
print("succ_cnt",succ_cnt)
print("noise_cnt",noise_cnt)
print("duplicate_cnt",duplicate_cnt)




import json
question2id = {}
path = "examples/raw_dataset/wikisql/data/train.jsonl"
with open(path) as f:
    line = f.readline()
    while line:
        d = json.loads(line)
        q = d["question"].lower().replace("\u00A0", " ").strip()
        tab_id = d["table_id"]
        if q in question2id: #avoid duplicate
            del question2id[q]
        else:
            question2id[q] = tab_id
        line = f.readline()
print(len(question2id))
with open("train_question2id.json",'w') as f:
    f.write(json.dumps(question2id))





#construct pseudo_samples
import json
out_f = open("pseudo_sample_iter2.json",'w')

with open("train_question2id.json") as f:
    train_question2id = json.load(f)

with open("question2pseudo_label.json") as f:
    question2pseudo_label = json.load(f)

for q,label in question2pseudo_label.items():
    # print(q)
    q = q.replace(u'\xa0', u' ')
    sample = {}
    sample["phase"] = 1
    if not q in train_question2id:
        print("error occur "+q)
        continue
    sample["table_id"] = train_question2id[q]
    sample["question"] = q
    sample["answer"] = label.split(",")
    out_f.write(json.dumps(sample)+"\n")

out_f.close()