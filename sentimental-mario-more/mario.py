# Get height between 1 and 8
# Print space by taking the height -1 then decrease spaces printed each time
# Print '#'s on left side
# 2 spaces in middle between left and right
# Print '#'s on right side
# make sure you include a new line

from cs50 import get_int

def main():
    height = get_height()
    for row in range(height):
        for space in range(height - row - 1):
            print(" ", end="")
        for hash in range(row + 1):
            print("#", end="")
        print("  ", end="")
        for rhash in range(row + 1):
            print("#", end="")
        print()


def get_height():
    while True:
        try:
            n = int(input("Height: "))
            if n < 1 or n > 8:
                print("This number needs to be between 1 and 8")
            elif n > 0:
                break
        except ValueError:
            print("That's not an integer!")
    return n


main()
