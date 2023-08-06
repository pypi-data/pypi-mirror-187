import langchain
from vcr.patch import CassettePatcherBuilder as OgCassettePatcherBuilder

from .cache import VcrCache


class CachePatch:
    def __init__(self, cassette):
        self.cache = VcrCache(cassette)

    def __enter__(self):
        langchain.llm_cache = self.cache

    def __exit__(self, *args):
        langchain.llm_cache = None


class CassettePatcherBuilder(OgCassettePatcherBuilder):
    def build(self):
        return [self._llm_cache()]

    def _llm_cache(self):
        return CachePatch(self._cassette)
