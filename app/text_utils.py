def get_rose_word_form(number: int) -> str:
    if number % 10 == 1 and number % 100 != 11:
        return "роза"
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return "розы"
    else:
        return "роз"

def get_peonies_word_form(number: int) -> str:
    if number == 0:
        return "пионов"
    if number % 10 == 1 and number % 100 != 11:
        return "пион"
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return "пиона"
    else:
        return "пионов"