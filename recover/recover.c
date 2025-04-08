#include <stdio.h>
#include <stdlib.h>
#include <stdint.h> // for uint8_t

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2) // should accept exactly one command-line argument, the name of a forensic image from which to recover JPEGs
    {
        printf("Usage: ./recover card.raw"); // If your program is not executed with exactly one command-line argument, it should remind the user of correct usage, and main should return 1
        return 1;
    }

    FILE *input_file = fopen(argv[1], "r"); // open file

    if (input_file == NULL) // If the forensic image cannot be opened for reading, your program should inform the user as much, and main should return 1
    {
        printf("Error: Cannot open file");
        return 2;
    }

    unsigned char buffer[512];
    int count_image = 0;
    FILE *output_file = NULL;
    char *filename = malloc(8 * sizeof(char)); // Your program, if it uses malloc, must not leak any memory.

    while (fread(buffer, sizeof(char), 512, input_file) != 0) // The files you generate should each be named ###.jpg, where ### is a three-digit decimal number, starting with 000 for the first image and counting up
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //write jpeg into file name in form 001.jpg, 002.jpg and so on
            sprintf(filename, "%03i.jpg", count_image);

            //open filename for writing
            output_file = fopen(filename, "w");

            //count number of image found
            count_image++;
        }

        if (output_file != NULL)
        {
            fwrite(buffer, sizeof(char), 512, output_file);
        }
    }
    free(filename); // Your program, if it uses malloc, must not leak any memory.
    fclose(output_file);
    fclose(input_file);

    return 0;
}
