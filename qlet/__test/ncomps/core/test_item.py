import unittest

from qlet.ncomps.core.item import Item

class TestItem(unittest.TestCase):

    def test_custom_id_pattern(self):
        self.assertRaises(
            AssertionError,
            lambda: Item(id="parent"),
        )
        self.assertRaises(
            AssertionError,
            lambda: Item(id="self"),
        )
        self.assertRaises(
            AssertionError,
            lambda: Item(id="_v1"),
        )
        self.assertRaises(
            AssertionError,
            lambda: Item(id="v1_"),
        )
        self.assertRaises(
            AssertionError,
            lambda: Item(id="v 1"),
        )
        self.assertRaises(
            AssertionError,
            lambda: Item(id="1v"),
        )

    def test_custom_variable_pattern(self):
        # custom variable cannot start with '_'
        self.assertRaises(
            AssertionError,
            lambda: Item(_v1=1),
        )
        # custom variable cannot end with '_'
        self.assertRaises(
            AssertionError,
            lambda: Item(v1=1),
        )

    def test_const(self):
        item = Item(
            root=True,
            v1_=1,
        )
        item.update()
        self.assertEqual(item.v1_, 1)

    def test_lambda_const(self):
        item = Item(
            root=True,
            v1_=lambda d: 1,
        )
        item.update()
        self.assertEqual(item.v1_, 1)

    def test_simple_dependency(self):
        item = Item(
            root=True,
            v1_=1,
            v2_=lambda d: d.self.v1_ + 2,
        )
        item.update()
        self.assertEqual(item.v1_, 1)
        self.assertEqual(item.v2_, 3)

        item = Item(
            root=True,
            v1_=1,
            v2_=lambda d: d.self.v1_ + 2,
            v3_=lambda d: d.self.v2_ + d.self.v1_,
        )
        item.update()
        self.assertEqual(item.v1_, 1)
        self.assertEqual(item.v2_, 3)
        self.assertEqual(item.v3_, 4)

    def test_shortcut_self_reference(self):
        item = Item(
            root=True,
            v1_=1,
            v2_=lambda d: d.v1_ + 2,
        )
        item.update()
        self.assertEqual(item.v1_, 1)
        self.assertEqual(item.v2_, 3)

    def test_simple_dependency_update(self):
        item = Item(
            root=True,
            v1_=1,
            v2_=lambda d: d.self.v1_ + 2,
        )
        item.update()
        item.v2_ = 10
        item.v1_ = lambda d: d.v2_ + 3
        item.update()
        self.assertEqual(item.v1_, 13)
        self.assertEqual(item.v2_, 10)

        # update new variable
        item.v3_ = lambda d: d.v2_ / 2
        item.v1_ = lambda d: d.v3_ + d.v2_
        item.update()
        self.assertEqual(item.v1_, 15)
        self.assertEqual(item.v2_, 10)
        self.assertEqual(item.v3_, 5)

        # update const variable
        item.v2_ = 20
        item.update()
        self.assertEqual(item.v1_, 30)
        self.assertEqual(item.v2_, 20)
        self.assertEqual(item.v3_, 10)

    def test_children_dependency(self):
        # check reference to "parent"
        child1 = Item(
            id="c1",
            v1_=lambda d: d.parent.v2_ * 2,
        )
        root = Item(
            id="root_item",
            root=True,
            v1_=1,
            v2_=lambda d: d.v1_ + 2,
            children=(
                child1,
            ),
        )
        root.update()
        self.assertEqual(root.v1_, 1)
        self.assertEqual(root.v2_, 3)
        self.assertEqual(child1.v1_, 6)

        # check reference by id
        child1 = Item(
            id="c1",
            v1_=lambda d: d.root_item.v2_ * 2,
        )
        root = Item(
            id="root_item",
            root=True,
            v1_=1,
            v2_=lambda d: d.v1_ + 2,
            children=(
                child1,
            ),
        )
        root.update()
        self.assertEqual(root.v1_, 1)
        self.assertEqual(root.v2_, 3)
        self.assertEqual(child1.v1_, 6)

    def test_children_dependency_update(self):
        child1 = Item(
            id="c1",
            v1_=lambda d: d.parent.v2_ * 2,
        )
        root = Item(
            id="root_item",
            root=True,
            v1_=1,
            v2_=lambda d: d.v1_ + 2,
            children=(
                child1,
            ),
        )
        root.update()
        root.v1_ = 3
        child1.v2_ = lambda d: d.v1_ + 1
        root.update()
        self.assertEqual(root.v1_, 3)
        self.assertEqual(root.v2_, 5)
        self.assertEqual(child1.v1_, 10)
        self.assertEqual(child1.v2_, 11)

    def test_multiple_children_cross_dependency(self):
        child1 = Item(
            id="c1",
            v1_=lambda d: d.parent.v2_ * 2,
            v2_=lambda d: d.c2.v1_ - 1,
        )
        child2 = Item(
            id="c2",
            v1_=lambda d: d.c1.v1_ * 2,
            v2_=lambda d: d.c1.v1_ * d.c1.v2_,
        )
        root = Item(
            id="root_item",
            root=True,
            v1_=1,
            v2_=lambda d: d.v1_ + 2,
            children=(
                child1,
                child2,
            ),
        )
        root.update()
        self.assertEqual(root.v1_, 1)
        self.assertEqual(root.v2_, 3)
        self.assertEqual(child1.v1_, 6)
        self.assertEqual(child1.v2_, 11)
        self.assertEqual(child2.v1_, 12)
        self.assertEqual(child2.v2_, 66)

    def test_multiple_children_cross_dependency_update(self):
        child1 = Item(
            id="c1",
            v1_=lambda d: d.parent.v2_ * 2,
            v2_=lambda d: d.c2.v1_ - 1,
        )
        child2 = Item(
            id="c2",
            v1_=lambda d: d.c1.v1_ * 2,
            v2_=lambda d: d.c1.v1_ * d.c1.v2_,
        )
        root = Item(
            root=True,
            v1_=1,
            v2_=lambda d: d.v1_ + 2,
            children=(
                child1,
                child2,
            ),
        )
        root.update()
        root.v1_ = 2
        root.update()
        self.assertEqual(root.v1_, 2)
        self.assertEqual(root.v2_, 4)
        self.assertEqual(child1.v1_, 8)
        self.assertEqual(child1.v2_, 15)
        self.assertEqual(child2.v1_, 16)
        self.assertEqual(child2.v2_, 120)

    def test_grandchildren_dependency(self):
        grandchild = Item(
            v1_=lambda d: d.parent.v2_ * 4,
        )
        child = Item(
            v1_=lambda d: d.parent.v1_ * 3,
            v2_=lambda d: d.v1_ + 2,
            children=(
                grandchild,
            ),
        )
        root = Item(
            root=True,
            v1_=1,
            children=(
                child,
            ),
        )
        root.update()
        self.assertEqual(root.v1_, 1)
        self.assertEqual(child.v1_, 3)
        self.assertEqual(child.v2_, 5)
        self.assertEqual(grandchild.v1_, 20)

    def test_grandchildren_dependency_update(self):
        grandchild = Item(
            v1_=lambda d: d.parent.v2_ * 4,
        )
        child = Item(
            v1_=lambda d: d.parent.v1_ * 3,
            v2_=lambda d: d.v1_ + 2,
            children=(
                grandchild,
            ),
        )
        root = Item(
            id="root_item",
            root=True,
            v1_=1,
            children=(
                child,
            ),
        )
        root.update()
        grandchild.v3_ = lambda d: d.root_item.v1_
        grandchild.v2_ = lambda d: d.parent.v1_ + d.parent.v2_ + d.v3_
        root.v1_ = lambda d: 7
        root.update()

        self.assertEqual(root.v1_, 7)
        self.assertEqual(child.v1_, 21)
        self.assertEqual(child.v2_, 23)
        self.assertEqual(grandchild.v1_, 92)
        self.assertEqual(grandchild.v2_, 51)
        self.assertEqual(grandchild.v3_, 7)

        root.v1_ = 1
        root.update()

        self.assertEqual(root.v1_, 1)
        self.assertEqual(child.v1_, 3)
        self.assertEqual(child.v2_, 5)
        self.assertEqual(grandchild.v1_, 20)
        self.assertEqual(grandchild.v2_, 9)
        self.assertEqual(grandchild.v3_, 1)
