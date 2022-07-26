import crescent
from crescent.ext import docstrings

from bot.util import TIME_FORMATS

plugin = crescent.Plugin()

FORMAT_EXAMPLES = "\n".join(
    f"`{name.ljust(15, ' ')}`\t<t:1658851200:{letter}>" for name, letter in TIME_FORMATS
)


@plugin.include
@docstrings.parse_doc
@crescent.command
async def formats(ctx: crescent.Context) -> None:
    await ctx.respond(FORMAT_EXAMPLES)
