async def replace_point_bottom_line(message):

    if "'" in message:
        incoming = message.replace("'", "")

    elif "_" in message:
        incoming = message.replace("_", "")

    else:
        incoming = message

    return incoming


async def replace_float(message):

    if "." in message:
        incoming = message.replace(".", "")

    elif "," in message:
        incoming = message.replace(",", "")

    else:
        incoming = message

    return int(incoming)


warning_text = ("Bot ishlashida muammo bo'lmasligi uchun kiritilayotgan matnda _, !, ? kabi belgilardan "
                "foydalanmasligingizni iltimos qilamiz!")


async def next_page_key(history: str, count: int, summary: int, db: list):

    for data in db[:50]:
        count += 1
        summary += data[1]
        history += f"{count}) {data[0]} | {data[1]} so'm\n"
    return history, count, summary
