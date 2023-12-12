# SD Webui Easy Tag Insert
This is an Extension for the [Automatic1111 Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), which trivializes inserting prompts.

**Note:** This Extension has been rewritten for the new `v1.6.0` UIs. For Webui `v1.5` or older, please download the one from the **Release** page. 

<p align="center">
<img src="sample.jpg"><br>
<i>(<a href="https://github.com/catppuccin/stable-diffusion-webui">Catppuccin Theme</a>)</i>
</p>

## How to Use 
This Extension creates buttons in a new `Extra Networks` tab, **EZ Tags**. 
When clicked, it will add the specified prompts into either the Positive or Negative field.

## Use Cases
You can use this Extension to simply make shortcuts for very long prompts:
```yml
Starting Prompts:
  Positive: (high quality, best quality)
  Negative: (low quality, worst quality:1.2)
```

This is really useful with LoRAs, especially for those that contain multiple concepts with different **trigger words**.
```yml
Character:
  Chara1: triggers1, <lora:franchise:0.75>
  Chara2: triggers2, <lora:franchise:0.75>
```

## How to Add Entries
The tags are loaded from the `.yml` files inside the `tags` folder. To add your own entry, write in the following format:
```yml
Category:
  Display Name: Actual Prompts
```

> Those are `2 spaces` at the beginning of each entry, as specified by YAML

## Note
- If no `tags` folder is present *(**eg.** fresh install)*, it will automatically clone the `samples` folder to `tags`. This is to avoid overriding users' local files.
- An example `.yml` file is also provided
- The `Show dirs` toggle displays the Categories for filtering
- You can have multiple `.yml` *(or `.yaml`)* files in the `tags` folder for better organizations
- You can also have the same Category in multiple files
- You can live reload the entries by pressing `Refresh` without restarting the UI
- Due to how the Webui is coded, the buttons are sorted like **Date Created** on launch

## Sorting
- **Default Sort:** First by `Category`, then by `Display Name`
- **Date Created:** By `Index` *(the order they are written in the YAML)*
- **Date Modified:** First by `Category`, then by `Index`
- **Name:** By `Display Name`
