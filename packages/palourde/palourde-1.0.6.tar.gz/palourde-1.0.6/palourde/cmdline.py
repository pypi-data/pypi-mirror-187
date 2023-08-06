import json
import pathlib
import sys

import dacite

from palourde.classes import Collection


def flatten(root: dict, out: list, dirs: list[str]) -> None:
    """
    Flatten the root dict into a list of requests with a recursive exploration
    :param root: The postman collection
    :param out: The list of request
    :param dirs: The list of folders and subfolders
    :return: None
    """
    for data in root.get("item"):
        if data.get("request") is None:
            dirs.clear()
            dirs.append(data.get("name"))
            flatten(data, out, dirs)
        else:
            joined_dirs = " > ".join(dirs)
            data["name"] = f"{joined_dirs} > {data.get('name')}"
            out.append(data)


def execute():
    postman_collection = sys.argv[1].strip()

    doc = pathlib.Path(postman_collection)
    with open(doc, 'r+') as json_coll:
        decoded = json.load(json_coll)
        items = []
        flatten(decoded, items, [])
        # Flatten the requests, ignoring the folder structure
        decoded["item"] = items

    collection = dacite.from_dict(data_class=Collection, data=decoded)
    collection.to_markdown()


if __name__ == '__main__':
    execute()
