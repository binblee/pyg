def binary_search(ordered_list, target):
    low = 0
    high = len(ordered_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if ordered_list[mid] == target:
            return mid
        elif ordered_list[mid] > target:
            high = mid - 1
        else:
            low = mid + 1
    return -1


def bs_contains(ordered_list, target):
    low = 0
    high = len(ordered_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if ordered_list[mid] == target:
            return mid
        elif ordered_list[mid] > target:
            high = mid - 1
        else:
            low = mid + 1
    return -(low+1)


def bs_insert(ordered_list: list, target):
    index = bs_contains(ordered_list, target)
    if index < 0:
        ordered_list.insert(-(index+1), target)
        index = bs_contains(ordered_list, target)
    return index


if __name__ == '__main__':
    arr1 = [1, 2, 5, 6, 10]
    for target in arr1:
        index = binary_search(arr1, target)
        print(f'binary search, list {arr1} target {target} index {index}')
        non_exist = target - 0.1
        index = binary_search(arr1, non_exist)
        print(f'binary search, list {arr1} target {non_exist} index {index}')
        non_exist = target + 0.1
        index = binary_search(arr1, non_exist)
        print(f'binary search, list {arr1} target {non_exist} index {index}')
    for target in tuple(arr1):
        index = bs_insert(arr1, target)
        print(f'bs insert, list {arr1} target {target} index {index}')
        non_exist = target - 0.1
        index = bs_insert(arr1, non_exist)
        print(f'bs insert, list {arr1} target {non_exist} index {index}')
        non_exist = target + 0.1
        index = bs_insert(arr1, non_exist)
        print(f'binary search, list {arr1} target {non_exist} index {index}')
