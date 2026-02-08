# CodeGance
CodeGlance is a multi-dimensional benchmark investigating code reasoning challenges across three realistic scenarios:
intrinsic logic reasoning, API interaction reasoning, and unseen function reasoning. 


This repository includes replication prompts and five CodeGlance [datasets](./data) with code-feature annotations: Cruxeval, DS1000_reasoning, MonkBeatEval_reasoning, PanNumEval_reasoning, and torchdata_reasoning.

## Setup and Installation
Clone this repository by git

## Requirements
```python
pip install -r requirements.txt
```
The code has been tested with Python version 3.9 and CUDA version 12.1.

## Getting Started
The benchmark is available in `.jsonl` format in `data/`.
Except `cruxeval.jsonl`, each sample in other `.jsonl` files contains `ID`, `code`, `test`, `result` and some code features of every dataset, because these datasets are converted from their original code tasks to code reasoning tasks by ourselves.
Due to format incompatibility, please use the original CRUXEval framework for inference and evaluation. We have also provided a version of CRUXEval annotated with code features in the repository, which can be used to analyze the evaluation results of CRUXEval.


## Running Inference on On-premises Deployment Models
On-premises Deployment Models should be in `../models`.

First `cd inference`. Then, run `./scripts/run_output_prediction.sh` for inference. The default script in the repository runs a variety of models with 1 GPU's at temperatures `0.8` with `n_sample=10` generations per sample. You should change one or more of `GPUS, batch_size, n_samples, temperatures, dirs (directory names), models` and `size` for different datasets.

If you want to use RAG or CoT additionally, you can modify `./tasks/output_prediction.py`. In this file, you can also choose which dataset to inference.

By the way, each `.jsonl` file in the folder `RAG`, contains retrieval results of API information in different granularity from total API docs. Each entry of a `.jsonl` file means the APIs used in this code reasoning task of `DS1000_reasoning`, `MonkBeatEval_reasoning` or `PanNumEval_reasoning` datasets. The results can be add to prompts to increase the models' API knowledge.

This script can parallelize samples of the benchmark in a data-parallel fashion across the GPU's. After running the scripts, the generations will appear in `inference/model_generations_raw/shard_i.json`, where `i` ranges from `0` to `GPUS-1`. To convert these into a form that is readily available for evaluation, run `python combine_generations.py`, which will create a file `../model_generations/{MODEL_datasets_INFO}/generations.json`. The generations can then be evaluated by following the above instructions.

## Running Inference on OpenAI Models
You need to use your own API key and comply with OpenAI terms of use. We provide a script to run inference on OpenAI models if you would like to try different temperatures or latest models. `cd openai` and run `python openai_run.py`. Like before, the generations will appear in `../model_generations/{MODEL_INFO}/generations.json`.

Different prompts(like RAG, Cot and others) and datasets are choosed in `openai_prompt.py`, and API key also must be set in `openai_prompt.py`.


## Scoring a Batch of Generations and summarize Results
Finally, we provide scripts to run evaluation on many models in parallel in `evaluation/evaluate_all_predictions_output.sh`. You should change `run_names`. For convenience, we have provided a script `evaluation/convert_evaluation_results.py` that can summarize the evaluation results. 
All raw results (`raws`) and pass@k scores can then be found in the `evaluation/evaluation_results` folder. Running `evaluation/convert_evaluation_results.py` will provide the results easier to understand in `evaluation/evaluation_results_summary`.

## Example
We provide an example inferrence and evaluation data named `deepseek-coder-7b-instruct-v1.5_temp0.8_output` in `model_generations`, `inference/model_generations_raw`, `evaluation/evaluation_results` and `evaluation/evaluation_results_summary` for you to see the results' format.


## Acknowledgements
This repository is built on top of [`facebookresearch/cruxeval`](https://github.com/facebookresearch/cruxeval) and [`xlang-ai/DS-1000`](https://github.com/xlang-ai/DS-1000), and we thank the contributors of these repos for their awesome works! 
