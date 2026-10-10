FROM ghcr.io/ggml-org/llama.cpp:server
USER root
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
ARG MODEL_URL=https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf
RUN curl -L "$MODEL_URL" -o /model.gguf
ENTRYPOINT ["/app/llama-server","-m","/model.gguf","--host","0.0.0.0","--port","8080","-c","2048"]
