from unittest import mock


class AsyncMock:
    def __init__(self, return_value=None, side_effect=None):
        self.return_value = return_value
        self.side_effect = side_effect

    def _raise_or_call(self):
        if isinstance(self.side_effect, Exception):
            raise self.side_effect()

        if callable(self.side_effect):
            return self.side_effect()

        return None

    async def __call__(self, *args, **kwargs):
        if self.side_effect:
            return self._raise_or_call()

        return self.return_value

    def __getattr__(self, _):
        if self.side_effect:
            return self._raise_or_call()

        return mock.AsyncMock(return_value=self.return_value)
