"""_summary_
"""


import unittest
from unittest import TestCase

from smiley.model.persistence.serialization import Serialization


class SerializationCaseTest(Serialization):
    """This is just used to test id.

    Args:
        Serialization (class): Serialization class.
    """

    def serialize(self, serialization_object: object):
        """Serialize the object information into object.

        Args:
            serialization_object (object): Object of google protocol buffer.
        """
        raise NotImplementedError

    def deserialize(self, serialization_object: object):
        """Deserialize self by serialization object.

        Args:
            serialization_object (object): Object of google protocol buffer.
        """
        raise NotImplementedError


class TestSerialization(TestCase):
    def test_id(self):
        """Test uuid."""
        id_set = set()
        for _ in range(10000):
            uuid = SerializationCaseTest().get_uuid()
            if uuid not in id_set:
                id_set.add(uuid)
            else:
                self.assert_(False)


if __name__ == "__main__":
    unittest.main()
