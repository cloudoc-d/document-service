from redis import Redis
from pydantic import BaseModel
import json


class LockRecord(BaseModel):
    locked: bool
    owner_id: str | None


class AlreadyLockedException(Exception): ...
class UnauthorizedReleaseException(Exception): ...

class LockManager:
    def __init__(
        self,
        resource_namespace: str,
        redis_client: Redis,
    ) -> None:
        self._redis_client = redis_client
        self._storage_key = f"locks:{resource_namespace}"

    async def lock(
        self,
        resource_id: str,
        user_id: str,
    ) -> None:
        lock = await self._get_lock(resource_id)
        if lock.locked:
            raise AlreadyLockedException()

        await self._update_lock(
            resource_id=resource_id,
            lock=LockRecord(
                locked=True,
                owner_id=user_id
            )
        )

    async def release(
        self,
        resource_id: str,
        user_id: str,
    ) -> None:
        lock = await self._get_lock(resource_id)
        if lock.locked and lock.owner_id != user_id:
            raise UnauthorizedReleaseException()

        await self._update_lock(
            resource_id=resource_id,
            lock=LockRecord(
                locked=False,
                owner_id=None
            )
        )

    async def is_locked(self, resource_id: str) -> bool:
        lock = await self._get_lock(resource_id)
        return lock.locked

    async def is_locked_by(
        self,
        resource_id: str,
        user_id: str,
    ) -> bool:
        lock = await self._get_lock(resource_id)
        return lock.locked and lock.owner_id == user_id

    async def _get_lock_data(self) -> dict:
        data = self._redis_client.get(self._storage_key)
        return json.loads(data) if data else {}

    async def _get_lock(self, resource_id: str) -> LockRecord:
        locks = await self._get_lock_data()
        record = locks.get(resource_id)
        return LockRecord(locked=False, owner_id=None) \
            if record is None else LockRecord(**record)

    async def _update_lock(
        self,
        resource_id: str,
        lock: LockRecord,
    ) -> None:
        locks = await self._get_lock_data()
        locks[resource_id] = lock.model_dump()
        self._redis_client.set(
            self._storage_key,
            json.dumps(locks)
        )
