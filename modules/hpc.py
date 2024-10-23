import requests

def i2i(checkpoint, prompt, negative_prompt, init_image, steps, strength, guidance_scale):
    data = {
        'checkpoint': checkpoint,
        'prompt': prompt,
        'negative_prompt': negative_prompt,
        'steps': steps,
        'strength': strength,
        'guidance_scale': guidance_scale,
        }

    files = {'init_image': init_image}

    url = 'http://localhost:5000/'
    response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        return [response.content]
    else:
        print("Error:", response.status_code)
