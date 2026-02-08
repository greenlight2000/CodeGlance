run_names=(
    "PanNumEval_qwen2.5-coder-3b-instruct+RAG_source_code_temp0.8_output"
    "PanNumEval_qwen2.5-coder-7b-instruct+RAG_source_code_temp0.8_output"
    "PanNumEval_qwen2.5-coder-14b-instruct+RAG_source_code_temp0.8_output"
    "PanNumEval_qwen2.5-coder-32b-instruct+RAG_source_code_temp0.8_output"
    "PanNumEval_qwen2.5-coder-3b-instruct+RAG_example_temp0.8_output"
    "PanNumEval_qwen2.5-coder-7b-instruct+RAG_example_temp0.8_output"
    "PanNumEval_qwen2.5-coder-14b-instruct+RAG_example_temp0.8_output"
    "PanNumEval_qwen2.5-coder-32b-instruct+RAG_example_temp0.8_output"
)

mkdir -p evaluation_results 

for run_name in "${run_names[@]}"; do
    echo "Processing: $run_name"

    python evaluate_generations.py \
        --generations_path "../model_generations/${run_name}/generations.json" \
        --scored_results_path "evaluation_results/${run_name}.json" \
        --mode output
done
