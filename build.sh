#!/bin/sh

set -eu

CWD=$(basename "$PWD")

set_gpu_arg() {
    while [ "$#" -gt 0 ]; do
        if [ "$1" = "--device" ] && [ "$2" = "gpu" ]; then
            GPU_ARG="--gpus=all"
            return
        fi
        shift
    done
    GPU_ARG=""
}

build() {
    docker build . --tag "$CWD"
}

clean() {
    docker system prune -f
}

dev() {
    docker run --rm --gpus=all --entrypoint=sh \
        -v huggingface:/home/huggingface/.cache/huggingface \
        -v "$PWD"/output:/home/huggingface/output \
        -it "$CWD"
}

pull() {
    GHCR="ghcr.io/azher-alnabi/anime-stable-diffusion-docker-container"
    docker pull "$GHCR"
    docker tag "$GHCR" "$CWD"
}

run() {
    set_gpu_arg "$@"
    docker run --rm ${GPU_ARG} \
        -v huggingface:/home/huggingface/.cache/huggingface \
        -v "$PWD"/output:/home/huggingface/output \
        "$CWD" "$@"
}

tests() {
    run --skip \
        --prompt "1girl, green hair, long hair, yellow eyes, warrior armor, warrior princess, tanned-black skin, battle field, shadows, lens flare, masterpiece" \
        --negative-prompt "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name" 
}

mkdir -p output
case ${1:-build} in
    build) build ;;
    clean) clean ;;
    dev) dev "$@" ;;
    pull) pull ;;
    run) shift; run "$@" ;;
    test) tests ;;
    *) echo "$0: No command named '$1'" ;;
esac
