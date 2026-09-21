"""Hermes Python plugin: a user-invoked asset installer, not a theme hook."""
from .installer import configure_parser, run


def register(ctx):
    ctx.register_cli_command(
        name="tokyo-night",
        help="Install or remove the Tokyo Night native skin",
        setup_fn=configure_parser,
        handler_fn=run,
    )
