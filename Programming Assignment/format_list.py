#!/usr/bin/env python3
"""Format a list of items so that they are comma separated and "and" appears before the last item.
"""

def format_list(data):
    """Format a list of items so that they are comma separated and "and"
    appears before the last item.

    Args:
        data (list): the list of items to format

    Returns:
        str: A string containing the items from data with nice formatting
    """
    # Handle the case where the list is empty
    if len(data) == 0:
        return "(None)"

    # Start with an empty string that we will add items to
    retval = ""

    sorted_data = sorted(data)
    # Handle all of the items except for the last two
    for i in range(0, len(sorted_data) - 2):
        retval = retval + str(sorted_data[i]) + ", "

    # Handle the second last item
    if len(sorted_data) >= 2:
        retval += str(sorted_data[-2]) + " and "

    # Handle the last item
    retval += str(sorted_data[-1])

    # Return the result
    return retval
print(format_list({'':['l', 'k']}))


# Run some tests if the module has not been imported
if __name__ == "__main__":
    # Test the empty list
    values = []

    print(values, "is formatted as", format_list(values))

    # Test a list containing a single item
    values = [1]
    print(values, "is formatted as", format_list(values))

    # Test a list containing two items
    values = [3, 4]
    print(values, "is formatted as", format_list(values))

    # Test a list containing three items
    values = [-1, -2, -3]
    print(values, "is formatted as", format_list(values))

    # Test a list containing four items
    values = ["Alice", "Bob", "Chad", "Diane"]
    print(values, "is formatted as", format_list(values))

    # Test a list containing lots of items
    values = [3, 1, 4, 1, 5, 9, 2, 6, 5, 9]
    print(values, "is formatted as", format_list(values))
