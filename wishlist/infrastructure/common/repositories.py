import abc
from typing import Dict, List

from wishlist import settings
from wishlist.infrastructure.common.databases import MongoDB


class BaseRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def create(self, model: Dict) -> str:
        pass  # pragma: no-cover

    @abc.abstractmethod
    async def update(self, model: Dict) -> bool:
        pass  # pragma: no-cover

    @abc.abstractmethod
    async def delete(self, query: Dict) -> int:
        pass  # pragma: no-cover

    @abc.abstractmethod
    async def find_one(self, query: Dict) -> Dict:
        pass  # pragma: no-cover

    @abc.abstractmethod
    async def find_all(
        self, query: Dict, page: int, size: int
    ) -> List[Dict]:
        pass  # pragma: no-cover

    @abc.abstractmethod
    async def count(self, query: Dict) -> int:
        pass  # pragma: no-cover

    @abc.abstractmethod
    async def find_all_and_count(
        self, query: Dict, page: int, size: int
    ) -> (Dict, List[Dict]):
        pass  # pragma: no-cover


class MongoRepository(BaseRepository):
    def __init__(self, collection: str):
        self._collection = MongoDB(
            uri=settings.MONGO_URI,
            db=settings.MONGO_DB
        ).get_collection(collection)

    async def create(self, model: Dict) -> str:
        result = await self._collection.insert_one(model)
        return str(result.inserted_id)

    async def update(self, id_: str, model: Dict) -> bool:
        result = await self._collection.update_one(
            {'id': id_},
            {'$set': model}
        )

        return result.modified_count > 0

    async def delete(self, id_: str) -> int:
        return await self._collection.delete_many({
            'id': id_
        })

    async def find_one(self, query: Dict) -> Dict:
        return await self._collection.find_one(query)

    async def find_all(
        self, query: Dict, page: int, size: int
    ) -> List[Dict]:
        cursor = self._collection.find(query)
        cursor.skip((page - 1) * size).limit(size)

        models = []
        async for item in cursor:
            models.append(item)

        return models

    async def count(self, query: Dict) -> int:
        return await self._collection.count_documents(query)

    async def find_all_and_count(
        self, query: Dict, page: int, size: int
    ) -> (Dict, List[Dict]):
        models = await self.find_all(query, page, size)
        count = await self.count(query)

        meta = {
            'count': count,
            'page': page,
            'size': size
        }

        return (meta, models)
