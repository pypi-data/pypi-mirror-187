import logging
from pkgutil import iter_modules

from aiohttp import ClientSession
from discord.ext import commands
from discord.utils import MISSING

__all__ = ["Bot"]
LOGGER = logging.getLogger(__name__)


class Bot(commands.Bot):
    """A subclass of `commands.Bot` which has stuff like

    a pre-populated session attribute
    a `load_extensions` method which will either load all extensions in a given folder, or from a list of them"""

    session: ClientSession

    async def start(
        self, token: str, *, reconnect: bool = True, **aiohttp_session_kwargs
    ) -> None:
        async with ClientSession(**aiohttp_session_kwargs) as session:
            self.session = session
            await super().start(token, reconnect=reconnect)

    async def load_extensions(
        self, *, extensions: list[str] = MISSING, folder: str = MISSING
    ):
        """|coro|

        Loads all of your extensions for you.

        Parameters
        -----------
        extensions : Optional[list[str]]
            a list of extensions to be loaded
        folder : Optional[str]
            the folder your extensions reside in

        Raises
        -----------
        ValueError
            both extensions and folder has been filled or neither have been filled
        """

        if extensions is MISSING and folder is MISSING:
            raise ValueError(
                "You must either provide a list of extensions `extentions kwarg`, or a folder name which contains your extensions `folder` kwarg"
            )
        elif extensions is not MISSING and folder is not MISSING:
            raise ValueError("Both folder and extensions given.")

        if folder:
            extensions = [m.name for m in iter_modules([folder], prefix="cogs.")]

        if extensions:
            for ext in extensions:
                try:
                    await self.load_extension(ext)
                except Exception as e:
                    LOGGER.error("Failed to load extension %s", exc_info=e)
