# Import function to read BMP header and pixel data
from file_operations import read_bmp_header_and_pixels

# Import helper to reorder pixel byte positions from BGR to RGB
from helpers import bgr_to_rgb_reordered

# Define the function that extracts a hidden message from a BMP image
def extract_message_from_bmp(output_bmp_image):
    try:
        # Read BMP header, pixel bytes, pixel start offset, and bits-per-pixel value
        header_bytes, pixel_bytes, pixel_start, bits_per_pixel = read_bmp_header_and_pixels(output_bmp_image)

        # Compute reordered RGB byte positions for consistent pixel traversal
        rgb_reordered = bgr_to_rgb_reordered(len(pixel_bytes), bits_per_pixel)

        # Initialize storage for collected bits
        bits_collected = ""

        # Initialize the variable that will hold the recovered message
        hidden_message = ""

        # Loop through each reordered pixel byte position
        for byte_position in rgb_reordered:

            # Collect the least significant bit of the current pixel byte
            bits_collected += str(pixel_bytes[byte_position] & 1)

            # If 8 bits are collected, convert them into one character
            if len(bits_collected) == 8:
                # Convert the 8-bit binary string to an ASCII character
                hidden_message += chr(int(bits_collected, 2))

                # Reset the collected bits for the next character
                bits_collected = ""

                # Check whether the hidden message ends with the delimiter
                if hidden_message.endswith("###END###"):
                    # Remove the delimiter to retrieve the real message
                    message = hidden_message[:-9]

                    # Print the number of extracted characters
                    print(f"Message extracted successfully: {len(message)} characters")

                    # Print the BMP bit depth
                    print(f"BMP bits-per-pixel: {bits_per_pixel}")

                    # Return the extracted message
                    return message

        # If no delimiter was found, then message does not exist or is damaged
        print("No hidden message found or message corrupted")

        # Return None to indicate failure to extract
        return None

    except Exception as error:
        # Print the error encountered during extraction
        print(f"Error extracting message: {error}")

        # Return None on exception
        return None

