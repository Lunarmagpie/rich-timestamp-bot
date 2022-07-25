import crescent

from bot import config


class Bot(crescent.Bot):
    def __init__(self) -> None:
        super().__init__(token=config.CONFIG.token)

        self.plugins.load_folder("bot.plugins")


def run() -> None:
    Bot().run()
