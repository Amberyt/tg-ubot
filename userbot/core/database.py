__all__ = ['get_collection']

import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient, AgnosticDatabase, AgnosticCollection

from userbot import logging, Config

_LOG = logging.getLogger(__name__)
_LOG_STR = "$$$>>> %s <<<$$$"

_LOG.info(_LOG_STR, "Connecting to Database...")

_MGCLIENT: AgnosticClient = AsyncIOMotorClient(Config.DB_URI)
_RUN = asyncio.get_event_loop().run_until_complete

if "Userbot" in _RUN(_MGCLIENT.list_database_names()):
    _LOG.info(_LOG_STR, "Userbot Database Found :) => Now Logging to it...")
else:
    _LOG.info(_LOG_STR, "Userbot Database Not Found :( => Creating New Database...")

_DATABASE: AgnosticDatabase = _MGCLIENT["Userbot"]
_COL_LIST = _RUN(_DATABASE.list_collection_names())


def get_collection(name: str) -> AgnosticCollection:
    """Create or Get Collection from your database"""
    if name in _COL_LIST:
        _LOG.debug(_LOG_STR, f"{name} Collection Found :) => Now Logging to it...")
    else:
        _LOG.debug(_LOG_STR, f"{name} Collection Not Found :( => Creating New Collection...")
    return _DATABASE[name]
