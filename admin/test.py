def rearrange_list_by_index(lst, index):
    if index < 0 or index >= len(lst):
        return lst  # Return the original list if index is out of bounds

    return lst[index:] + lst[:index]

# Example usage:
my_list = [1, 2, 3, 4, 5, 6, 7]
new_index = 4
result = rearrange_list_by_index(my_list, new_index)
print(result)