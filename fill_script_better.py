'''
A fill tool script writen by Chat-GPT 3.5 that's a better version of the other one
because, again, I really didn't want to make one myself
I actually didn't need to do anything to this one!
'''

def flood_fill(image, start_x, start_y, new_color):
    stack = [(start_x, start_y)]
    original_color = image[start_x][start_y]
    if original_color == new_color:
        return  # No need to fill if new_color is the same as original color
    while stack:
        x, y = stack.pop()
        if image[x][y] == original_color:
            image[x][y] = new_color
            if x > 0 and image[x - 1][y] == original_color:
                stack.append((x - 1, y))
            if x < len(image) - 1 and image[x + 1][y] == original_color:
                stack.append((x + 1, y))
            if y > 0 and image[x][y - 1] == original_color:
                stack.append((x, y - 1))
            if y < len(image[0]) - 1 and image[x][y + 1] == original_color:
                stack.append((x, y + 1))

# Example usage:
image = [
    [1, 1, 1, 1, 1],
    [3, 1, 1, 1, 1],
    [1, 3, 1, 1, 1],
    [1, 3, 3, 3, 1],
    [1, 3, 1, 1, 1]
]

flood_fill(image, 2, 2, 2)
for row in image:
    print(row)
