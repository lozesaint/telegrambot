def refactor(number):
    number = str(number)
    for x in range(3, len(number), 3):
        number = number[:-x] + " " + number[-x:]

    return number
