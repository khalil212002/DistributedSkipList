import unittest
import random
from skip_list import SkipList
from linked_list_2d import LinkedList2D


class TestSkipListComprehensive(unittest.TestCase):
    def setUp(self):
        self.max_levels = 16
        self.sl = SkipList(maxLevels=self.max_levels)

    def test_empty_list(self):
        """Test searching in an empty list."""
        self.assertIsNone(self.sl.search(100))
        self.assertIsNone(self.sl.search(float("inf")))
        self.assertIsNone(self.sl.search(float("-inf")))

    def test_single_element(self):
        """Test inserting and searching for a single element."""
        self.sl.insert(42)
        self.assertEqual(self.sl.search(42), 42)
        self.assertIsNone(self.sl.search(41))
        self.assertIsNone(self.sl.search(43))
        self.verify_integrity()

    def test_duplicates(self):
        """Test inserting duplicate values."""
        self.sl.insert(10)
        self.sl.insert(10)
        self.sl.insert(10)
        self.assertEqual(self.sl.search(10), 10)
        self.verify_integrity()

    def test_sorted_insertion(self):
        """Test inserting elements in sorted order."""
        elements = list(range(100))
        for x in elements:
            self.sl.insert(x)
        for x in elements:
            self.assertEqual(self.sl.search(x), x)
        self.verify_integrity()

    def test_reverse_sorted_insertion(self):
        """Test inserting elements in reverse sorted order."""
        elements = list(range(99, -1, -1))
        for x in elements:
            self.sl.insert(x)
        for x in range(100):
            self.assertEqual(self.sl.search(x), x)
        self.verify_integrity()

    def test_random_insertion(self):
        """Test inserting elements in random order."""
        elements = list(range(500))
        random.shuffle(elements)
        for x in elements:
            self.sl.insert(x)
        for x in range(500):
            self.assertEqual(self.sl.search(x), x)
        self.verify_integrity()

    def test_negative_values(self):
        """Test with negative values."""
        values = [-100, -50, -1, 0, 1, 50, 100]
        for v in values:
            self.sl.insert(v)
        for v in values:
            self.assertEqual(self.sl.search(v), v)
        self.verify_integrity()

    def test_boundary_values(self):
        """Test with extremely large and small values."""
        self.sl.insert(float("inf"))
        self.sl.insert(1e100)
        self.sl.insert(-1e100)

        self.assertEqual(self.sl.search(float("inf")), float("inf"))
        self.assertEqual(self.sl.search(1e100), 1e100)
        self.assertEqual(self.sl.search(-1e100), -1e100)
        self.verify_integrity()

    def test_not_found_between(self):
        """Test searching for values that are between inserted values."""
        self.sl.insert(10)
        self.sl.insert(20)
        self.sl.insert(30)
        self.assertIsNone(self.sl.search(15))
        self.assertIsNone(self.sl.search(25))
        self.assertIsNone(self.sl.search(5))
        self.assertIsNone(self.sl.search(35))
        self.verify_integrity()

    def test_basic_deletion(self):
        """Test deleting elements from the middle, start, and end."""
        elements = [10, 20, 30, 40, 50]
        for x in elements:
            self.sl.insert(x)

        # Delete from middle
        self.sl.delete(30)
        self.assertIsNone(self.sl.search(30))
        self.verify_integrity()

        # Delete from start
        self.sl.delete(10)
        self.assertIsNone(self.sl.search(10))
        self.verify_integrity()

        # Delete from end
        self.sl.delete(50)
        self.assertIsNone(self.sl.search(50))
        self.verify_integrity()

        # Remaining should be there
        self.assertEqual(self.sl.search(20), 20)
        self.assertEqual(self.sl.search(40), 40)

    def test_delete_non_existent(self):
        """Test deleting an element that is not in the list."""
        self.sl.insert(10)
        self.sl.delete(20) # Should not crash
        self.assertEqual(self.sl.search(10), 10)
        self.verify_integrity()

    def test_delete_all(self):
        """Test deleting all elements from the list."""
        elements = list(range(50))
        for x in elements:
            self.sl.insert(x)

        for x in elements:
            self.sl.delete(x)
            self.assertIsNone(self.sl.search(x))

        self.verify_integrity()
        # Ensure only root nodes remain in each level
        curr = self.sl.root
        while curr.top:
            curr = curr.top
        while curr:
            self.assertIsNone(curr.next)
            curr = curr.bottom

    def test_max_levels_one(self):

        """Test with maxLevels set to 1 (effectively a linked list)."""
        sl_small = SkipList(maxLevels=1)
        for i in range(10):
            sl_small.insert(i)
        for i in range(10):
            self.assertEqual(sl_small.search(i), i)
        self.assertEqual(sl_small.height, 1)

    def verify_integrity(self):
        """
        Walks the skip list to ensure all next/prev and top/bottom pointers are consistent.
        """
        # Start at the top root
        curr_row_root = self.sl.root

        # Go up to the very top root if self.sl.root isn't there (though it should be)
        while curr_row_root.top:
            curr_row_root = curr_row_root.top

        while curr_row_root:
            curr = curr_row_root
            while curr:
                # Check next/prev consistency
                if curr.next:
                    self.assertEqual(
                        curr.next.prev, curr, f"Next pointer mismatch at {curr.data}"
                    )

                # Check top/bottom consistency
                if curr.bottom:
                    self.assertEqual(
                        curr.bottom.top, curr, f"Bottom pointer mismatch at {curr.data}"
                    )

                # Check that row is sorted
                if curr.next:
                    # Use a small tolerance for floats or handle -inf
                    self.assertTrue(
                        curr.data <= curr.next.data,
                        f"Row not sorted: {curr.data} > {curr.next.data}",
                    )

                # If there's a bottom node, it should have the same data
                if curr.bottom:
                    self.assertEqual(
                        curr.data,
                        curr.bottom.data,
                        f"Vertical data mismatch: {curr.data} != {curr.bottom.data}",
                    )

                curr = curr.next

            curr_row_root = curr_row_root.bottom


if __name__ == "__main__":
    unittest.main()
