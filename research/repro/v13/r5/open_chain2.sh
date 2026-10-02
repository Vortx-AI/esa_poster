#!/bin/bash
M=/tmp/claude-0/-home-user-esa-poster/0db6b3ad-8059-51a6-bd74-2d7a97faf986/scratchpad/v8/followup-G2-two-llm-plugin-handoff
cd /home/user/esa_poster/research/repro/v13/r5
Q=$M/models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf
$M/venv/bin/python run_open.py $Q qwen2.5-7b-instruct-q4_k_m >> logs/open_qwen7b.log 2>&1
$M/venv/bin/python crossruntime_43.py qwen $Q > logs/crossruntime_qwen.log 2>&1
rm -f $M/models/qwen2.5-7b-instruct-q4_k_m-0000*.gguf
$M/venv/bin/python run_open.py $M/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf llama-3.2-3b-instruct-q4_k_m > logs/open_llama3b.log 2>&1
rm -f $M/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf
$M/venv/bin/python run_open.py $M/models/google_gemma-3-4b-it-Q4_K_M.gguf gemma-3-4b-it-q4_k_m > logs/open_gemma4b.log 2>&1
rm -f $M/models/google_gemma-3-4b-it-Q4_K_M.gguf
curl -sL --retry 5 -o $M/models/microsoft_Phi-4-mini-instruct-Q4_K_M.gguf "https://huggingface.co/bartowski/microsoft_Phi-4-mini-instruct-GGUF/resolve/main/microsoft_Phi-4-mini-instruct-Q4_K_M.gguf"
$M/venv/bin/python run_open.py $M/models/microsoft_Phi-4-mini-instruct-Q4_K_M.gguf phi-4-mini-instruct-q4_k_m > logs/open_phi4mini.log 2>&1
echo CHAIN_DONE > logs/open_chain.done
