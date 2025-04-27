import motor.motor_asyncio
from app.config import Config

client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGODB_URL)
