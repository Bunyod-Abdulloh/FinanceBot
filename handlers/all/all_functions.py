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


warning_text = ("Bot ishlashida muammo bo'lmasligi uchun kiritilayotgan matnda <b>', _, -, !, ?</b> kabi belgilardan "
                "foydalanmasligingizni iltimos qilamiz!")