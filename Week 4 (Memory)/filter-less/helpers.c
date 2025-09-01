#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green, and blue
            int average =
                round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            // Update pixel values
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute sepia values
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen +
                                 .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen +
                                   .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen +
                                  .131 * image[i][j].rgbtBlue);
            sepiaRed = fmin(sepiaRed, 255);
            sepiaGreen = fmin(sepiaGreen, 255);
            sepiaBlue = fmin(sepiaBlue, 255);
            // Update pixel with sepia values
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++) // row
    {
        for (int j = 0; j < width / 2; j++) // each half of the pixel individually
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    // Loop over all pixels
    for (int i = 0; i < height; i++) // row
    {
        for (int j = 0; j < width; j++) // each pixel individually
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++) // row
    {
        for (int j = 0; j < width; j++) // each pixel individually
        {
            int total_red, total_green, total_blue, counter;
            total_red = total_green = total_blue = counter = 0;
            for (int di = (i - 1); di <= (i + 1); di++)
            {
                for (int dj = (j - 1); dj <= (j + 1); dj++)
                {
                    if ((di >= 0 && di <= height - 1) && (dj >= 0 && dj <= width - 1))
                    {
                        total_red += copy[di][dj].rgbtRed;
                        total_green += copy[di][dj].rgbtGreen;
                        total_blue += copy[di][dj].rgbtBlue;
                        counter++;
                    }
                }
            }
            image[i][j].rgbtRed = (int) round((double) total_red / (double) counter);
            image[i][j].rgbtGreen = (int) round((double) total_green / (double) counter);
            image[i][j].rgbtBlue = (int) round((double) total_blue / (double) counter);
        }
    }
    return;
}
