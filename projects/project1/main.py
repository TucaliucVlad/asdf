# main.py: CLI entrypoint for the factorial calculator

import sys
from factorial import factorial  # Import the factorial function from factorial.py

def main():
    """
    Main function to handle user input, validate it, compute factorial,
    and display the result or error message.
    """
    try:
        # Prompt the user for input as per REQ-001
        user_input = input("Please enter a non-negative integer to calculate its factorial: ")
        
        # Convert input to integer as per REQ-004 (handle non-integer errors)
        n = int(user_input)
        
        # Check for negative numbers as per REQ-003
        if n < 0:
            print("Error: Input must be a non-negative integer.")
            sys.exit(1)  # Exit gracefully
        
        # Calculate factorial using the recursive function as per REQ-002
        result = factorial(n)
        
        # Format and display the output clearly as per REQ-005
        print(f"The factorial of {n} is {result}.")
    
    except ValueError:
        # Handle non-integer inputs
        print("Error: Input must be an integer.")
        sys.exit(1)  # Exit gracefully

if __name__ == "__main__":
    main()  # Run the main function when the script is executed