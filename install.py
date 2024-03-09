import launch

try:
    import yaml
except ModuleNotFoundError:
    launch.run_pip(f"install PyYAML", f"sd-webui-easy-tag-insert requirement: PyYAML")
