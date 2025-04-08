#include <math.h>

#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // need to go through each row to check each pixel [height][width]
    int average;
    for (int h = 0; h < height; h++) // height
    {
        for (int w = 0; w < width; w++) // width
        {
            // calculate pixels in image
            int blue = image[h][w].rgbtBlue;
            int green = image[h][w].rgbtGreen;
            int red = image[h][w].rgbtRed;
            average = round(((float)blue + (float)red + (float)green) / 3); // average those pixels to match darkness/lightness - needs to be a whole value (int)
            // make rgb all the same
            image[h][w].rgbtBlue = average;
            image[h][w].rgbtGreen = average;
            image[h][w].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaBlue, sepiaGreen, sepiaRed, originalBlue, originalGreen, originalRed;
    // similar to greyscale first go through height and width
    for (int h = 0; h < height; h++) //height
    {
        for (int w = 0; w < width; w++) //width
        {
            // set original amounts of rbg
            originalBlue = image[h][w].rgbtBlue;
            originalGreen = image[h][w].rgbtGreen;
            originalRed = image[h][w].rgbtRed;

            sepiaBlue = round(0.272 * originalRed + 0.534 * originalGreen + 0.131 * originalBlue); //calculate new colour for blue and implement
            if (sepiaBlue > 255) //cannot go above 255 - need to put a cap on it
            {
                image[h][w].rgbtBlue = 255;
            }
            else
            {
                image[h][w].rgbtBlue = sepiaBlue;
            }

            sepiaGreen = round(0.349 * originalRed + 0.686 * originalGreen + 0.168 * originalBlue); // calculate new colour for green and implement
            if (sepiaGreen > 255) //cannot go above 255 - need to put a cap on it
            {
                image[h][w].rgbtGreen = 255;
            }
            else
            {
                image[h][w].rgbtGreen = sepiaGreen;
            }

            sepiaRed = round(0.393 * originalRed + 0.769 * originalGreen + 0.189 * originalBlue); // calculate new colour for red and implement
            if (sepiaRed > 255) //cannot go above 255 - need to put a cap on it
            {
                image[h][w].rgbtRed = 255;
            }
            else
            {
                image[h][w].rgbtRed = sepiaRed;
            }
        }
    }
    return;
}

// Reflect image horizontally
// rows stay in the same order but the pixels switch places
// use a loop
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++) //height stays the same
    {
        for (int w = 0; w < (width / 2); w++) //half the width to flip, ie you would half the height to turn the image upsidedown
        {
            // need to rearrange the pixels - assign memory (temp)
            int tempBlue = image[h][w].rgbtBlue;
            int tempGreen = image[h][w].rgbtGreen;
            int tempRed = image[h][w].rgbtRed;

            // now swap
            image[h][w].rgbtBlue = image[h][width - w - 1].rgbtBlue;
            image[h][w].rgbtGreen = image[h][width - w - 1].rgbtGreen;
            image[h][w].rgbtRed = image[h][width - w - 1].rgbtRed;

            image[h][width - w - 1].rgbtBlue = tempBlue;
            image[h][width - w - 1].rgbtGreen = tempGreen;
            image[h][width - w - 1].rgbtRed = tempRed;
        }
    }
    return;
}

// Blur image - box blur
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // new pixel value = avg of 9 pixels around the OG pixel (within 1 row and 1 column)
    RGBTRIPLE copy[height][width]; // temp image

    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            int totalBLUE, totalGREEN, totalRED;
            totalBLUE = totalGREEN = totalRED = 0;
            float counter = 0.00;

            // surrounding pixels
            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    int currentX = h + x;
                    int currentY = w + y;

                    if (currentX < 0 || currentX > (height - 1) || currentY < 0 || currentY > (width - 1)) //check if valid
                    {
                        continue;
                    }
                    // get image
                    totalBLUE += image[currentX][currentY].rgbtBlue;
                    totalGREEN += image[currentX][currentY].rgbtGreen;
                    totalRED += image[currentX][currentY].rgbtRed;

                    counter++;
                }
                // average of surrounding cells
                copy[h][w].rgbtBlue = round(totalBLUE / counter);
                copy[h][w].rgbtGreen = round(totalGREEN / counter);
                copy[h][w].rgbtRed = round(totalRED / counter);
            }
        }
    }
    // copy blurred image to OG
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            image[h][w].rgbtBlue = copy[h][w].rgbtBlue;
            image[h][w].rgbtGreen = copy[h][w].rgbtGreen;
            image[h][w].rgbtRed = copy[h][w].rgbtRed;
        }
    }
    return;
}