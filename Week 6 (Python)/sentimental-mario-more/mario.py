def main(get_int):
    while True:
        height = get_int("Height: ")
        if height is not None and 1 <= height <= 8:
            break

    for row in range(height):
        for spaces in range(height - 1, row, - 1):
            print(" " ,end = "")
        for brick in range(row + 1):
            print("#" ,end = "")
        print("  ", end = "")
        for brick in range(row + 1):
            print("#" ,end = "")
        print()

def get_int(prompt):
    try:
        value = int(input(prompt))
        return value
    except ValueError:
        print("Please enter an integer")





main(get_int)
