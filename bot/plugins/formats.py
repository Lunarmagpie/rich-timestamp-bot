import crescent
import hikari
from crescent.ext import docstrings

from bot.util import TIME_FORMATS

plugin = crescent.Plugin()

resp_embed = hikari.Embed()


format_examples = "\n".join(
    f"`{name.ljust(15, ' ')}`\t<t:1658851200:{letter}>" for name, letter in TIME_FORMATS
)
resp_embed.add_field("Formats", value=format_examples)


@plugin.include
@docstrings.parse_doc
@crescent.command
async def formats(ctx: crescent.Context) -> None:
    await ctx.respond(format_examples)
