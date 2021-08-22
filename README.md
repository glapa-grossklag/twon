# Overview

A simple (2, n) secret-sharing scheme that allows the user to split a secret
into n shares, and require at least two shares to recover the secret.

This works by generating a line which has the secret as the y-intercept. The
"shares" are then generated as random points on this line. With one share it is
impossible to know the line, but with any two points one can recover the line
and thus recover the secret.

# Usage

Split a secret in `secret.txt` into 5 shares:

`./twon.py split secret.txt 5`

Recover a secret from the first two shares (lines) in `shares.txt`:

`./twon.py recover shares.txt`
