import gradio as gr
from modules import cmd_args, hpc, capture, translator

args = cmd_args.parser.parse_args()

def create_ui() :
    with gr.Blocks() as demo:
        gr.Markdown("# SDXL-Turbo from Camera Image by KCCT D4")
        with gr.Row(equal_height=True):
            with gr.Column(scale=3):
                prompt = gr.Textbox(lines=2, label="Prompt")
                negative_prompt = gr.Textbox(lines=2, label="Negative Prompt")
                dummy_prompt = gr.Textbox(visible=False)
                dummy_negative_prompt = gr.Textbox(visible=False)
            with gr.Column():
                start_button = gr.Button(value='Start', variant="primary", visible=True)
                stop_button = gr.Button(value='Stop', variant="secondary", visible=False)
                language = gr.Dropdown(label='Language',
                                       choices=["日本語", "English(Original)"], 
                                       value="日本語")

        with gr.Accordion(label="Configuration", open=False):
            with gr.Row():
                with gr.Column(scale=1):
                    checkpoint_name = gr.Dropdown(label='Checkpoint', 
                                                  choices=["stabilityai/sdxl-turbo", "Lykon/AAM_XL_AnimeMix_Turbo"], 
                                                  value="stabilityai/sdxl-turbo", 
                                                  visible=False)
                    gr.Markdown("# <u>**!!!! 必ず steps * strength >= 1.0 にしてください !!!!**</u>")
                    
                    steps = gr.Slider(minimum=1, maximum=20, step=1, label="Steps", value=2)
                    strength = gr.Slider(minimum=0.0, maximum=1.0, step=0.05, label="Strength", value=0.5)
                    cfg_scale = gr.Slider(minimum=0.0, maximum=15.0, step=0.5, label="CFG Scale", value=0.0)
                    screen = gr.Checkbox(value=False, label="Switch to ScreenCap?")
                    width = gr.Slider(minimum=0, maximum=2048, step=16, label="Resize Width", value=640)
                    height = gr.Slider(minimum=0, maximum=2048, step=16, label="Resize Height", value=480)

                with gr.Column(scale=2):
                    gr.Markdown("## Input Image")
                    input_image = gr.Image(label="Input Image", interactive=False, show_label=False)
                    dummy_input = gr.Image(visible=False)
                    dummy_output = gr.Gallery(visible=False)

        prompt.change(fn=translate_prompt,
                      inputs=[prompt, language], 
                      outputs=[dummy_prompt])
        
        negative_prompt.change(fn=translate_prompt,
                      inputs=[negative_prompt, language], 
                      outputs=[dummy_negative_prompt])

        start_button.click(fn=start_click,
                           inputs=[screen, width, height, 
                                   checkpoint_name, dummy_prompt, dummy_negative_prompt, dummy_input, steps, strength, cfg_scale],
                           outputs=[dummy_input, dummy_output, 
                                    stop_button, start_button])
        
        stop_button.click(fn=switch_button,
                          outputs=[start_button, stop_button])
        
        dummy_input.change(fn=dummy_to_image,
                            inputs=[dummy_input],
                            outputs=[input_image])

        dummy_output.change(fn=generate,
                            inputs=[screen, width, height, 
                                    checkpoint_name, dummy_prompt, dummy_negative_prompt, dummy_input, steps, strength, cfg_scale],
                            outputs=[dummy_input, dummy_output])

    return demo

def translate_prompt(prompt, language):
    if language == "日本語":
        prompt = translator.jap_to_eng(prompt)
    return prompt
    

def start_click(screen, width, height, checkpoint_name, prompt, negative_prompt, dummy_input, steps, strength, cfg_scale):
    stop, start = switch_button()
    input, output = generate(screen, width, height, checkpoint_name, prompt, negative_prompt, dummy_input, steps, strength, cfg_scale)
    return input, output, stop, start

def switch_button():
    global now_generate
    now_generate = not now_generate
    return gr.Button(visible=True), gr.Button(visible=False)

def dummy_to_image(image):
    return image

def generate(screen, width, height, checkpoint, prompt, negative_prompt, input_image,  steps, strength, cfg_scale):
    if now_generate:
        input_image = capture.capture_image(screen, width, height)
        output_image = hpc.i2i(checkpoint, prompt, negative_prompt, input_image, steps, strength, cfg_scale)
        return input_image, output_image
    
    else:
        return input_image, None

def start() :
    global now_generate
    now_generate = False
    # i2i.create_pipe("stabilityai/sdxl-turbo")
    create_ui().launch(share=args.share, inbrowser=args.autolaunch)
