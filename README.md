###### \# \*\*Milestone 1 and 2: pseudocode and coding.

###### \# \*\*BMP Image Steganography –

###### \#

###### \# \*\*Introduction to Programming



**Project Overview**



  A Python program is built to hide and extract secret messages in BMP

  images using only basic programming techniques. It applies the  LSB

  method, changing the lowest pixel bits so the image looks the same. The

  program supports 24-bit and 32-bit BMP files, embeds a message, creates a

  modified image, and can fully extract and save the hidden text.



How the Application Works

   - Message Hiding (Encoding)

        The program writes a message by changing the LSB of the pixel bytes.

 

       The details are as follows:

          The file of BMP is opened in binary mode and it is verified for any

          Mistakes by its header details.

          After that, the message is  ready to add the delimiter and

          Turning  it into bits. Then the pixel bytes are adjusted to RGB places.

          At last, every single bit of the message is the LSB of the pixel byte that

          corresponds to it and thus the new BMP image is saved.



\-  Message Extraction (Decoding)

   - Extraction reverses the encoding steps:

          It reads a BMP file, pixel bytes rearranged into RGB positions; the LSB bit is taken from the byte of interest

          and collected until the 8 bits are formed into a character, ending at the predefined ###END### delimiter. The

          message recovered will be returned for viewing and/or saving, excluding the delimiter.







**Why BMP?**



BMP images are uncompressed binary files with a simple structure,

making them ideal for steganography.

Their raw pixel data can be directly accessed and modified without distortion.

Unlike JPEG or PNG, BMP doesn’t use compression,

so changing the Least Significant Bits (LSB) of pixels

doesn’t affect image quality or file integrity.

