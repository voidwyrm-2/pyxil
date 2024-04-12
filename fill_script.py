'''
A fill tool script writen by Chat-GPT 3.5
because I really didn't want to make one myself
I've had to fix some things, but otherwise it's the same as the one ChatGPT made
'''

def fill(image, x, y, target_color, fill_color):
    '''
    Flood fill algorithm(written by Chat-GPT 3.5) to fill a connected region with a new color.
    '''
    if image[x][y] != target_color:
        return
    
    image[x][y] = fill_color
    
    # Check neighboring pixels
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(image) and 0 <= ny < len(image[0]):
            fill(image, nx, ny, target_color, fill_color)

# Example usage:
image = {
    0: {0: (255, 255, 255), 1: (255, 0, 0)},
    1: {0: (255, 0, 0), 1: (255, 255, 255)},
    2: {0: (255, 255, 255), 1: (255, 255, 255)}
}

target_color = (255, 255, 255)  # Color to replace
fill_color = (0, 0, 0)          # New fill color
x, y = 1, 1                     # Starting point

fill(image, x, y, target_color, fill_color)

# Print the modified image
for row in image.values():
    for pixel in row.values():
        print(pixel, end=' ')
    print()
