# SD Webui Easy Tag Insert
This is an Extension for the [Automatic1111 Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), which helps inserting prompts and using LoRA/LyCORIS.

## How to Use
1. Click the green `🍀` button under **Generate** to open the panel
    - Hides **Extra Networks** panel automatically to avoid clutters
2. Select between category tabs
3. Click the button to insert the tag; Click the button again to remove the tag
    - Toggle `To Negative` to insert the tag to the Negative Prompt instead
4. Click `Refresh` to reload the modified tags without reloading the webui
    - **Note:** `Refresh` only works on adding, deleting or editing existing tags; For adding/deleting Categories, you still need to **Reload UI**
5. Works in both `txt2img` and `img2img`

## Use Cases
This Extension is especially useful along with LoRA or LyCORIS, as most of them require **trigger words** to function. 
Therefore you can add entries like:
```yml
Character:
  Mana: nagase mana, idol, <lora:mana:0.75>
  Kotono: nagase kotono, uniform, <lyco:kotono:0.75>
```
This way, you will only need to click 1 button to add the trigger words as well as the syntax.

You can also just use this as simple shortcuts for long prompts:
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

#### Note
- You can have multiple `.yml` *(or `.yaml`)* files in the `tags` folder
- An example file is provided
    - *The LoRA ones only work if you do have them*

## Special Thanks
This Extension is inspired by [Easy Prompt Selector](https://github.com/blue-pen5805/sdweb-easy-prompt-selector)~