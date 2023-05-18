import copy
import json
import math
def get_table_mapping(table,fact):
    for i in range(len(table)):
        for j in range(len(table[i])):
            if str(fact) in table[i][j]:
                return [i,j]
            try:
                if abs(float(table[i][j].replace('%', '').replace(')', '').replace('(', '').replace('$', '').replace(",", "")))== abs(fact):
                    return [i,j]
            except:
                pass
    return None

def get_para_mapping(para,fact):
    # print(fact)
    for p in para:
        text = p["text"].lower()
        # print(text)
        rel_index = p["order"]
        try:
            start_idx = text.index(fact.lower())
        except:
            continue
        end_idx = start_idx + len(fact)
        return rel_index,[start_idx,end_idx] 
    return None,None

def get_mapping(table,para,facts):
    mapping = {"table":[],"paragraph": {}}
    for fact in facts:
        if isinstance(fact,float):
            if math.isnan(fact):
                continue
            if int(fact) == fact:
                fact = int(fact)
        tm = get_table_mapping(table,fact)
        # print(tm)
        # exit(0)
        if tm!=None:
            mapping["table"].append(tm)
        para_id,interval = get_para_mapping(para,fact)
        # print(para_id,interval)
        if para_id!=None:
            if not para_id in mapping["paragraph"]:
                mapping["paragraph"][para_id] = []
            mapping["paragraph"][para_id].append(interval)
    if len(mapping["table"])==0:
        del mapping["table"]
    if len(mapping["paragraph"]) == 0:
        del mapping["paragraph"]
    return mapping

data = json.load(open("dataset_tagop/tatqa_dataset_train.json"))
pred_data = json.load(open("predict_st_for_iter1/pred_result_on_train.json"))
for item in data:
    table = item["table"]["table"]
    para = item["paragraphs"]
    questions = copy.deepcopy(item["questions"])
    pseudo_questions = []
    for q in questions:
        uid = q['uid']
        if not uid in pred_data:
            print("key error:",uid)
            continue
        pred_answer = pred_data[uid]["pred_answer"]
        if not isinstance(pred_answer,list):
            pred_answer = [pred_answer]
        if len(pred_answer)==0:
            continue
        q["answer"] = pred_answer
        del q["derivation"]
        q["answer_type"] = pred_data[uid]["answer_type"]
        q["answer_from"] = pred_data[uid]["answer_from"]
        q["facts"] = list(set(pred_data[uid]["facts"]))
        q["mapping"] = get_mapping(table,para,q["facts"])
        # q["mapping"] = {}
        del q["rel_paragraphs"]
        del q["req_comparison"]
        q["scale"] = pred_data[uid]["pred_scale"]
        q["predict_num_order"] = pred_data[uid]["predict_num_order"]
        q["operator_class"] = pred_data[uid]["operator_class"]
        pseudo_questions.append(q)
    item["questions"] = pseudo_questions

syn_data = json.load(open("dataset_tagop/tatqa_dataset_synthetic_data.json"))
print(len(syn_data))
print(len(data))

agg_data = syn_data+data

with open("dataset_tagop/tatqa_dataset_syn+pseudo_train.json",'w') as f:
    f.write(json.dumps(agg_data))