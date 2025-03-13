from modules.shared import OptionInfo, opts


def on_ez_settings():
    opts.add_option(
        "ez_use_category",
        OptionInfo(
            True,
            "Group the Cards based on Categories",
            section=("ez", "EZ Tags"),
            category_id="ui",
        ).needs_reload_ui(),
    )
    opts.add_option(
        "ez_use_style",
        OptionInfo(
            False,
            "Use custom style",
            section=("ez", "EZ Tags"),
            category_id="ui",
        )
        .info("smaller cards with gradient styles")
        .info("<b>note:</b> this will disable preview images and metadata buttons")
        .needs_reload_ui(),
    )
