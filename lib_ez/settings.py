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
