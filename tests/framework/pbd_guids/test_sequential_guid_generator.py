import unittest
import uuid
from unittest.mock import patch
from pbd_guids.sequential_guid_generator import SequentialGuidGenerator

class TestSequentialGuidGenerator(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.guid_generator = SequentialGuidGenerator()

    async def test_happy_path(self):
        guid1 = await self.guid_generator.create()
        guid2 = await self.guid_generator.create()
        self.assertIsInstance(guid1, uuid.UUID)
        self.assertIsInstance(guid2, uuid.UUID)
        self.assertNotEqual(guid1, guid2)

    async def test_sequence_increment(self):
        with patch('time.time_ns', return_value=1609459200000000):
            guid1 = await self.guid_generator.create()
        with patch('time.time_ns', return_value=1609459200000000):
            guid2 = await self.guid_generator.create()
        self.assertNotEqual(guid1, guid2)

    # @pytest.mark.slow
    # async def test_timestamp_increment_on_same_time(self):
    #     with patch('time.time_ns', return_value=1609459200000000):
    #         for _ in range(0x10000):
    #             await self.guid_generator.create()
    #     with patch('time.time_ns', return_value=1609459200000000):
    #         guid1 = await self.guid_generator.create()
    #     with patch('time.time_ns', return_value=1609459200000001):
    #         guid2 = await self.guid_generator.create()
    #     self.assertNotEqual(guid1, guid2)

    # @pytest.mark.slow
    # async def test_sequence_wraparound(self):
    #     with patch('time.time_ns', return_value=1609459200000000):
    #         for _ in range(0x10000):
    #             await self.guid_generator.create()
    #         guid1 = await self.guid_generator.create()
    #     with patch('time.time_ns', return_value=1609459200000001):
    #         guid2 = await self.guid_generator.create()
    #     self.assertNotEqual(guid1, guid2)

    async def test_timestamp_increment(self):
        with patch('time.time_ns', return_value=1609459200000000):
            guid1 = await self.guid_generator.create()
        with patch('time.time_ns', return_value=1609459201000000):
            guid2 = await self.guid_generator.create()
        self.assertNotEqual(guid1, guid2)

if __name__ == '__main__':
    unittest.main()