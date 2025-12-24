# hypr
A little programming language that I made
# Notes
I'm too lazy to make docs, so you'll have to reverse engineer the six example code files added... for now.
Also the programming language hasn't been settled yet and things may change.
## Hypr 1.0 code files
To compile Hypr 1.0 code files in the 1.1 version of the compiler, add `#legacy10` at the top of your code.
### supercomp.phf
Searches for all Highly Composite Numbers (numbers with more divisors than anything below) below 10000.
### test.phf
Searches for the numbers whose Collatz sequence is longer than anything below. Note that due to a bug, 1 has a length of 4
### hworld.phf
The obligatory Hello World program. Will work on Hypr 1.1 without needing the `#legacy10` tag.
### sqrt.phf
Computes the square root of a number, as (unfortunately) the language doesn't (yet) have sqrt functions.
## Hypr 1.1 code files
Hypr 1.1 massively simplifies control flow.
### collatz_v2.phf
`test.phf` rewritten in 1.1 as a demonstation.
### fizzbuzz.phf
A slightly modified FizzBuzz program, to test nested ifs.
### collatz_v3.phf
I just love the Collatz problem as a benchmark for the compiler. Tests functions
### abacaba.phf
`1 2 1 4 1 2 1 8 1 2 1 4 1 2 1`
The numeric ABACABA sequence. See above. Tests recursion.
# Formats
Hypr uses 2 file formats, PHF (Plain Hypr File) for reading by the Interpreter, and CHF (Compiled Hypr File) for accelerated execution. CHF is simpler for computers, while PHF is best for programmers.