import unittest
from store import Store
from skip_list import SkipList

class TestSkipListStore(unittest.TestCase):
    def test_store_insertion_and_search(self):
        sl = SkipList(maxLevels=4)
        s1 = Store(10, "value10")
        s2 = Store("apple", "valueApple")
        s3 = Store(5, "value5")
        
        sl.insert(s1)
        sl.insert(s2)
        sl.insert(s3)
        
        # Searching should use a Store object with the same key
        res10 = sl.search(Store(10, ""))
        self.assertIsNotNone(res10)
        self.assertEqual(res10.value, "value10")
        
        resApple = sl.search(Store("Apple", ""))
        self.assertIsNotNone(resApple)
        self.assertEqual(resApple.value, "valueApple")
        
        res5 = sl.search(Store(5, ""))
        self.assertIsNotNone(res5)
        self.assertEqual(res5.value, "value5")
        
        # Non-existent
        self.assertIsNone(sl.search(Store(100, "")))
        self.assertIsNone(sl.search(Store("banana", "")))

    def test_no_duplicates(self):
        sl = SkipList(maxLevels=4)
        s1 = Store(10, "first_value")
        s2 = Store(10, "second_value")
        
        sl.insert(s1)
        sl.insert(s2)
        
        # Check that it doesn't save duplicates by traversing the bottom-most list.
        count = 0
        curr = sl.root
        while curr.bottom:
            curr = curr.bottom
            
        curr = curr.next # Skip -inf
        while curr:
            if isinstance(curr.data, Store) and curr.data.key == 10:
                count += 1
            curr = curr.next
            
        self.assertEqual(count, 1, "There should be exactly one node with key 10")
        
        # The stored object should be evaluated.
        res = sl.search(Store(10, ""))
        self.assertIsNotNone(res)
        
    def test_update_duplicate(self):
        sl = SkipList(maxLevels=4)
        s1 = Store(10, "initial_value")
        s2 = Store(10, "updated_value")
        
        sl.insert(s1)
        sl.insert(s2)
        
        # Both top level and bottom level should have "updated_value"
        res = sl.search(Store(10, ""))
        self.assertIsNotNone(res)
        self.assertEqual(res.value, "updated_value")

    def test_mixed_types(self):
        sl = SkipList(maxLevels=4)
        elements = [
            Store(20, "v20"),
            Store("zebra", "vZebra"),
            Store(1, "v1"),
            Store("apple", "vApple")
        ]
        for e in elements:
            sl.insert(e)
            
        for e in elements:
            res = sl.search(Store(e.key, ""))
            self.assertIsNotNone(res)
            self.assertEqual(res.value, e.value)

if __name__ == "__main__":
    unittest.main()
