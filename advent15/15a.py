from collections import defaultdict

def iter_numbers():
    starter = [9, 12, 1, 4, 17, 0, 18]
    last_seen = defaultdict(list)
    latest = 0
    ct = 0

    while True:
        if starter:
            n, starter = starter[0], starter[1:]
        else:
            n = latest
            seen_list = last_seen[n]
            if len(seen_list) <= 1:
                n = 0
            else:
                n = seen_list[-1] - seen_list[-2]

        last_seen[n].append(ct)
        latest = n
        ct += 1
        yield n

for i, n in enumerate(iter_numbers(), start=1):
    if i == 2020:
        print(n)
        break
