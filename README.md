# Stable Diffusion in Docker



```sh
<<<<<<< HEAD
./build.sh run --device cpu --prompt 'An impressionist painting of a parakeet eating spaghetti in the desert'
=======
./build.sh run --device cpu --skip \
--prompt "1girl, green hair, long hair, yellow eyes, warrior armor, warrior princess, tanned-black skin, battle field, shadows, lens flare, masterpiece" \ --negative-prompt "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name" 
>>>>>>> 8f59ea0 (Updated README)
```

![Warrior Princess](img/1girl,_green_hair,_long_hair,_yellow_eyes,_warrior_armor,_warrior_princess,_tanned-black_skin,_battle_field,_shadows,_lens_flare,_masterpiece__steps_20__scale_11.00__seed_9746260096546669498__n_1.png)
![Warrior Princess](img/1girl,_green_hair,_long_hair,_yellow_eyes,_warrior_armor,_warrior_princess,_tanned-black_skin,_battle_field,_shadows,_lens_flare,_masterpiece__steps_20__scale_11.00__seed_2951297131937974408__n_1.png)
![Warrior Princess](img/1girl,_green_hair,_long_hair,_yellow_eyes,_warrior_armor,_warrior_princess,_tanned-black_skin,_battle_field,_shadows,_lens_flare,_masterpiece__steps_20__scale_11.00__seed_9764299217508183519__n_1.png)



## Before you start

### Minimum requirements

<<<<<<< HEAD
By default, this pipeline focuses on only using the CPU. 
It will take a few minutes to create one image 
(Roughly 4 minutes and 50 seconds on a Ryzen 5 5600x CPU).
=======
By default, this pipeline focuses on only using the CPU as rendering on a GPU is extremely cost prohibitive.
It will take a few minutes to create one image.
>>>>>>> 8f59ea0 (Updated README)
Make sure to only use `--device cpu` 

## Quickstart

The pipeline is managed using a single [`build.sh`](build.sh) script.

Work in progress: Pull Functionality using `./build.sh pull`. 
Will pull latest image once it is available.

Currently, follow the build section to initialize Dockerfile.

## Build

To build:

```sh
./build.sh build  # or just ./build.sh
```

Work in progress: make sure your [user access token](#huggingface-token) is saved in a file called
`token.txt`.

## Testing


## Run

### Text-to-Image (`txt2img`)

To run:

```sh
./build.sh run --device cpu --prompt 'Andromeda galaxy in a bottle'
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

This will only utilize CPU, minimizing rendering time can be used with these options:

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

## Credits

Special Thank you to the following people/groups involved with helping me create this Docker container.

### Github Member: fboutnois
Thank you to fboutnois for the original implementation of this Docker container, and for being super accomadating to my questions and requests. Check out their [github](https://github.com/fboulnois) for more of their work.

### Furqanil Taqwa (Aka Linaqruf)
Thank you to Linaqruf for the creation of the diffuser model: Linaqruf/anything-v3-better-vae. Their work can be found [hugging face](https://huggingface.co/Linaqruf)

### Huggingface Community
Thank you to the Huggingface team for creating the AI community and Machine Learning platform [hugging face](https://huggingface.co/).

### Stability AI
THank you to Stability AI for open sourcing Stable Diffusion. Learn more about their work [stable ai](https://stability.ai/).