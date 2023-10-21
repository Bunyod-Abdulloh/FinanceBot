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


async def next_history_page(history: list):
    PAGE_COUNT = 50
    h = " "
    c = 0
    s = 0
    for data in history[:PAGE_COUNT]:
        c += 1
        s += data[1]
        h += f"{c}) {data[0]} | {data[1]} so'm\n"
    return h, s
