from a15lib import iter_numbers

if __name__ == "__main__":
    for i, n in enumerate(iter_numbers(), start=1):
        if i == 2020:
            print(n)
            break
