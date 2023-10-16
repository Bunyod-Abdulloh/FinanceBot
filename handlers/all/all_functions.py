async def replace_point(message):

    if "'" in message:
        incoming = message.replace("'", "")

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

    return incoming
