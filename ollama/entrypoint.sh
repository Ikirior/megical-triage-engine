#!/bin/bash
 
nohup ollama serve &
ollama pull hf.co/unsloth/medgemma-27b-it-GGUF:Q6_K
echo "FROM hf.co/unsloth/medgemma-27b-it-GGUF:Q6_K" > Modelfile
echo "PARAMETER num_ctx 16384" >> Modelfile
ollama create medgemma-q6-limitado -f Modelfile
exec ollama run medgemma-q6-limitado