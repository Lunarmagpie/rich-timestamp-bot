import crescent
import hikari

from bot.config import CONFIG

plugin = crescent.Plugin()


@plugin.include
@crescent.command
async def info(ctx: crescent.Context) -> None:
    """
    View the info for this discord bot.
    """
    embed = (
        hikari.Embed(title="The Time")
        .add_field("Source code", "https://github.com/Lunarmagpie/rich-timestamp-bot")
        .add_field("Author", "<@318076068290494466>")
        .add_field(
            "Invite this bot to your server",
            f"[Click here]({CONFIG.invite_link})",
        )
    )

    await ctx.respond(embed=embed)
