from yaml import safe_load
from PIL import Image
import requests

def read_yaml(path:str):
    with open(path,mode='r') as file:
        data = safe_load(file)
    return data

def yaml_dot(yaml_after_read:str,query:str) -> str:
    query_list = query.split(".")
    def read_data(data,query_list):
        for i in range(len(query_list)):
            data = data[query_list[i]]
        return data
    return read_data(yaml_after_read,query_list)

def url_to_imagebit(url):
    image = Image.open(requests.get(url, stream=True).raw)
    return image

def imagebit_to_string(img: Image, dest_width: int, unicode: bool = True) -> str:
    img_width, img_height = img.size
    scale = img_width / dest_width
    dest_height = int(img_height / scale)
    dest_height = dest_height + 1 if dest_height % 2 != 0 else dest_height
    img = img.resize((dest_width, dest_height))
    output = ""
    for y in range(0, dest_height, 2):
        for x in range(dest_width):
            if unicode:
                r1, g1, b1 = img.getpixel((x, y))
                r2, g2, b2 = img.getpixel((x, y + 1))
                output = output + f"[rgb({r1},{g1},{b1}) on rgb({r2},{g2},{b2})]▀[/]"
            else:
                r, g, b = img.getpixel((x, y))
                output = output + f"[on rgb({r},{g},{b})] [/]"

        output = output + "\n"
    return output

