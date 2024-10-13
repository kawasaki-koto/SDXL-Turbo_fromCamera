import gradio as gr
from modules import cmd_args, i2i, capture

args = cmd_args.parser.parse_args()

def create_ui() :
    with gr.Blocks() as demo:
        gr.Markdown("# SDXL-Turbo from Camera Image by KCCT D4")
        with gr.Row(equal_height=True):
            with gr.Column(scale=3):
                prompt = gr.Textbox(lines=2, label="Prompt")
                negative_prompt = gr.Textbox(lines=2, label="Negative Prompt")
            with gr.Column():
                start_button = gr.Button(value='Start', variant="primary", visible=True)
                stop_button = gr.Button(value='Stop', variant="secondary", visible=False)
                now_generate = gr.Checkbox(value=False, visible=False)

        with gr.Accordion(label="Configuration", open=False):
            with gr.Row():
                with gr.Column(scale=1):
                    checkpoint_name = gr.Dropdown(label='Checkpoint', 
                                                  choices=["stabilityai/sdxl-turbo", "Lykon/AAM_XL_AnimeMix_Turbo"], 
                                                  value="stabilityai/sdxl-turbo")
                    gr.Markdown("# <u>**!!!! steps * strength >= 1.0. This is must !!!!**</u>")
                    
                    steps = gr.Slider(minimum=1, maximum=20, step=1, label="Steps", value=2)
                    strength = gr.Slider(minimum=0.0, maximum=1.0, step=0.05, label="Strength", value=0.5)
                    cfg_scale = gr.Slider(minimum=0.0, maximum=15.0, step=0.5, label="CFG Scale", value=0.0)
                    screen = gr.Checkbox(value=True, label="Switch to ScreenCap?")
                    width = gr.Slider(minimum=0, maximum=2048, step=16, label="Resize Width", value=768)
                    height = gr.Slider(minimum=0, maximum=2048, step=16, label="Resize Height", value=432)

                with gr.Column(scale=2):
                    gr.Markdown("## Input Image")
                    input_image = gr.Image(label="Input Image", interactive=False, show_label=False)
                    dummy_input = gr.Image(visible=False)

        with gr.Column():
            gr.Markdown("## Output Image")
            output_image = gr.Gallery(label="Output Image", show_label=False)
            dummy_output = gr.Gallery(visible=False)

        start_button.click(fn=start_generate,
                           inputs=[screen, width, height, 
                                   checkpoint_name, prompt, negative_prompt, steps, strength, cfg_scale],
                           outputs=[dummy_input, dummy_output, 
                                    start_button, stop_button, now_generate])
        
        stop_button.click(fn=stop_generate,
                          outputs=[start_button, stop_button, now_generate])
        
        dummy_output.change(fn=dummy_to_image,
                            inputs=[dummy_output],
                            outputs=[output_image])
        
        dummy_input.change(fn=dummy_to_image,
                            inputs=[dummy_input],
                            outputs=[input_image])

        output_image.change(fn=generate,
                            inputs=[now_generate, screen, width, height, 
                                    checkpoint_name, prompt, negative_prompt, dummy_input, steps, strength, cfg_scale],
                            outputs=[dummy_input, dummy_output])

    return demo

def start_generate(screen, width, height, checkpoint, prompt, negative_prompt, steps, strength, cfg_scale):
    input_image = capture.capture_image(screen, width, height)
    output_image = i2i.create_image(checkpoint, prompt, negative_prompt, input_image, steps, strength, cfg_scale)
    return input_image, output_image, gr.Button(visible=False), gr.Button(visible=True), True

def stop_generate():
    global now_generate
    now_generate = False
    return gr.Button(visible=True), gr.Button(visible=False), False

def dummy_to_image(image):
    return image

def generate(now_generate, screen, width, height, checkpoint, prompt, negative_prompt, input_image,  steps, strength, cfg_scale):
    if now_generate:
        input_image = capture.capture_image(screen, width, height)
        output_image = i2i.create_image(checkpoint, prompt, negative_prompt, input_image, steps, strength, cfg_scale)
        return input_image, output_image
    else:
        return input_image, None

def start() :
    i2i.create_pipe("stabilityai/sdxl-turbo")
    create_ui().launch(share=args.share, inbrowser=args.autolaunch)
