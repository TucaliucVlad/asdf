# factorial.py: Contains the core logic for calculating factorial using recursion

def factorial(n):
    """
    Recursive function to calculate the factorial of a non-negative integer n.
    
    Args:
    n (int): A non-negative integer.
    
    Returns:
    int: The factorial of n.
    
    Raises:
    ValueError: If n is negative (though primary handling is in main.py).
    """
    if n == 0:
        return 1  # Base case: 0! = 1
    elif n > 0:
        return n * factorial(n - 1)  # Recursive case
    else:
        raise ValueError("n must be a non-negative integer")  # Safety check, though handled in main.py