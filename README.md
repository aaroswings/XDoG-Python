# XDoG-Python
Python command-line implementation of XDoG Image filter modeled after [CenalUnal's Matlab implementation](https://github.com/CemalUnal/XDoG-Filter).
Run with commands:
```
-i/--input : input image file path
-o/--output : output image file path
-p/--params : XDoG parameters in the following order: gamma, phi, epsilon, k, sigma

Example:
python XDoG.py -i ./input.png -o ./output.png -p 0.98, 200, -0.1, 1.6, 0.8
```
Uses 0.98, 200, -0.1, 1.6, 0.8 as default parameters and will save out an output file in the same location as the input file with "-out.png" appended to the name if an output file name is not provided (overwriting current if exists).
