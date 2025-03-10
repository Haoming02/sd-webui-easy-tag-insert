import gradio as gr

is_gradio_4: bool = str(gr.__version__).startswith("4")


def js(func: str) -> dict:
    return {("js" if is_gradio_4 else "_js"): func}
