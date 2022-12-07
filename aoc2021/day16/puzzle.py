""" -- Advent of Code 2021 --
Day 16, https://adventofcode.com/2021/day/16

Notes on Solutions:
- Part 1 and 2: Solutions to Part 1 and 2 are essentially the same, and implemented as part of the `Decoder` class.
    Solution to this challenge relies on a framework of mutually-recursive methods, which are in turn applied
    to each corresponding substring of packets to be decoded. 
    The base case of the recursion is of course when a literal packet is found. Therefore, the `bin_literal` is 
    calculated, and converted into value to be returned. Each literal packet should be (generally) enclosed within
    operational packets which in turns read literals, or any other operation packets, recursively.
    Once submessages have been decoded, values are collected and treated accordingly to the `OPERATION_MAP`.
    As per the solution itself, two points maybe of interest:
    1) Once a `Decoder` instance has been created on a given message, its value is calculated and stored 
    in the `decode` method. This is to avoid decoding multiple times the same string.
    Note: this is of no interest for the challenge, just an example of good object encapsulation. This is 
    merely because each `decoder` instance makes sense for one and only one input `HEX` message.

    2) When calculating the `bin_literal` for literal packets, the 
    [`itertools.takewhile`](https://docs.python.org/3/library/itertools.html#itertools.takewhile) function 
    is used which in turn takes sub-portions of the input message with step `5` until a `0` initial bit 
    (i.e. **stop** bit is found). In that case, the last sequence is also added in, and the whole `bin_literal`
    finally converted.
"""

__day__ = "16"
__title__ = "Packet Decoder"
__author__ = "leriomaggio"

from pathlib import Path
from typing import Union
from functools import reduce
from operator import mul
from itertools import takewhile


def load(filepath: Union[str, Path]):
    return open(filepath).read().strip()


# =========== Part 1 ============


class Decoder:

    OPERATOR_MAP = {
        0: lambda values: sum(values),
        1: lambda values: reduce(mul, values),
        2: lambda values: min(values),
        3: lambda values: max(values),
        5: lambda values: 1 if values[0] > values[1] else 0,
        6: lambda values: 1 if values[0] < values[1] else 0,
        7: lambda values: 1 if values[0] == values[1] else 0,
    }

    def __init__(self, msg: str):
        self.msg = msg
        self.versions: list[str] = list()
        self.value: int = -1

    def decode(self):
        if self.value < 0:  # this is to avoid decoding the same message multiple times
            bin_msg = "".join(
                map(lambda c: str(bin(int(c, base=16)))[2:].zfill(4), self.msg)
            )
            _, self.value = self._decode(bin_msg)
        return self.value

    def _decode_literal_packet(self, message: str) -> tuple[str, int]:
        bin_literal = "".join(
            map(
                lambda i: message[i + 1 : i + 5],
                takewhile(lambda i: message[i] != "0", range(0, len(message), 5)),
            )
        )
        bin_literal += message[5 * (lb := len(bin_literal) // 4) + 1 : 5 * lb + 5]
        return message[5 * lb + 5 :], int(bin_literal, 2)

    def _decode_operator_packet(
        self, message: str, packet_type: int
    ) -> tuple[str, int]:
        length_type_bit = int(message[0], base=2)
        packet_values = list()
        if length_type_bit == 0:
            len_bits, message = int(message[1:16], base=2), message[16:]
            starting_len, read_bits = len(message), 0
            while read_bits != len_bits:
                message, value = self._decode(message)
                packet_values.append(value)
                read_bits = starting_len - len(message)
        else:  # length_type_bit is 1
            n_packets, message = int(message[1:12], base=2), message[12:]
            for _ in range(n_packets):
                message, value = self._decode(message)
                packet_values.append(value)
        # eval
        return message, self.OPERATOR_MAP[packet_type](packet_values)

    def _decode(self, message: str) -> tuple[str, int]:
        packet_version = int(message[0:3], base=2)
        packet_type_ = int(message[3:6], base=2)
        self.versions.append(packet_version)
        if packet_type_ == 4:  # lit
            return self._decode_literal_packet(message[6:])
        else:
            return self._decode_operator_packet(message[6:], packet_type_)


def part1(msg: str) -> int:
    decoder = Decoder(msg)
    decoder.decode()
    return sum(decoder.versions)


# =========== Part 2 ============


def part2(msg: str) -> int:
    decoder = Decoder(msg)
    decoder.decode()
    return decoder.value


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2021 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    msg = load(filepath=filepath)
    # solve part 1
    print(part1(msg))
    # solve part 2
    print(part2(msg))
