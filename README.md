# SD Webui Easy Tag Insert
This is an Extension for the [Automatic1111 Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), which trivialize inserting prompts.

### Note
This Extension has been rewritten for the new `v1.6` UIs. For Webui version **`v1.5`** or older, please download the one from the **Release** page. 

### Use Cases
This Extension is useful along with LoRA, especially those that contain multiple **trigger words** for different concepts.
```yml
Character:
  Chara1: chara1, tags1, <lora:franchise:0.75>
  Chara2: chara2, tags2, <lora:franchise:0.75>
```
This way, you will only need to click 1 button to add the trigger words as well as the syntax.

You can also just use this Extension as a way to simply make shortcuts for long prompts:
```yml
Starting Prompts:
  Positive: (high quality, best quality)
  Negative: (low quality, worst quality:1.2)
```

## How to Add Entry
The tags are loaded from the `.yml` files inside the `tags` folder. To add your own entry, write in the following format:
```yml
Category:
  Display Name: Actual Prompts
```

- If no `tags` folder is present *(**eg.** fresh install)*, it will automatically rename the `samples` folder to `tags`. This is to avoid overriding users' local files.
- An example file is provided

### Note
- The `Show dirs` toggle displays the Categories for filtering
- You can have multiple `.yml` *(or `.yaml`)* files in the `tags` folder for better organizations
- You can also have the same Category in multiple files
- You can live reload the entries by pressing `Refresh`, without restarting the UI
