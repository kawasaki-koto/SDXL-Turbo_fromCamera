import requests, io
from PIL import Image

def i2i(checkpoint, prompt, negative_prompt, init_image, steps, strength, guidance_scale):
    data = {
        'checkpoint': checkpoint,
        'prompt': prompt,
        'negative_prompt': negative_prompt,
        'steps': steps,
        'strength': strength,
        'guidance_scale': guidance_scale,
        }

    img_io = io.BytesIO()
    init_image.save(img_io, 'JPEG')
    img_io.seek(0)
    files = {'init_image': ('init_image.jpg', img_io, 'image/jpg')}

    url = 'http://10.30.128.245:82/'
    response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        img_data = io.BytesIO(response.content)
        output_image = Image.open(img_data)
        output_image.save('./output.jpg')
        return [output_image]
    else:
        print("Error:", response.status_code)
