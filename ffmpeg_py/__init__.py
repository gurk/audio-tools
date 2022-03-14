from .exceptions import FilterInstanceError


class FilterBase:
    name = ''
    settings = {}

    def __init__(self, **kwargs):
        self.settings.update(kwargs)

    def __str__(self):
        # generate filter argument string
        return self._make_filter(self.name, self.settings)

    @staticmethod
    def _make_filter(command: str, settings: dict) -> str:
        params = [f'{k}={v}' for k, v in settings.items()]
        return f'{command}={":".join(params)}'


class Compressor(FilterBase):
    name = 'acompressor'
    settings = dict(
        level_in=1,
        mode='downward',
        threshold=0.1,
        ratio=2,
        attack=20,
        release=250,
        makeup=1,
        knee=2.82843,
        link='average',
        detection='rms',
        mix=1
    )


class FadeOut(FilterBase):
    name = 'afade'
    settings = dict(
        type='out',
        start_time=1.98,
        duration=0.02,
        curve='tri'
    )


class FilterGraph:
    def __init__(self, *filters):
        for f in filters:
            if not isinstance(f, FilterBase):
                raise FilterInstanceError('Filter must be subclass instance of FilterBase.')
        self._filters = filters

    def __str__(self):
        # generate filtergraph argument string
        return ','.join([str(f) for f in self._filters])


