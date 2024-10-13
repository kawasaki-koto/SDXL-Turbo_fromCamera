from diffusers import AutoPipelineForImage2Image, EulerAncestralDiscreteScheduler
from diffusers.utils import load_image
import torch

def create_pipe(name):
    global pipe, pipe_name
    pipe_name = name
    pipe = AutoPipelineForImage2Image.from_pretrained(name, torch_dtype=torch.float16, variant="fp16")
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    pipe.to("cuda")

def create_image(checkpoint, prompt, negative_prompt, init_image, steps, strength, guidance_scale):
    if not pipe_name == checkpoint:
        create_pipe(checkpoint)
    output_image = pipe(prompt, negative_prompt=negative_prompt, image=init_image, num_inference_steps=steps, strength=strength, guidance_scale=guidance_scale).images[0]
    return [output_image]
    # Galleyにはlistで返さないと行けないので
