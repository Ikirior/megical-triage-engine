FROM ubuntu

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y pciutils lshw
RUN apt-get install -y zstd
RUN apt-get install -y curl
RUN curl -fsSL https://ollama.com/install.sh | sh
CMD ["ollama","serve"]