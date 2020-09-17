from unittest import mock


class AsyncMock:
    def __init__(self, return_value=None, side_effect=None):
        self._return_value = return_value
        self._side_effect = side_effect

    def _raise_or_call(self):
        if isinstance(self._side_effect, Exception):
            raise self._side_effect()

        if callable(self._side_effect):
            return self._side_effect()

        return None

    async def __call__(self, *args, **kwargs):
        if self._side_effect:
            return self._raise_or_call()

        return self._return_value

    def __getattr__(self, _):
        if self._side_effect:
            return self._raise_or_call()

        return mock.AsyncMock(return_value=self._return_value)
