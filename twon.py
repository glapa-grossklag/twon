#!/usr/bin/env python3
"""
twon.py

A simple (2, n) secret-sharing scheme that allows the user to split a secret
into n shares, and require at least two shares to recover the secret.
"""
import argparse
import sys
from random import randrange as uniform


def __byte_length(n: int) -> int:
    """
    The minimum number of bytes required to hold n.
    """
    return (n.bit_length() // 8) + (1 if n.bit_length() % 8 != 0 else 0)


def __encode(s: bytes) -> int:
    """
    Encode bytes as an int.
    """
    return int.from_bytes(s, "big")

def __decode(n: int):
    """
    Decode an int into :ytes.
    """
    return n.to_bytes(__byte_length(n), "big")


def __slope(a: tuple[int, int], b: tuple[int, int]):
    """
    The slope between two points, rounded down to the nearest integer.
    """
    if b[0] - a[0] == 0:
        raise ValueError("infinite slope")
    return (a[1] - b[1]) // (b[0] - a[0])


def split(secret: int, n: int) -> list[tuple[int, int]]:
    """
    Split a secret into n shares. Each share is a point on a line.
    """
    if n < 2:
        raise ValueError("a secret cannot be split into less than two shares")

    # Create the line upon which all shares will lie. The secret is the
    # y-intercept.
    m = uniform(0, secret)

    def l(x):
        return m * x + secret

    # Generate n unique shares.
    shares = set()
    while len(shares) < n:
        x = uniform(0, secret)
        share = (x, l(x))
        shares.add(share)

    return list(shares)


def recover(a: tuple[int, int], b: tuple[int, int]) -> int:
    """
    Retrieve the secret using two shares.
    """
    m = __slope(a, b)
    secret = a[1] + m * a[0]
    return secret


def main():
    # ==========================================================================
    # Parse Arguments
    # ==========================================================================
    parser = argparse.ArgumentParser(
        description="""
        A simple (2, n) secret-sharing scheme that allows the user to split a
        secret into n shares, and require at least two shares to recover the
        secret.
        """
    )
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Subcommand: split
    split_parser = subparsers.add_parser(
        "split",
        help="split a secret into multiple shares"
    )
    split_parser.add_argument(
        "file",
        help="the file to split",
        type=argparse.FileType("rb")
    )
    split_parser.add_argument(
        "n",
        help="the number of shares to generate",
        type=int
    )

    # Subcommand: recover
    recover_parser = subparsers.add_parser(
        "recover",
        help="recover a secret from two shares"
    )
    recover_parser.add_argument(
        "file",
        help="the file from which to read shares",
        type=argparse.FileType("rb")
    )

    args = parser.parse_args()

    # ==========================================================================
    # Split/Recover
    # ==========================================================================

    if args.subparser_name not in ("split", "recover"):
        parser.print_help()
        quit(2)

    # Regardless of mode, there will always be a file that needs reading.
    contents = args.file.read()

    # If stdin is opened, the file will be in text mode rather than binary
    # mode, meaning `contents` is a string. It needs to be bytes.
    if args.file == sys.stdin:
        contents = bytes(contents, "ascii")

    if args.subparser_name == "split":
        secret = __encode(contents)
        shares = split(secret, args.n)

        for share in shares:
            x, y = map(hex, share)
            print(x + "\t" + y)
    elif args.subparser_name == "recover":
        # Parse shares.
        shares = [line.split() for line in contents.splitlines()]
        shares = [(int(x, 16), int(y, 16)) for (x, y) in shares]

        # Recover secret.
        secret = recover(shares[0], shares[1])
        sys.stdout.buffer.write(__decode(secret))

    args.file.close()


if __name__ == "__main__":
    main()
