#!/bin/bash
 
nohup ollama serve &

if [ -z "$( ollama ls | grep medgemma-q6-limitado )" ]; then
    echo "<!> LOADING MODEL"
    ollama pull hf.co/unsloth/medgemma-27b-it-GGUF:Q6_K
    echo "FROM hf.co/unsloth/medgemma-27b-it-GGUF:Q6_K" > Modelfile
    echo "PARAMETER num_ctx 16384" >> Modelfile
    ollama create medgemma-q6-limitado -f Modelfile
    ollama rm hf.co/unsloth/medgemma-27b-it-GGUF:Q6_K
fi

tail -f /dev/null