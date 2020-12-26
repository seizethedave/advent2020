from collections import defaultdict

last_seen = defaultdict(list)
latest = 0
ct = 0

starter = [9, 12, 1, 4, 17, 0, 18]

def next_number():
    global latest, ct, starter

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
    return n


while ct < 2020:
    n = next_number()
print(n)