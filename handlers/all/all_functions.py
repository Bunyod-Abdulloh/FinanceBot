from openpyxl import Workbook


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


async def openpyxl_downloader(filename: str, a: str, b: str, rows: str = None, c: str = None):
    wb = Workbook()

    ws = wb.active
    if c:
        ws.append([f'{a}', f'{b}', f'{c}'])
    else:
        ws.append([f'{a}', f'{b}'])

    wb.save(f'{filename}.xlsx')
