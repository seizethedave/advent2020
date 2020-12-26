from collections import defaultdict

def iter_numbers():
    starter = [9, 12, 1, 4, 17, 0, 18]
    last_seen = defaultdict(list)
    ct = 0

    while True:
        if starter:
            n, starter = starter[0], starter[1:]
        else:
            seen_list = last_seen[n]
            try:
                n = seen_list[-1] - seen_list[-2]
            except IndexError:
                n = 0

        last_seen[n].append(ct)
        ct += 1
        yield n