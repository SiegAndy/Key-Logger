import codecs, json
from bs4 import BeautifulSoup


def get_vk_mapping():
    f = codecs.open("data/virtual_key.html", "r", "utf-8")
    document = BeautifulSoup(f.read(), features="html.parser")
    entries = document.find_all("tr")
    virtual_key_mapping = {}
    for entry in entries:
        key_alias, key_code, key_name = entry.find_all("td")
        virtual_key_mapping[key_name.get_text().strip(" key")] = {
            "alias": key_alias.get_text(),
            "virtual_key": key_code.get_text(),
        }

    with open("key_mapping.py", "w", encoding="utf-8") as output:
        output.write(json.dumps(virtual_key_mapping, indent=4))
