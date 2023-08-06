
# Invicta

A fun little command line utility for [Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher) encryption and decryption.

## Installation

Clone the repository and install with pip.

```
git clone https://github.com/LilyAsFlora/invicta/
cd invicta
pip install .
```

## Usage
```
invicta [-h] [-v] {encrypt,decrypt} ...
```

#### Global Options
`-h, --help` — Show a help message and exit.

`-v, --version` —  Show the program's version number and exit.

### Encryption
```
invicta encrypt [-h] shift text
```

#### Positional Arguments

`shift` —        The number of alphabet positions to shift letters by. This
                 value can be positive or negative, and will be rounded to the
                 nearest integer.
                 
`text` —         The plaintext to encrypt. Non-ASCII characters and whitespace
                 are preserved.

### Decryption

Here, decryption is done with a brute-force approach. If the `--english` flag is not used, the user must interpret the results.

```
invicta decrypt [-h] [-o] [-e] text
```
#### Positional Arguments
`text` — The ciphertext to decrypt. Will output all possible solutions.

#### Options
`-h, --help` — Show a help message and exit.

`-o, --output-shifts` — Shows the shift keys needed to get from each plaintext to the ciphertext. This shows both positive & negative keys (mod 26).

`-e, --english` — Only output plaintexts containing English text.

## Encryption Examples

### Positive shift with spaces:

```
$ invicta 3 "Hello, world!"
Khoor, zruog!
```

### Negative shift with spaces:

```
$ invicta -2 "Hello, world!"
Fcjjm, umpjb!
```

### Shift greater than alphabet length:

```
$ invicta 28 "Hello, world!"
Jgnnq, yqtnf!
```

## Decryption Examples

### Multi-word decryption with shift keys:
```
$ invicta decrypt --output-shifts "Zwddg, ogjdv!"
25 -1 Axeeh, phkew!
24 -2 Byffi, qilfx!
23 -3 Czggj, rjmgy!
22 -4 Dahhk, sknhz!
21 -5 Ebiil, tloia!
20 -6 Fcjjm, umpjb!
19 -7 Gdkkn, vnqkc!
18 -8 Hello, world! ← This one works!
17 -9 Ifmmp, xpsme!
16 -10 Jgnnq, yqtnf!
15 -11 Khoor, zruog!
14 -12 Lipps, asvph!
13 -13 Mjqqt, btwqi!
12 -14 Nkrru, cuxrj!
11 -15 Olssv, dvysk!
10 -16 Pmttw, ewztl!
9 -17 Qnuux, fxaum!
8 -18 Rovvy, gybvn!
7 -19 Spwwz, hzcwo!
6 -20 Tqxxa, iadxp!
5 -21 Uryyb, jbeyq!
4 -22 Vszzc, kcfzr!
3 -23 Wtaad, ldgas!
2 -24 Xubbe, mehbt!
1 -25 Yvccf, nficu!
```

### Multi-word decryption with keys, filtering for English:

```
$ invicta decrypt --english --output-shifts "Zwddg, ogjdv!"
18 -8 Hello, world!
```

From these results, we can conclude the string "Hello, world!" was shifted by either 18 or -8 characters to produce "Zwddg, ogjdv!".

## Running Tests

All unit tests are in `tests/`.

To run **all tests**, run:

`python -m unittest tests/*.py`

To run a **single test**, run:

`python -m unittest tests/<TEST>`

Where `<TEST>` is the name of the target test file.

### Example (as of v0.5.0)
```
$ python -m unittest tests/*.py
...............................
----------------------------------------------------------------------
Ran 27 tests in 0.929s

OK
```
