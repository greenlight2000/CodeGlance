export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export TORCH_DISTRIBUTED_DEBUG=OFF
export TORCH_CPP_LOG_LEVEL=ERROR
export CUDA_LAUNCH_BLOCKING=1

dirs=(
    "deepseek-coder-7b-instruct-v1.5"
    #"Qwen2.5-Coder-7B-Instruct"
    #"deepseek-coder-6.7b-instruct"
    )

models=(
    "deepseek-ai/deepseek-coder-7b-instruct-v1.5"
    #"Qwen/Qwen2.5-Coder-7B-Instruct"
    #"deepseek-ai/deepseek-coder-6.7b-instruct"
    )

temperatures=(0.8)

export CUDA_VISIBLE_DEVICES=0

for ((i=0; i<${#models[@]}; i++)); do
    model=${models[$i]}
    base_dir=${dirs[$i]}
    echo "Running model: $model on GPU 3"

    for temperature in "${temperatures[@]}"; do
        dir="MonkBeatEval_${base_dir}_temp${temperature}_output"

        SIZE=50
        mkdir -p model_generations_raw/$dir

        for ((i=0; i<1; i++)); do
            ip=$((i+1))
            echo "Starting iteration $i, processing range $((i*SIZE)) to $((ip*SIZE))"
            python /data/zxh/CodeGlance/inference/main.py \
                --model "/data/zxh/CodeGlance/models/${base_dir}" \
                --use_auth_token \
                --trust_remote_code \
                --tasks output_prediction \
                --batch_size 10 \
                --n_samples 10 \
                --max_length_generation 1024 \
                --precision bf16 \
                --limit "$SIZE" \
                --temperature "$temperature" \
                --save_generations \
                --save_generations_path model_generations_raw/${dir}/shard_${i}.json \
                --start "$((i*SIZE))" \
                --end "$((ip*SIZE))" \
                --shuffle \
                --max_tokens 1024\
                #--tensor_parallel_size 2
        done
    done
done
