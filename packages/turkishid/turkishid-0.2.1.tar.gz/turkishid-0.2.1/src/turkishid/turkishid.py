def digit(c: str) -> int:
    """
    Returns the integer value of the given digit.
    If the given character is not a digit, returns -1.
    """
    try:
        d = int(c)
        if d < 0 or d > 9:
            return -1
        return d
    except ValueError:
        return -1


def compute_final_checksum(odd_sum: int, even_sum: int, first_checksum: int) -> int:
    """
    Computes the final checksum of the national identification number based on the sums and the first checksum.
    """
    computed_final = (odd_sum + even_sum + first_checksum) % 10
    return computed_final


def compute_first_digit(odd_sum: int, even_sum: int) -> int:
    """
    Computes the first digit of the national identification number based on the odd and even sums.
    """
    first = (odd_sum * 7 - even_sum) % 10
    if first < 0:
        first += 10
    return first


def validate_id(national_identification_number: int) -> bool:
    """
    Validates the given national identification number.
    Returns True if the number is valid, False otherwise.
    """
    if len(str(national_identification_number)) != 11:
        return False
    invalid = False
    odd_sum = digit(str(national_identification_number)[0])
    if odd_sum == -1:
        return False
    even_sum = 0
    for i in range(1, 9, 2):
        even_sum += digit(str(national_identification_number)[i])
        odd_sum += digit(str(national_identification_number)[i + 1])
    first_checksum = digit(str(national_identification_number)[9])
    final_checksum = digit(str(national_identification_number)[10])
    if odd_sum == -1 or even_sum == -1 or first_checksum == -1 or final_checksum == -1:
        return False
    computed_final = compute_final_checksum(odd_sum, even_sum, first_checksum)
    if final_checksum != computed_final:
        return False
    first = compute_first_digit(odd_sum, even_sum)
    return first_checksum == first
