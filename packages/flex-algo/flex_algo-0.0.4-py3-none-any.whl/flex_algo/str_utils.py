def length_of_longest_substring(s):
    seen = {}
    left = 0
    longest = 0

    for right in range(len(s)):
        current_char = s[right]
        prev_seen_pos = seen.get(current_char)

        if prev_seen_pos is not None and prev_seen_pos >= left:
            left = prev_seen_pos + 1

        seen[current_char] = right
        longest = max(longest, right - left + 1)

    return longest


def backspace_compare(s, t):
    p1 = len(s) - 1
    p2 = len(t) - 1

    while p1 >= 0 or p2 >= 0:
        if s[p1] == '#':
            back_count = 2

            while back_count > 0:
                p1 -= 1
                back_count -= 1

                if p1 >= 0 and s[p1] == '#':
                    back_count += 2

        if t[p2] == '#':
            back_count = 2

            while back_count > 0:
                p2 -= 1
                back_count -= 1

                if p2 >= 0 and t[p2] == '#':
                    back_count += 2

        if s[p1] != t[p2]:
            return False

        p1 -= 1
        p2 -= 1

    return True


if __name__ == '__main__':
    ss = "abcabcbb"
    longest = length_of_longest_substring(ss)
    print(longest)

    s, t = "ab#c", "ad#c"
    equal = backspace_compare(s, t)
    print(equal)

    s2, t2 = "ab##", "c#d#"
    equal2 = backspace_compare(s2, t2)
    print(equal2)

    s3, t3 = "a#c", "b"
    equal3 = backspace_compare(s3, t3)
    print(equal3)
