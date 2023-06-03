import modules.scripts as scripts
import gradio as gr

from yaml_loader import reload_yaml

class EasyTags(scripts.Script):

    def title(self):
        return "Easy Tag Insert"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        global DUMMY
        DUMMY = gr.Textbox(interactive=False, visible=False, elem_id = 'ez-tag-textbox') if not is_img2img else DUMMY

        COLLECTION = reload_yaml()

        if not is_img2img:
            enable_btn = gr.Button('🍀', elem_id = 'ez-tag-toggle-txt', full_width = False)

            with gr.Box(elem_id = 'ez-tag-container-txt'):
                for key in COLLECTION.keys():
                    if COLLECTION[key] == None:
                        print('\n\n[Easy Tag Insert]: Category ' + key + ' is Empty!\n\n')
                        continue

                    with gr.Tab(key, elem_id = 'tab-' + key.replace(' ', '-').lower() + '-txt'):
                        tags = COLLECTION[key]

                        with gr.Row():
                            for key, value in tags.items():
                                if value == None:
                                    print('\n\n[Easy Tag Insert]: Button ' + key + ' is Empty!\n\n')
                                    continue

                                button = gr.Button(key, elem_id = value)
                                button.style(size = 'sm', full_width = False)

                with gr.Row():
                    refresh_btn = gr.Button('Refresh', elem_id = 'ez-tag-refresh-txt')
                    refresh_btn.click(fn=reload_yaml, outputs=DUMMY)
                    refresh_btn.style(full_width = False)

                    to_negative = gr.Checkbox(label = ' To Negative ', elem_id = 'ez-tag-negative-txt')

        else:
            enable_btn = gr.Button('🍀', elem_id = 'ez-tag-toggle-img', full_width = False)

            with gr.Box(elem_id = 'ez-tag-container-img'):
                for key in COLLECTION.keys():
                    if COLLECTION[key] == None:
                        continue

                    with gr.Tab(key, elem_id = 'tab-' + key.replace(' ', '-').lower() + '-img'):
                        tags = COLLECTION[key]

                        with gr.Row():
                            for key, value in tags.items():
                                if value == None:
                                    continue

                                button = gr.Button(key, elem_id = value)
                                button.style(size = 'sm', full_width = False)

                with gr.Row():
                    refresh_btn = gr.Button('Refresh', elem_id = 'ez-tag-refresh-img')
                    refresh_btn.click(fn=reload_yaml, outputs=DUMMY)
                    refresh_btn.style(full_width = False)

                    to_negative = gr.Checkbox(label = ' To Negative ', elem_id = 'ez-tag-negative-img')

        return None