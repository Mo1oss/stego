# Import the main function that handles user interaction and steganography operations
from input_handling import main

# Ensure this block only runs when the script is executed directly
if __name__ == "__main__":
    # Start an infinite loop to allow repeated program execution
    while True:
        try:
            # Call the main function to run the program menu
            main()

            # Ask the user if they want to continue running the program
            cont = input("\nContinue? (y/n): ").strip().lower()

            # If the user chooses anything other than 'y', exit the loop
            if cont != 'y':
                print("Goodbye!")
                break

        # Handle Ctrl+C (KeyboardInterrupt) gracefully
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
