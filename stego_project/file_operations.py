# Define a function to read the BMP header and its pixel data
def read_bmp_header_and_pixels(input_bmp_image):

    # Open the BMP file in binary read mode
    with open(input_bmp_image, 'rb') as bmp_file:

        # Read the first 54 bytes, which contain the BMP header
        header_54 = bmp_file.read(54)

        # Check if the file starts with the 'BM' signature (valid BMP)
        if header_54[0:2] != b'BM':
           raise ValueError("Not a valid BMP file")

        # Read the pixel start offset from bytes 10–13
        pixel_start = int.from_bytes(header_54[10:14], 'little')

        # Read the bits-per-pixel value from bytes 28–29
        bits_per_pixel = int.from_bytes(header_54[28:30], 'little')

        # Go back to the beginning of the file to read the full header section
        bmp_file.seek(0)

        # Read the entire header up to the pixel data
        header_bytes = bmp_file.read(pixel_start)

        # Read all remaining bytes (the pixel data)
        pixel_bytes = bytearray(bmp_file.read())

    # Return header, pixel data, pixel offset, and bit depth
    return header_bytes, pixel_bytes, pixel_start, bits_per_pixel


# Define a function that writes header and modified pixels into a BMP output file
def write_bmp_header_and_pixels(output_bmp_image, header_bytes, pixels_modified):

    # Open the output BMP file in binary write mode
    with open(output_bmp_image, 'wb') as bmp_file:

        # Write the header bytes (unchanged from input)
        bmp_file.write(header_bytes)

        # Write the modified pixel data containing the hidden message
        bmp_file.write(pixels_modified)
