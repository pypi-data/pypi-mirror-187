'''
Module with functionality for verifying Danish CPR-numbers.
'''

__all__ = ['is_cpr_number',
           'satisfies_mod11',
           'is_leap_year']

_mod11_values = [4, 3, 2, 7, 6, 5, 4, 3, 2, 1]


def is_leap_year(year: int) -> bool:
    '''
    Checks whether a given year is a leap year.
    '''
    if year < 0:
        raise ValueError("Year cannot be negative.")

    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True

    return False


def is_cpr_number(cpr_number: str) -> bool:
    '''
    Checks that the parameter string `cpr_number` has the
    format of a Danish CPR-number: DDMMYY(-)NNNN.
    '''

    if not (10 <= len(cpr_number) <= 11):
        return False

    cpr_number = cpr_number.replace('-', '')

    try:
        day = int(cpr_number[0:2])
        month = int(cpr_number[2:4])
        year = int(cpr_number[4:6])
        int(cpr_number[6:])

        match month:
            case 1 | 3 | 5 | 7 | 8 | 10 | 12:
                return 1 <= day <= 31
            case 4 | 6 | 9 | 11:
                return 1 <= day <= 30
            case 2:
                if is_leap_year(year):
                    return 1 <= day <= 29
                else:
                    return 1 <= day <= 28
    except ValueError:
        return False

    return False


def satisfies_mod11(cpr_number: str) -> bool:
    '''
    Checks that the parameter string `cpr_number` satisfies
    the modulus-11 control condition.
    '''
    if not is_cpr_number(cpr_number):
        return False

    cpr_number = cpr_number.replace('-', '')

    cpr_number_list = map(lambda a: int(a), list(cpr_number))

    return sum([n*v for n, v in zip(cpr_number_list, _mod11_values)]) % 11 == 0
