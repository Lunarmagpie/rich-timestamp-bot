import crescent
import hikari
from crescent.ext import docstrings

from bot.config import CONFIG

plugin = crescent.Plugin()


EMBED = (
    hikari.Embed(title="The Time")
    .add_field("Source code", "https://github.com/Lunarmagpie/rich-timestamp-bot")
    .add_field("Author", "<@318076068290494466>")
    .add_field(
        "Invite this bot to your server",
        f"[Click here]({CONFIG.invite_link})",
    )
)


@plugin.include
@docstrings.parse_doc
@crescent.command
async def info(ctx: crescent.Context) -> None:
    """
    View the info for this discord bot.
    """

    await ctx.respond(embed=EMBED)
