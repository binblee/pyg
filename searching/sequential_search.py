def sequential_search(arr, target):
    for index in range(len(arr)):
        if arr[index] == target:
            return index
    return -1


if __name__ == '__main__':
    print(sequential_search((1, 2, 5, 6, 10), 3))
