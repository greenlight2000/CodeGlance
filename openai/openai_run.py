import os
import json
from itertools import product

from openai_prompt import (
    batch_prompt_direct_output,
    batch_prompt_RAG_output

)

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "..", "data", "torchdata_reasoning.jsonl")
#RAG_path = "/data/zxh/ApiDataset/RAG/total_RAG_result_top_1.jsonl"


def run_openai(model, mode, temperature):
    # dataset = [json.loads(l) for l in open("../data/DS1000_reasoning.jsonl", "r").readlines()]
    with open(file_path, "r") as f:
        dataset = [json.loads(line) for line in f.readlines()]

    ###################add ID
    # prompts = [(data["ID"], data["code"], data["test"]) for data in dataset] 
    prompts = [( data["code"], data["test"]) for data in dataset] 


    # add RAG knowledge base
    # with open(RAG_path, "r", encoding="utf-8") as f:
    #     ragdata =  json.load(f)

    
    max_tokens = 100

    fn = batch_prompt_direct_output
    #fn = batch_prompt_RAG_output


    #############add RAG knowledge base
    outputs = fn(prompts, temperature=temperature, n=10, model=model, max_tokens=max_tokens, stop=["[/ANSWER]"])
    save_dir = get_save_dir(mode, model, temperature)
    outputs_dict = {f"sample_{i}": [j[0] for j in o] for i, o in enumerate(outputs)}
    json.dump(outputs_dict, open(save_dir, "w"))
    return outputs

def get_save_dir(mode, model, temperature):
    base_dir = os.path.join(os.path.dirname(current_dir), "model_generations", f"torchdata_{model}_temp{temperature}_{mode}")
    try: os.makedirs(base_dir)
    except: pass
    return os.path.join(base_dir, "generations.json")
        
if __name__ == "__main__":
    models = ["gpt-4o-2024-11-20"]
    modes = ["output"]
    temperatures = [0.8]
    for model, mode, temperature in product(models, modes, temperatures):
        run_openai(model, mode, temperature)
        break # comment out to run the whole thing 