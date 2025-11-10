###### \# BMP Image Steganography – KH4017CMD

###### Author: Mohamed Osama

###### Module: KH4017CMD – Introduction to Programming

###### 

###### Milestone 1: Plan the logic and pseudocode before coding.







Project Overview

This Python program hides and extracts secret messages within BMP images

using the Least Significant Bit (LSB) technique.

It reads the BMP header, modifies pixel data, and adds an end marker "###END###" 

to identify where the hidden message stops



Why BMP?

BMP images are uncompressed and have a simple structure, making them ideal for steganography.

Their raw pixel data can be easily accessed and modified without distortion.

Unlike JPEG or PNG, BMP doesn’t use compression, 

so changing the Least Significant Bits (LSB) of pixels doesn’t damage the image quality or file integrity.



