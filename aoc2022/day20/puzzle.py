""" -- Advent of Code 2022 --
Day 20, https://adventofcode.com/2022/day/20

Notes on Solutions:
The key to this puzzle is built around two key pieces (directly
gathered from the Python standard library), and both wrapping around
the same idea of _using the "right" data abstractions_.

This puzzle is a game of rotations over a _circular_ list (queue)
that represents the encrypted message. Therefore, we could represent
the encrypted message using `collections.deque`, also providing a `rotate`
method that shifts items around the queue. This is _sort of_ what the puzzle
is indeed asking to do. In fact, we would need to "rotate" items in the queue
by actually moving them to their corresponding position, while slicing the
rest of the queue in a cirucular fashion.

To do so, the solution adopts a "trick" that would avoid using any
additional data structures (than the actual `deque`), or any (much more)
complicated slicing over indices. The trick is indeed inspired in how the
_insertion sort_ algorithm works.
In more details, for each item (processed in the original order), we do:

1. Rotate the encrypted message by n positions on the left, where n is the current
position of the item in the encrypted message.
(this would have the effect of moving the target item to the head of the queue).

2. Remove the target item from the queue (i.e. `popleft` as it's the new head)

3. Rotate the queue in the **opposite** direction of the item's value (i.e.
left if positive, right if negative). This would have the effect of having
the two values where the target item was supposed to be moved in between as
the new head and tail of the queue.

4. Finally, add the target item to the head of the queue (i.e. `appendleft`), so
it now results correctly _inserted_ in between.

As a last step, we move the item with value zero to the head of the queue
(using the same "trick" as in step 1) so that the answer to the puzzle
could be calculated as `modulo` the `len(encrypted_message)`.

There is a small catch though! Even if test data does NOT contain repetitions (i.e.
items with the same values), the input puzzle does, therefore shifting ops in step 1
should take this into account. To do so, we need to represent items in the
encrypted message with a proper abstraction that would make them uniquey identifiable.

To do so, we will represent each encrypted number as `Encrypted` that is a
`collections.namedtuple` that will map to each number its original position
as a uniquely identifiable id.

Part 1 & 2:
The difference between part 1 and part 2 is merely based on the fact that
in part 2 we need to apply the same game 10 times, as well as applying
a _decryption key_ to input values (which is generically set equal to `1`
in part 1).
"""

__day__ = "20"
__title__ = "Grove Positioning System"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from collections import namedtuple, deque

Encrypted = namedtuple("Encrypted", ("eid", "value"))


def load(filepath: Union[str, Path]):
    return parse_input(open(filepath).read().split("\n"))


def parse_input(lines: list[str]) -> tuple[int]:
    return tuple(map(int, lines))


def decrypt(message: tuple[int], times: int = 1, dec_key: int = 1):
    encrypted_msg = deque(
        Encrypted(eid=pos, value=(v * dec_key)) for pos, v in enumerate(message)
    )
    original_order = tuple(encrypted_msg)

    for _ in range(times):
        for enc in original_order:
            encrypted_msg.rotate(-encrypted_msg.index(enc))
            encrypted_msg.popleft()
            encrypted_msg.rotate(-enc.value)
            encrypted_msg.appendleft(enc)

    enc_zero = next(filter(lambda e: e.value == 0, encrypted_msg))
    encrypted_msg.rotate(-encrypted_msg.index(enc_zero))
    return (
        encrypted_msg[1000 % len(encrypted_msg)].value
        + encrypted_msg[2000 % len(encrypted_msg)].value
        + encrypted_msg[3000 % len(encrypted_msg)].value
    )


# =========== Part 1 ============


def part1(data: list[int]) -> int:
    return decrypt(message=data, times=1)


# =========== Part 2 ============


def part2(data: list[int]) -> int:
    return decrypt(message=data, times=10, dec_key=811589153)


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2022 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    data = load(filepath=filepath)
    # solve part 1
    print(part1(data))
    # solve part 2
    print(part2(data))
