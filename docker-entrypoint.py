#!/usr/bin/env python
import argparse, datetime, inspect, os
import numpy as np
import torch
from PIL import Image
from diffusers import (
    StableDiffusionPipeline,
    schedulers,
)


def iso_date_time():
    return datetime.datetime.now().isoformat()


def load_image(path):
    image = Image.open(os.path.join("input", path)).convert("RGB")
    print(f"loaded image from {path}:", iso_date_time(), flush=True)
    return image


def remove_unused_args(p):
    params = inspect.signature(p.pipeline).parameters.keys()
    args = {
        "prompt": p.prompt,
        "negative_prompt": p.negative_prompt,
        "height": p.H,
        "width": p.W,
        "num_images_per_prompt": p.n_samples,
        "num_inference_steps": p.ddim_steps,
        "guidance_scale": p.scale,
        "generator": p.generator,
    }
    return {p: args[p] for p in params if p in args}


def stable_diffusion_pipeline(p):
    p.dtype = torch.float16 if p.half else torch.float32
    p.diffuser = StableDiffusionPipeline
    p.revision = "fp16" if p.half else "main"

    if p.token is None:
        with open("token.txt") as f:
            p.token = f.read().replace("\n", "")

    if p.seed == 0:
        p.seed = torch.random.seed()

    p.generator = torch.Generator(device=p.device).manual_seed(p.seed)

    print("load pipeline start:", iso_date_time(), flush=True)

    pipeline = p.diffuser.from_pretrained(
        p.model,
        torch_dtype=p.dtype,
        revision=p.revision,
        use_auth_token=p.token,
    ).to(p.device)

    if p.scheduler is not None:
        scheduler = getattr(schedulers, p.scheduler)
        pipeline.scheduler = scheduler.from_config(pipeline.scheduler.config)

    if p.skip:
        pipeline.safety_checker = None

    if p.attention_slicing:
        pipeline.enable_attention_slicing()

    p.pipeline = pipeline

    print("loaded models after:", iso_date_time(), flush=True)

    return p


def stable_diffusion_inference(p):
    prefix = p.prompt.replace(" ", "_")[:170]
    for j in range(p.n_iter):
        result = p.pipeline(**remove_unused_args(p))

        for i, img in enumerate(result.images):
            idx = j * p.n_samples + i + 1
            out = f"{prefix}__steps_{p.ddim_steps}__scale_{p.scale:.2f}__seed_{p.seed}__n_{idx}.png"
            img.save(os.path.join("output", out))

    print("completed pipeline:", iso_date_time(), flush=True)


def main():
    parser = argparse.ArgumentParser(description="Create images from a text prompt.")
    parser.add_argument(
        "prompt0",
        metavar="PROMPT",
        type=str,
        nargs="?",
        help="The prompt to render into an image",
    )
    parser.add_argument(
        "--prompt", type=str, nargs="?", help="The prompt to render into an image"
    )
    parser.add_argument(
        "--n_samples",
        type=int,
        nargs="?",
        default=1,
        help="Number of images to create per run",
    )
    parser.add_argument(
        "--n_iter",
        type=int,
        nargs="?",
        default=1,
        help="Number of times to run pipeline",
    )
    parser.add_argument(
        "--H", type=int, nargs="?", default=512, help="Image height in pixels"
    )
    parser.add_argument(
        "--W", type=int, nargs="?", default=512, help="Image width in pixels"
    )
    parser.add_argument(
        "--scale",
        type=float,
        nargs="?",
        default=11,
        help="Classifier free guidance scale",
    )
    parser.add_argument(
        "--seed", type=int, nargs="?", default=0, help="RNG seed for repeatability"
    )
    parser.add_argument(
        "--ddim_steps", type=int, nargs="?", default=20, help="Number of sampling steps"
    )
    parser.add_argument(
        "--attention-slicing",
        type=bool,
        nargs="?",
        const=True,
        default=False,
        help="Use less memory at the expense of inference speed",
    )
    parser.add_argument(
        "--device",
        type=str,
        nargs="?",
        default="cpu",
        help="The cpu or cuda device to use to render images",
    )
    parser.add_argument(
        "--half",
        type=bool,
        nargs="?",
        const=True,
        default=False,
        help="Use float16 (half-sized) tensors instead of float32",
    )
    parser.add_argument(
        "--model",
        type=str,
        nargs="?",
        default="Linaqruf/anything-v3-better-vae", # "CompVis/stable-diffusion-v1-4", "andite/anything-v4.0", "Linaqruf/anything-v3-better-vae",
        help="The model used to render images",
    )
    parser.add_argument(
        "--negative-prompt",
        type=str,
        nargs="?",
        help="The prompt to not render into an image",
    )
    parser.add_argument(
        "--scheduler",
        type=str,
        nargs="?",
        default="DPMSolverSinglestepScheduler",
        help="Override the scheduler used to denoise the image",
    )
    parser.add_argument(
        "--skip",
        type=bool,
        nargs="?",
        const=True,
        default=False,
        help="Skip the safety checker",
    )
    parser.add_argument(
        "--token", type=str, nargs="?", help="Huggingface user access token"
    )


    args = parser.parse_args()

    if args.prompt0 is not None:
        args.prompt = args.prompt0

    pipeline = stable_diffusion_pipeline(args)
    stable_diffusion_inference(pipeline)


if __name__ == "__main__":
    main()
