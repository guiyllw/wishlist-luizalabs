from motor.motor_asyncio import AsyncIOMotorClient

from wishlist.infrastructure.common.metaclasses import SingletonMeta


class MongoDB(metaclass=SingletonMeta):

    def __init__(self, uri: str, db: str):
        self._client = None
        self._db = db
        self.connect(uri)

    def connect(self, uri: str):
        if not self._client:
            self._client = AsyncIOMotorClient(uri)

    def close(self):
        if self._client:
            self._client.close()
            self._client = None

    def get_collection(self, name: str):
        return self._client[self._db][name]
