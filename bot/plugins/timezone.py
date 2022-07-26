from __future__ import annotations

from datetime import datetime

import crescent
import hikari
from crescent.ext import docstrings

import pytz
import rusty

plugin = crescent.Plugin()


def parse_time(s: str) -> int:
    """
    Parses a time possibly ending in `am` or `pm`, raising errors if necessary.
    """
    s = s.casefold().removesuffix("am").removesuffix("pm")
    if not s.isnumeric():
        raise TimezoneError(
            "Excepted a number for `time` or a number that ends with `pm` or `am`."
        )
    return int(s)


class TimezoneError(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


str_searcher = rusty.StringSearcher(pytz.all_timezones)


async def region_autocomplete(
    _: crescent.Context, option: hikari.AutocompleteInteractionOption
) -> list[hikari.CommandChoice]:
    if not option.value:
        return []
    return [
        hikari.CommandChoice(name=word, value=word)
        for word in str_searcher.fuzzy_search(str(option.value), 10)
    ]


def unwrap_date(date: str | None) -> tuple[int, int, int]:
    now = datetime.utcnow()

    if not date:
        return now.month, now.day, now.year

    def safe_to_int(s: str) -> int:
        try:
            return int(s)
        except ValueError:
            raise TimezoneError(
                "Expected a number for month, day, and optionally year of argument"
                "`date`."
            )

    date_strs = date.split("/")
    date_ints = list(map(safe_to_int, date_strs))

    if len(date_ints) == 2:
        month, day, year = *date_ints, now.year
    elif len(date_ints) == 3:
        month, day, year = date_ints

        if len(date_strs[2]) == 2:
            # user entered yy
            year += 2000

    else:
        raise TimeoutError("Expected either mm/dd or mm/dd/yyyy for argument `date`")

    if month < 1 or month > 12:
        raise TimezoneError("The specified month must be between 1 and 12.")
    if day < 1 or day > 31:
        raise TimezoneError("The specified day must be between 1 and 31.")
    if year < 0:
        raise TimezoneError("The specified year must be greater than or equal to 0.")

    return month, day, year


@plugin.include
@docstrings.parse_doc
@crescent.command(name="timestamp")
class Timezone:
    """
    Generates a dynamic timestamp.

    Args:
        date:
            The date in mm/dd/yyyy or mm/dd format.
        time:
            A human readable timestamp, such as "3:00pm" or in 24 hour time if you do
            not specify "am" or "pm".
        region:
            The identifier for the region you are in.
        format:
            The format to display the time in.
    """

    time = crescent.option(str)
    region = crescent.option(str, autocomplete=region_autocomplete)
    date = crescent.option(str, default=None)
    format = crescent.option(
        str,
        choices=[
            ("Short Time", "t"),
            ("Long Time", "T"),
            ("Short Date", "d"),
            ("Long Date", "D"),
            ("Short Date/Time", "f"),
            ("Long Date/Time", "F"),
            ("Relative Time", "R"),
        ],
        default="t",
    )

    async def callback(self, ctx: crescent.Context) -> None:

        month, day, year = unwrap_date(self.date)

        hours_offset: int
        if "pm" in self.time:
            hours_offset = 12
        else:
            hours_offset = 0

        time_in_day = list(map(parse_time, self.time.split(":")))

        if len(time_in_day) == 2:
            hours, minutes = time_in_day
        else:
            hours = time_in_day[0]
            minutes = 0

        if minutes < 0 or minutes > 60:
            raise TimezoneError("Minutes must be between 0 and 60.")
        if hours < 0 or hours > 23:
            raise TimezoneError("Hours must be between 0 and 23.")

        if hours == 12:
            hours_offset += 12

        hours = (hours + hours_offset) % 24

        time = datetime(
            year=year,
            month=month,
            day=day,
            hour=hours,
            minute=minutes,
        )

        try:
            adjusted_time = pytz.timezone(self.region).localize(time)
        except pytz.UnknownTimeZoneError:
            raise TimezoneError(f"`{self.region}` is not a valid region.")

        timestamp = f"<t:{str(int(adjusted_time.timestamp()))}:{self.format}>"

        await ctx.respond(
            "Use the unformatted timestamp in your message:\n"
            f"{timestamp} `{timestamp}`",
            ephemeral=True,
        )


@plugin.include
@crescent.catch_command(TimezoneError)
async def on_timezone_error(exc: TimezoneError, ctx: crescent.Context) -> None:
    await ctx.respond(exc.reason, ephemeral=True)
