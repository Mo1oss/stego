# Import functions to read and write BMP headers and pixel data
from file_operations import read_bmp_header_and_pixels, write_bmp_header_and_pixels

# Import helpers for converting a message to bits and embedding those bits into pixels
from helpers import message_to_bits, hide_bits_in_pixels

# Define the function that hides a message inside a BMP image
def hide_message_in_bmp(input_bmp_image, message, output_bmp_image):
    try:
        # Read header bytes, pixel bytes, pixel start offset, and bit depth from the input BMP
        header_bytes, pixel_bytes, pixel_start, bits_per_pixel = read_bmp_header_and_pixels(input_bmp_image)

        # Append the delimiter to mark the end of the hidden message
        message_with_delimiter = message + "###END###"

        # Convert the message plus delimiter into a sequence of bits
        message_bits = message_to_bits(message_with_delimiter)

        # Embed the message bits into the pixel bytes based on the bit depth
        pixels_modified = hide_bits_in_pixels(pixel_bytes, message_bits, bits_per_pixel)

        # Write the new BMP file with the modified pixel data
        write_bmp_header_and_pixels(output_bmp_image, header_bytes, pixels_modified)

        # Print confirmation that the message was successfully hidden
        print(f"Message hidden successfully in {output_bmp_image}")

        # Print the message length in characters and bits
        print(f"Message length: {len(message)} characters ({len(message_bits)} bits)")

        # Print the BMP's bits-per-pixel value
        print(f"BMP bits-per-pixel: {bits_per_pixel}")

    except Exception as error:
        # Print any errors that occur during the hiding process
        print(f"Error hiding message: {error}") 
