###### \# \*\*Milestone 1and 2: pseudocode and coding.

###### \# \*\*BMP Image Steganography –

###### \# 

###### \# \*\*Introduction to Programming



**Project Overview**



&nbsp; A Python program is built to hide and extract secret messages in BMP   

&nbsp; images using only basic programming techniques. It applies the  LSB   

&nbsp; method, changing the lowest pixel bits so the image looks the same. The  

&nbsp; program supports 24-bit and 32-bit BMP files, embeds a message, creates a  

&nbsp; modified image, and can fully extract and save the hidden text.



How the Application Works

&nbsp;  - Message Hiding (Encoding)

&nbsp;       The program writes a message by changing the LSB of the pixel bytes.

&nbsp;            

&nbsp;      The details are as follows:

&nbsp;         The file of BMP is opened in binary mode and it is verified for any           

&nbsp;         Mistakes by its header details.

&nbsp;         After that, the message is  ready to add the delimiter and 

&nbsp;         Turning  it into bits. Then the pixel bytes are adjusted to RGB places.

&nbsp;         At last, every single bit of the message is the LSB of the pixel byte that  

&nbsp;         corresponds to it and thus the new BMP image is saved.



\-  Message Extraction (Decoding)

&nbsp;  - Extraction reverses the encoding steps:

&nbsp;         It reads a BMP file, pixel bytes rearranged into RGB positions; the LSB bit is taken from the byte of interest           

&nbsp;         and collected until the 8 bits are formed into a character, ending at the predefined ###END### delimiter. The  

&nbsp;         message recovered will be returned for viewing and/or saving, excluding the delimiter.







**Why BMP?**



BMP images are uncompressed binary files with a simple structure,

making them ideal for steganography.

Their raw pixel data can be directly accessed and modified without distortion.

Unlike JPEG or PNG, BMP doesn’t use compression,

so changing the Least Significant Bits (LSB) of pixels

doesn’t affect image quality or file integrity.

