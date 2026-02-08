import json
from collections import defaultdict
import numpy as np

def pass_at_k(n, c, k):
    if n - c < k: return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

with open("/data/zxh/CodeGlance/evaluation/evaluation_results/MonkBeatEval_pre-qwen2.5-coder-7b-instruct-chat_temp0.8_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

raw_scored_generations = data.get("raw_scored_generations", {})

with open("/data/zxh/CodeGlance/data/MonkBeatEval_reasoning.jsonl", "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]

id_mapping = {str(index): item["ID"] for index, item in enumerate(data)}
merged_data = defaultdict(list)

for sample_key, values in raw_scored_generations.items():
    sample_index = sample_key.replace("sample_", "") 
    id_value = id_mapping.get(sample_index, sample_key)  
    merged_data[id_value].extend(values)  

final_jsonl_data = []
pass_at_1s, pass_at_3s, pass_at_5s, pass_at_10s = [], [], [], []

for task_id, execution_result in merged_data.items():
    c, n = execution_result.count(True), len(execution_result)
    pass_at_1 = pass_at_k(n, c, 1)
    pass_at_3 = pass_at_k(n, c, 3)
    pass_at_5 = pass_at_k(n, c, 5)
    pass_at_10 = pass_at_k(n, c, 10)
    
    pass_at_1s.append(pass_at_1)
    pass_at_3s.append(pass_at_3)
    pass_at_5s.append(pass_at_5)
    pass_at_10s.append(pass_at_10)
    
    final_jsonl_data.append({
        "ID": task_id,
        "raw_scored_generations": execution_result,
        "pass_at_1": pass_at_1 * 100
    })

final_output = {
    "pass_at_1": sum(pass_at_1s) / len(pass_at_1s) * 100,
    "pass_at_3": sum(pass_at_3s) / len(pass_at_3s) * 100,
    "pass_at_5": sum(pass_at_5s) / len(pass_at_5s) * 100,
    "pass_at_10": sum(pass_at_10s) / len(pass_at_10s) * 100
}

jsonl_path = "/data/zxh/CodeGlance/evaluation/evaluation_results_summary/MonkBeatEval_pre-qwen2.5-coder-7b-instruct-chat_temp0.8_output.json"
with open(jsonl_path, "w", encoding="utf-8") as f:
    for entry in final_jsonl_data:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

json_path = "/data/zxh/CodeGlance/evaluation/evaluation_results_summary/MonkBeatEval_pre-qwen2.5-coder-7b-instruct-chat_temp0.8_summary.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(final_output, f, ensure_ascii=False, indent=4)

print("Pass@k: ", {k: round(v, 2) for k, v in final_output.items()})
print("task num: ", len(merged_data))



