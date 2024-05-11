
async def rebuild_phone_number(number: str) -> str:
    if number[0] == "+":
        if number[1] == "8":
            return "+7" + number[2:]
        return number
    if number[0] == "8":
        return "+7" + number[1:]
    return number
