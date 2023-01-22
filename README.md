# Stable Diffusion in Docker

```sh
./build.sh run --device cpu 'An impressionist painting of a parakeet eating spaghetti in the desert'
```

![An impressionist painting of a parakeet eating spaghetti in the desert 1](img/An_impressionist_painting_of_a_parakeet_eating_spaghetti_in_the_desert_s1.png)
![An impressionist painting of a parakeet eating spaghetti in the desert 2](img/An_impressionist_painting_of_a_parakeet_eating_spaghetti_in_the_desert_s2.png)

## Before you start

### Minimum requirements

By default, this pipeline focuses on only using the CPU. 
It will take a few minutes to create one image.
Make sure to only use `--device cpu` 

### Huggingface token

Since it uses the official model, you will need to create a [user access token](https://huggingface.co/docs/hub/security-tokens)
in your [Huggingface account](https://huggingface.co/settings/tokens). Save the
user access token in a file called `token.txt` and make sure it is available
when building the container. The token content should begin with `hf_...`

## Quickstart

The pipeline is managed using a single [`build.sh`](build.sh) script.

Pull the latest version of `stable-diffusion-docker` using `./build.sh pull`.
You will need to use the option `--token` to specify a valid [user access token](#huggingface-token)
when using [`./build run`](#run).

Alternately, build the image locally before running it.

## Build

Make sure your [user access token](#huggingface-token) is saved in a file called
`token.txt`.

To build:

```sh
./build.sh build  # or just ./build.sh
```

## Run

### Text-to-Image (`txt2img`)

To run:

```sh
./build.sh run 'Andromeda galaxy in a bottle'
```

### Options

Some of the options from [`txt2img.py`](https://github.com/CompVis/stable-diffusion/blob/main/scripts/txt2img.py)
are implemented for compatibility:

* `--prompt [PROMPT]`: the prompt to render into an image
* `--n_samples [N_SAMPLES]`: number of images to create per run (default 1)
* `--n_iter [N_ITER]`: number of times to run pipeline (default 1)
* `--H [H]`: image height in pixels (default 512, must be divisible by 64)
* `--W [W]`: image width in pixels (default 512, must be divisible by 64)
* `--scale [SCALE]`: unconditional guidance scale (default 7.5)
* `--seed [SEED]`: RNG seed for repeatability (default is a random seed)
* `--ddim_steps [DDIM_STEPS]`: number of sampling steps (default 50)

Other options:

* `--attention-slicing`: use less memory at the expense of inference speed
(default is no attention slicing)
* `--device [DEVICE]`: the cpu or cuda device to use to render images (default
`cpu`)
* `--half`: use float16 tensors instead of float32 (default `float32`)
* `--model [MODEL]`: the model used to render images (default is
`Linaqruf/anything-v3-better-vae`)
* `--negative-prompt [NEGATIVE_PROMPT]`: the prompt to not render into an image
(default `None`)
* `--scheduler [SCHEDULER]`: override the scheduler used to denoise the image
(default `None`)
* `--skip`: skip safety checker (default is the safety checker is on)
* `--token [TOKEN]`: specify a Huggingface user access token at the command line
instead of reading it from a file (default is a file)

## Examples

These commands are both identical:

```sh
./build.sh run 'abstract art'
./build.sh run --prompt 'abstract art'
```

Set the seed to 42:

```sh
./build.sh run --seed 42 'abstract art'
```

Options can be combined:

```sh
./build.sh run --scale 7.0 --seed 42 'abstract art'
```

This will only utilize CPU, you can try mixing and matching options:

* Make images smaller than 512x512 using `--W` and `--H` to decrease memory use
and increase image creation speed
* Use `--half` to decrease memory use but slightly decrease image quality
* Use `--attention-slicing` to decrease memory use but also decrease image
creation speed
* Decrease the number of samples and increase the number of iterations with
`--n_samples` and `--n_iter` to decrease overall memory use
* Skip the safety checker with `--skip` to run less code

```sh
./build.sh run --W 256 --H 256 --half \
  --attention-slicing --xformers-memory-efficient-attention \
  --n_samples 1 --n_iter 1 --skip --prompt 'abstract art'
```

On Windows, if you aren't using WSL2 and instead use MSYS, MinGW, or Git Bash,
prefix your commands with `MSYS_NO_PATHCONV=1` (or export it beforehand):

```sh
MSYS_NO_PATHCONV=1 ./build.sh run --half --prompt 'abstract art'
```

## Outputs

### Model

The model and other files are cached in a volume called `huggingface`. The
models are stored in `<volume>/diffusers/<model>/snapshots/<githash>/unet/<weights>`.
Checkpoint files (`ckpt`s) are unofficial versions of the official models, and
so these are not part of the official release.

### Images

The images are saved as PNGs in the `output` folder using the prompt text. The
`build.sh` script creates and mounts this folder as a volume in the container.
