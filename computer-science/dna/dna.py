import csv
import sys


def main():
    if len(sys.argv) != 3:  # Check for command-line usage
        print("Error, incorrect command-line argument")  # print error message
        sys.exit(1)  # exit

    # Read database file into a variable
    with open(sys.argv[1], 'r') as csv_file:  # open the CSV file and read its contents into memory
        reader = csv.DictReader(csv_file)
        dna_database = list(reader)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], 'r') as text_file:
        sequence = text_file.read()

    # Find longest match of each STR in DNA sequence
    matches = {}

    for i in dna_database[0]:  # first row is headers
        matches[i] = (longest_match(sequence, i))  # uses helper function 'def longest_match()'

    # TODO: Check database for matching profiles
    profile = "No match"
    profile_counter = 1

    for i in range(len(dna_database)):
        for j in matches:
            if str(matches[j]) == dna_database[i][j]:
                profile_counter += 1
        if profile_counter == len(matches):
            profile = dna_database[i]["name"]  # takes information from database
            break
        else:
            profile_counter = 1

    print(profile)  # if match is found prints name, if not prints no match

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()