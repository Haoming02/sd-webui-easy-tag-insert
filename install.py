import launch

package = 'PyYAML'

if not launch.is_installed(package):
    launch.run_pip(f"install {package}", f"sd-webui-easy-tag-insert requirement: {package}")
