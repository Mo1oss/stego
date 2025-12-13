# Import function to hide a message inside a BMP image
from encoding import hide_message_in_bmp

# Import function to extract a hidden message from a BMP image
from decoding import extract_message_from_bmp

# Define the main program that controls the menu and user interaction
def main():
    # Print the main title for the program
    print("\n=== BMP Image Steganography ===")
    # Menu option to hide a message
    print("1. Hide message in image")
    # Menu option to extract a message
    print("2. Extract message from image")
    # Menu option to exit
    print("3. Exit")

    # Read the user's menu choice
    choice = input("\nEnter choice (1-3): ").strip()

    # If the user chooses to hide a message
    if choice == '1':
        # Ask for the input BMP image path
        input_bmp_image = input("Enter input BMP image path: ").strip()
        # Ask where to save the output BMP image
        output_bmp_image = input("Enter output BMP image path: ").strip()
        # Present message input options
        print("\nEnter message to hide:")
        print("1. Type message")
        print("2. Read from file")
        # Read choice for message input method
        msg_choice = input("Choice (1-2): ").strip()

        # If user wants to type a message manually
        if msg_choice == '1':
            message = input("Enter your secret message: ")

        # If user wants to load a message from a file
        elif msg_choice == '2':
            file_input = input("Enter file path: ").strip()
            try:
                # Open and read the message from the file
                with open(file_input, 'r', encoding='utf-8') as file:
                    message = file.read()
            except Exception as error:
                # Print any file-reading error
                print(f"Error reading file: {error}")
                return
        else:
            # Invalid message input option
            print("Invalid choice")
            return

        # Call the function to hide the message inside the BMP image
        hide_message_in_bmp(input_bmp_image, message, output_bmp_image)

    # If the user chooses to extract a message
    elif choice == '2':
        # Ask for the BMP image that contains a hidden message
        output_bmp_image = input("Enter BMP image path (with hidden message): ").strip()
        # Extract the hidden message
        message = extract_message_from_bmp(output_bmp_image)

        # If extraction succeeded and message is found
        if message:
            print("\n--- Hidden Message ---")
            print(message)
            print("----------------------")
            # Ask user if they want to save the message into a file
            save = input("\nSave to file? (y/n): ").strip().lower()

            # If yes, ask for file path
            if save == 'y':
                output_file = input("Enter output file path: ").strip()
                try:
                    # Write the message into the file
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(message)
                    print(f"Message saved to {output_file}")
                except Exception as error:
                    # Print any file-writing error
                    print(f"Error saving file: {error}")

    # If the user chooses to exit
    elif choice == '3':
        print("Exiting...")
        return

    # If the user enters a menu option outside 1–3
    else:
        print("Invalid choice")
