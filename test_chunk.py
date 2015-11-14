from buffalo import utils
utils.init()

from chunk import Chunk
from pluginManager import PluginManager

PluginManager.loadPlugins()

class TestChunk:
	def test_init(self):
		assert Chunk(0,0) is not None

	def test_data(self):
		chunk = Chunk(100,100)
		assert chunk.data is not None
		assert len(chunk.data) is Chunk.CHUNK_HEIGHT and len(chunk.data[0]) is Chunk.CHUNK_WIDTH

	def test_pos(self):
		chunk = Chunk(100,100)
		assert chunk.pos == (100, 100)

	def test_surface(self):
		assert Chunk(0,0).surface is not None
