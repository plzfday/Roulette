def sort_name(user_list):
    if len(user_list) > 1:
        mid = len(user_list) // 2
        left = user_list[:mid]
        right = user_list[mid:]

        sort_name(left)
        sort_name(right)

        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i]['name'] < right[j]['name']:
                user_list[k] = left[i]
                i += 1
            else:
                user_list[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            user_list[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            user_list[k] = right[j]
            j += 1
            k += 1


def find_user(user_list, key) -> int:
    low = 0
    high = len(user_list) - 1

    while low <= high:
        mid = (low + high) // 2

        if key < user_list[mid]['name']:
            high = mid - 1
        elif key > user_list[mid]['name']:
            low = mid + 1
        else:
            return mid
    return -1
