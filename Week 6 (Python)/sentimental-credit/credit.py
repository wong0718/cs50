def main(get_int):
    while True:
        n = get_int("Number: ")
        if n is not None and n > 0:
            break

    checksum(n)

def get_int(prompt):
    try:
        value = int(input(prompt))
        return value
    except ValueError:
        print("Please enter an integer")

def checksum(number):
    number_copy = number
    total_sum = pos = total_length = 0

    while number != 0:
        if pos % 2 != 0:
            temp = 2 * (number % 10)
            if temp > 9:
                total_sum += (temp % 10 + temp // 10)
            else:
                total_sum += temp
        else:
            total_sum += number % 10
        number = number // 10
        pos += 1
        total_length += 1

    if total_sum % 10 == 0:
        amex_start = number_copy // 10000000000000
        mastercard_start = number_copy // 100000000000000
        visa_start = number_copy // 1000000000000

        if ((amex_start == 34 or amex_start == 37) and total_length == 15):
            print("AMEX\n")

        elif ((51 <= mastercard_start <= 55) and total_length == 16):
            print("MASTERCARD\n")

        elif ((total_length == 13 or total_length == 16) and
                (visa_start == 4 or mastercard_start // 10 == 4)):
            print("VISA\n")

        else:
            print("INVALID\n")
    else:
        print("INVALID\n")




if __name__ == "__main__":
    main(get_int)
