from .base import Task
from datasets import load_dataset  # 导入 load_dataset 方法

import sys
sys.path.append("..")
from prompts import (
    make_direct_output_prompt,
    make_RAG_details_output_prompt,
    make_RAG_no_details_output_prompt,
    make_cot_output_prompt,
    make_cot_direct_output_prompt

)

class OutputPrediction(Task):
    """A task represents an entire benchmark including its dataset, problems,
    answers, generation settings and evaluation methods.
    """
#####################################################
    #DATASET_PATH = "/data/zxh/ApiDataset/data/DS1000_reasoning.jsonl"
    DATASET_PATH = "/data/zxh/ApiDataset/data/MonkBeatEval_reasoning.jsonl"
    #DATASET_PATH = "/data/zxh/ApiDataset/data/torchdata_reasoning.jsonl"
    DATASET_NAME = None
    #RAG_PATH = "/data/zxh/ApiDataset/RAG/total_RAG_result_top_1.jsonl"
    #RAG_PATH = "/data/zxh/ApiDataset/RAG/total_RAG_result.jsonl"

    def __init__(self, cot = False, phind_output = False):
        self.cot = cot
        self.phind_output = phind_output

        if self.phind_output:
            stop_words = ["# done"]
        else:
            stop_words = ["[/ANSWER]"]

        super().__init__(
            stop_words=stop_words,
            requires_execution=False,
        )

    def get_dataset(self):
        """Returns dataset for the task or an iterable of any object, that get_prompt can handle"""
        return self.dataset

    def get_prompt(self, doc):
        return make_direct_output_prompt((doc["code"], doc["test"]))
        #return make_cot_output_prompt((doc["code"], doc["test"]))
        #return make_cot_direct_output_prompt((doc["code"], doc["test"]))
        #return make_RAG_details_output_prompt((doc["ID"], doc["code"], doc["test"]), self.RAGdata)
        #return make_RAG_no_details_output_prompt((doc["ID"], doc["code"], doc["test"]), self.RAGdata)

    def get_reference(self, doc):
        return (doc["code"], doc["test"])

    def postprocess_generation(self, generation, idx):
        prompt = self.get_prompt(self.get_dataset()[idx])
        assert generation.startswith(prompt)
        generation = generation[len(prompt):]

        if self.cot:
            if "[ANSWER]" in generation:
                generation = generation.split("[ANSWER]")[1].strip()
        if "==" in generation:
            generation = generation.split("==")[1].strip()
        return generation.strip()

    def process_results(self, generations, references):
        return {}