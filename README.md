# Stable Diffusion Docker Container (CPU Only)

This Docker container is a text-to-image (txt2img) generation tool that leverages Stable Diffusion with a packaged diffusion model. Stable Diffusion is a deep learning, latent txt2img diffusion model capable of generating photo-realistic images given any text input, for more information visit this wikipedia page: [Stable Diffusion](https://en.wikipedia.org/wiki/Stable_Diffusion). The diffusion model that was packaged in this docker container can be found here: [Diffuser Model](https://huggingface.co/Linaqruf/anything-v3-better-vae).

## Example Image Output

The following prompt was used to render the three images below, feel free to test this out yourself (Careful may generate NSFW, "not safe for work", imagery, use at your own discretion)

```sh
./build.sh run --device cpu --skip --prompt "1girl, green hair, long hair, yellow eyes, warrior armor, warrior princess, tanned-black skin, battle field, shadows, lens flare, masterpiece" --negative-prompt "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name"
```

<p float="left">
  <img src="img/1girl,_green_hair,_long_hair,_yellow_eyes,_warrior_armor,_warrior_princess,_tanned-black_skin,_battle_field,_shadows,_lens_flare,_masterpiece__steps_20__scale_11.00__seed_9746260096546669498__n_1.png" alt="Green-Haired Warrior Princess" width="256" height="256">
  <img src="img/1girl,_green_hair,_long_hair,_yellow_eyes,_warrior_armor,_warrior_princess,_tanned-black_skin,_battle_field,_shadows,_lens_flare,_masterpiece__steps_20__scale_11.00__seed_2951297131937974408__n_1.png" alt="Green-Haired Warrior Princess" width="256" height="256">
  <img src="img/1girl,_green_hair,_long_hair,_yellow_eyes,_warrior_armor,_warrior_princess,_tanned-black_skin,_battle_field,_shadows,_lens_flare,_masterpiece__steps_20__scale_11.00__seed_9764299217508183519__n_1.png" alt="Green-Haired Warrior Princess" width="256" height="256">
</p>

## Disclaimer

By default, this pipeline will render images that may be NSFW (Not safe for work). The reason with why this will occur is that it utilizes the ```--skip``` feature set as this allows for the time with which it takes to render an image to be quicker. As such, if you use this tool for safe for work applications (SFW), do not include ```--skip```. Use at your own discretion.

## Requirements

By default, this pipeline will render images using only the CPU as rendering on a GPU is extremely cost prohibitive. As a result of this, it will take a few minutes to create one image (Roughly 4 minutes and 50 seconds on a Ryzen 5 5600x CPU, your mileage may vary). Make sure to only use `--device cpu`

## Quickstart

The pipeline is managed using a single [`build.sh`](build.sh) script.

### Work in progress:

Pull Functionality using `./build.sh pull`. This functionality will allow you to pull the latest image once it is available. Currently, follow the build section to initialize Dockerfile.

## Build

To build:

```sh
./build.sh build
```

### Work in progress 

Work in progress: Make sure your [user access token](#huggingface-token) is saved in a file called `token.txt`. As far as I am aware, you don't need to pass through a huggingface token current;y, however open a github issue if an error occurs.

## Testing

To run a test:

```sh
./build.sh test
```

This will render a single 512x512 (height and width) image similar to the three images found at the start of this README.md

## Run

### Text-to-Image (`txt2img`)

To run:

```sh
./build.sh run --device cpu --prompt 'warrior princess'
```

### Options

Some of the options from [`txt2img.py`](https://github.com/CompVis/stable-diffusion/blob/main/scripts/txt2img.py) are implemented for compatibility:

* `--prompt [PROMPT]`: the prompt to render into an image
* `--negative-prompt [NEGATIVE_PROMPT]`: the prompt to not render into an image
(default `None`)
* `--n_samples [N_SAMPLES]`: number of images to create per run (default 1)
* `--n_iter [N_ITER]`: number of times to run pipeline (default 1)
* `--H [H]`: image height in pixels (default 512, must be divisible by 64)
* `--W [W]`: image width in pixels (default 512, must be divisible by 64)
* `--scale [SCALE]`: Classifier Guidance Scale (CGS) (default 11)
* `--seed [SEED]`: RNG seed for repeatability (default is a random seed)
* `--ddim_steps [DDIM_STEPS]`: number of sampling steps (default 20)
* `--skip`: skip safety checker (default is the safety checker is on)

## Examples

These commands are both identical:

```sh
./build.sh run --device cpu 'warrior princess'
./build.sh run --device cpu --prompt 'warrior princess'
```

Set the seed to 255 (Allows rendering of image with constant output):

```sh
./build.sh run --device cpu --seed 255 --prompt 'warrior princess'
```

Options can be combined:

```sh
./build.sh run --device cpu --skip --scale 11.0 --seed 255 --prompt 'warrior princess'
```

## Minimize Time Rendering

Minimize rendering time with these options (some options are in experimental):

* Make images smaller than 512x512 using `--W` and `--H` to decrease memory use and increase image creation speed
* Use `--half` to decrease memory use but slightly decrease image quality
* Use `--attention-slicing` to decrease memory use but also decrease image creation speed
* Decrease the number of samples and increase the number of iterations with `--n_samples` and `--n_iter` to decrease overall memory use
* Skip the safety checker with `--skip` to run less code (Work in progress: Implementation by default)

```sh
./build.sh run --device cpu --skip \
  --W 256 --H 256 --half --attention-slicing \
  --n_samples 1 --n_iter 1 --prompt 'warrior princess'
```

## Experimental Options

Options you can play around with (May not work):

* `--attention-slicing`: use less memory at the expense of inference speed (default is no attention slicing)
* `--device [DEVICE]`: the cpu or cuda device to use to render images (default is unfortunatly `gpu`, will try and fix later)
* `--half`: use float16 tensors instead of float32 (default `float32`)
* `--model [MODEL]`: the model used to render images (default is `Linaqruf/anything-v3-better-vae`)
* `--scheduler [SCHEDULER]`: override the scheduler used to denoise the image (default `DPMSolverSinglestepScheduler`)
* `--token [TOKEN]`: specify a Huggingface user access token at the command line instead of reading it from a file (default is a file)

On Windows, if you aren't using WSL2 and instead use MSYS, MinGW, or Git Bash,
prefix your commands with `MSYS_NO_PATHCONV=1` (or export it beforehand):

```sh
MSYS_NO_PATHCONV=1 ./build.sh run --device cpu --half --prompt 'warrior princess'
```

## Outputs

### Images

The images are saved as PNGs in the `output` folder using the prompt text. The
`build.sh` script creates and mounts this folder as a volume in the container.

## Credits

Special Thanks to the following people and communities involved with helping me create this Docker container.

### Github Member: fboutnois
Thank you to fboutnois for the original implementation of this Docker container, and for being super accommodating to my questions and requests. Check out their [github](https://github.com/fboulnois) profile for more of their work.

### Furqanil Taqwa (Aka Linaqruf)
Thank you to Linaqruf for the creation of the diffuser model: Linaqruf/anything-v3-better-vae. Their work can be found at: [Linaqruf Hugging Face Profile](https://huggingface.co/Linaqruf)

### Huggingface Community
Thank you to the Huggingface team for creating the AI community and Machine Learning platform, community found at: [Hugging Face Community Landing Page](https://huggingface.co/).

### Stability AI
Thank you to Stability AI for open sourcing Stable Diffusion. Learn more about their work at: [Stability AI Landing Page](https://stability.ai/).