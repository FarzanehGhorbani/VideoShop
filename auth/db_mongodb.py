from http import client
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

client=AsyncIOMotorClient('mongodb://root:example@192.168.63.26:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false')

# this make if another loop is running in the background use same loop for database operations
client.get_io_loop = asyncio.get_running_loop


db=client['Authentication']['auth']