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
> That's 2 `spaces` instead of a `tab` character, as specified by YAML

### Note
- The tabs appear in the order they were written in the files. So write your most-used Category first!
  - Since files are ordered alphabetically, you can add numbers in front to force a certain order instead.
- You can have multiple `.yml` *(or `.yaml`)* files in the `tags` folder for better organizations
  - You can also have the same Category in multiple files. For example:
    - `male.yml`:
        ```yml
        Arknights:
          Silverash: trigger, <lora>
        ```
    - `female.yml`:
        ```yml
        Arknights:
          Blaze: trigger, <lora>
        ```
    - They will still show up in the same tab
- Some placeholder sample files are provided
    - If no `tags` folder is present, it will automatically rename the `samples` folder to `tags`. This is to avoid overriding users' local files.

## Special Thanks
This Extension was inspired by [Easy Prompt Selector](https://github.com/blue-pen5805/sdweb-easy-prompt-selector)~