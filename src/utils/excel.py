import os

from openpyxl import Workbook

from classes.post import Post


def write_excel(file_name: str, data: list[Post]):
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Twitter Posts"

        ws.append(["Usuario", "Cuenta", "Fecha", "Hora", "URL", "Text", "Links", "Likes", "Replies", "Reposts", "Views"])
        for post in data:
            ws.append([post.username, post.account, post.date.date(), post.date.time(), post.url, post.text, ", ".join(post.links), post.likes, post.replies, post.reposts, post.views])
        
        wb.save(file_name)
        wb.close()
    except Exception:
        raise Exception("Error: No se pudo crear el archivo en Excel")
    
def delete_excel(file_name: str):
    try:
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            print("Error: No se pudo encontrar el archivo en Excel")
    except Exception:
        raise Exception("Error: No se pudo eliminar el archivo en Excel")
    