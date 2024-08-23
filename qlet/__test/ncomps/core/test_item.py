import multiprocessing
import queue
import time
import unittest
from functools import cache
from typing import Callable, Sequence

from qlet.ncomps.core.item import CircleException, Item


def wait_with_timeout(
        fail_text: str,
        timeout: float | int,
        f: Callable[[multiprocessing.Queue], None],
) -> None:
    channel = multiprocessing.Queue()
    process = multiprocessing.Process(target=f, args=(channel,))
    process.start()
    channel.get()  # wait for start
    try:
        channel.get(timeout=timeout)
        process.join()
    except queue.Empty:
        process.terminate()
        process.join()
        raise Exception(fail_text)


def self_circle_case(queue: multiprocessing.Queue):
    queue.put("start")
    item = Item(
        root=True,
        v1_=lambda d: d.v1_,
    )
    try:
        item.compute()
    except CircleException:
        queue.put("end")


def inter_circle_case(queue: multiprocessing.Queue):
    queue.put("start")
    item = Item(
        root=True,
        v1_=lambda d: d.v2_,
        v2_=lambda d: d.v1_, 
    )
    try:
        item.compute()
    except CircleException:
        queue.put("end")


def long_circle_case(queue: multiprocessing.Queue):
    queue.put("start")
    item = Item(
        root=True,
        v1_=1,
        v2_=lambda d: d.v1_, 
        v3_=lambda d: d.v2_ + d.v5_,
        v4_=lambda d: d.v3_ + d.v6_,
        v5_=lambda d: d.v4_,
        v6_=lambda d: d.v5_,
    )
    try:
        item.compute()
    except CircleException:
        queue.put("end")


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

    def test_default_id(self):
        item = Item()
        self.assertEqual(item.id, "")
        self.assertNotEqual(item.displayed_id, "")

        item = Item(id="name")
        self.assertEqual(item.id, "name")
        self.assertEqual(item.displayed_id, "name")

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
        item.compute()
        self.assertEqual(item.v1_, 1)

    def test_lambda_const(self):
        item = Item(
            root=True,
            v1_=lambda d: 1,
        )
        item.compute()
        self.assertEqual(item.v1_, 1)

    def test_simple_dependency(self):
        item = Item(
            root=True,
            v1_=1,
            v2_=lambda d: d.self.v1_ + 2,
        )
        item.compute()
        self.assertEqual(item.v1_, 1)
        self.assertEqual(item.v2_, 3)

        item = Item(
            root=True,
            v1_=1,
            v2_=lambda d: d.self.v1_ + 2,
            v3_=lambda d: d.self.v2_ + d.self.v1_,
        )
        item.compute()
        self.assertEqual(item.v1_, 1)
        self.assertEqual(item.v2_, 3)
        self.assertEqual(item.v3_, 4)

    def test_shortcut_self_reference(self):
        item = Item(
            root=True,
            v1_=1,
            v2_=lambda d: d.v1_ + 2,
        )
        item.compute()
        self.assertEqual(item.v1_, 1)
        self.assertEqual(item.v2_, 3)

    def test_simple_dependency_update(self):
        item = Item(
            root=True,
            v1_=1,
            v2_=lambda d: d.self.v1_ + 2,
        )
        item.compute()
        item.v2_ = 10
        item.v1_ = lambda d: d.v2_ + 3
        item.compute()
        self.assertEqual(item.v1_, 13)
        self.assertEqual(item.v2_, 10)

        # update new variable
        item.v3_ = lambda d: d.v2_ / 2
        item.v1_ = lambda d: d.v3_ + d.v2_
        item.compute()
        self.assertEqual(item.v1_, 15)
        self.assertEqual(item.v2_, 10)
        self.assertEqual(item.v3_, 5)

        # update const variable
        item.v2_ = 20
        item.compute()
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
        root.compute()
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
        root.compute()
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
        root.compute()
        root.v1_ = 3
        child1.v2_ = lambda d: d.v1_ + 1
        root.compute()
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
        root.compute()
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
        root.compute()
        root.v1_ = 2
        root.compute()
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
        root.compute()
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
        root.compute()
        grandchild.v3_ = lambda d: d.root_item.v1_
        grandchild.v2_ = lambda d: d.parent.v1_ + d.parent.v2_ + d.v3_
        root.v1_ = lambda d: 7
        root.compute()

        self.assertEqual(root.v1_, 7)
        self.assertEqual(child.v1_, 21)
        self.assertEqual(child.v2_, 23)
        self.assertEqual(grandchild.v1_, 92)
        self.assertEqual(grandchild.v2_, 51)
        self.assertEqual(grandchild.v3_, 7)

        root.v1_ = 1
        root.compute()

        self.assertEqual(root.v1_, 1)
        self.assertEqual(child.v1_, 3)
        self.assertEqual(child.v2_, 5)
        self.assertEqual(grandchild.v1_, 20)
        self.assertEqual(grandchild.v2_, 9)
        self.assertEqual(grandchild.v3_, 1)

    def test_detect_circle(self):
        TIMEOUT = 1
        FAIL_TEXT = f"Circle not detected in {TIMEOUT}s!"
        wait_with_timeout(FAIL_TEXT, TIMEOUT, self_circle_case)
        wait_with_timeout(FAIL_TEXT, TIMEOUT, inter_circle_case)
        wait_with_timeout(FAIL_TEXT, TIMEOUT, long_circle_case)

    def test_new_child_update(self):
        child = Item(
            v1_=lambda d: d.parent.v1_ + 1,
        )
        root = Item(
            root=True,
            v1_=1,
        )
        root.compute()
        root.add_child(child)
        root.compute()
        self.assertEqual(child.v1_, 2)

    def test_new_grandchild_update(self):
        grandchild = Item(
            v1_=lambda d: d.parent.v1_ + 1,
        )
        child = Item(
            v1_=lambda d: d.parent.v1_ + 1,
            children=grandchild,
        )
        root = Item(
            root=True,
            v1_=1,
        )
        root.compute()
        root.add_child(child)
        root.compute()
        self.assertEqual(child.v1_, 2)
        self.assertEqual(grandchild.v1_, 3)

        grandchild = Item(
            v1_=lambda d: d.parent.v1_ + 1,
        )
        child = Item(
            v1_=lambda d: d.parent.v1_ + 1,
        )
        root = Item(
            root=True,
            v1_=1,
            children=child,
        )
        root.compute()
        child.add_child(grandchild)
        root.compute()
        self.assertEqual(child.v1_, 2)
        self.assertEqual(grandchild.v1_, 3)

    def test_new_peer_update(self):
        # child 2 added later
        child1 = Item(
            v1_=lambda d: d.keqing.v1_,
        )
        child2 = Item(
            id="keqing",
            v1_=11,
        )
        root = Item(
            id="keqing",
            root=True,
            v1_=1,
            children=child1,
        )
        root.compute()
        self.assertEqual(child1.v1_, 1)

        root.add_child(child2)
        root.compute()
        self.assertEqual(child1.v1_, 11)

        # check at grandchildren level
        grandchild1 = Item(
            v1_=lambda d: d.keqing.v1_,
        )
        grandchild2 = Item(
            id="keqing",
            v1_=11,
        )
        child = Item(
            children=grandchild1,
        )
        root = Item(
            id="keqing",
            root=True,
            v1_=1,
            children=child,
        )
        root.compute()
        self.assertEqual(grandchild1.v1_, 1)

        child.add_child(grandchild2)
        root.compute()
        self.assertEqual(grandchild1.v1_, 11)
    
    def test_remove_peer_update(self):
        # children level
        child1 = Item(
            v1_=lambda d: d.keqing.v1_,
        )
        child2 = Item(
            id="keqing",
            v1_=11,
        )
        root = Item(
            id="keqing",
            root=True,
            v1_=1,
            children=(
                child1,
                child2,
            ),
        )
        root.compute()
        self.assertEqual(child1.v1_, 11)

        root.remove_child(child2)
        root.compute()
        self.assertEqual(child1.v1_, 1)

        # grandchildren level
        grandchild1 = Item(
            v1_=lambda d: d.keqing.v1_,
        )
        grandchild2 = Item(
            id="keqing",
            v1_=11,
        )
        child = Item(
            children=(
                grandchild1,
                grandchild2
            ),
        )
        root = Item(
            id="keqing",
            root=True,
            v1_=1,
            children=child,
        )
        root.compute()
        self.assertEqual(grandchild1.v1_, 11)

        child.remove_child(grandchild2)
        root.compute()
        self.assertEqual(grandchild1.v1_, 1)

    def test_reserved_proeprty_keyword(self):
        class TmpItem(Item):
            @Item.cached_classproperty
            def _RESERVED_PROPERTY_NAMES(cls) -> set[str]:
                return super()._RESERVED_PROPERTY_NAMES | {
                    "a",
                    "b",
                }

        root = TmpItem(
            root=True,
            v1_=1,
            a=2,
            b=lambda d: d.v1_ + d.a,
        )
        root.compute()
        self.assertEqual(root.v1_, 1)
        self.assertEqual(root.a, 2)
        self.assertEqual(root.b, 3)

    def test_on_property_update_handler(self):
        counter = 0
        class TmpItem(Item):
            def _on_v2__change(self) -> None:
                nonlocal counter
                counter += 1

        root = TmpItem(
            root=True,
            v1_=1,
            v2_=lambda d: d.v1_ + 1,
        )
        self.assertEqual(counter, 0)
        root.compute()
        self.assertEqual(counter, 1)

    def test_compute_sub_item(self):
        root = Item(
            root=True,
            v1_=1,
            children=(
                item1 := Item(
                    v1_=lambda d: d.item2.v1_ + 1,
                ),
                item2 := Item(
                    id="item2",
                    v1_=lambda d: d.parent.v1_ + 1,
                ),
            ),
        )
        root.compute()
        item1.add_child(
            item1_1 := Item(
                v1_=lambda d: d.parent.v1_ + 1,
            )
        )
        item1.compute()
        self.assertEqual(item1.v1_, 3)
        self.assertEqual(item1_1.v1_, 4)

        root = Item(
            root=True,
            v1_=1,
            children=(
                item1 := Item(
                    v1_=lambda d: d.item2.v1_ + 1,
                ),
                Item(
                    id="item2",
                    v1_=lambda d: d.parent.v1_ + 1,
                ),
            ),
        )
        root.compute()
        item1.add_child(
            item1_1 := Item(
                v1_=lambda d: d.parent.v1_ + 1,
            )
        )
        item1.v1_ = lambda d: d.item2.v1_ + 2
        item1.compute()
        self.assertEqual(item1.v1_, 4)
        self.assertEqual(item1_1.v1_, 5)
