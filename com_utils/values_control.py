def find_next_value(arr, keyword):
    for i in range(len(arr)):
        if keyword in arr[i]:
            if i < len(arr) - 1:
                return arr[i + 1]
            else:
                return None
    return None

def find_next_double_value(arr, keyword):
    for i in range(len(arr)):
        if keyword in arr[i]:
            if i < len(arr) - 1:
                return arr[i + 2]
            else:
                return None
    return None