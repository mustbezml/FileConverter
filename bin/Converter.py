import json
import xml.etree.ElementTree as ET

from logging import Logger
from pathlib import Path

logger = Logger("Converter")

class XMLStorage:
    def __init__(self, file="input/impulse_test_input.xml"):
        self.classes = []
        self.aggregations = []
        self.file = file

    def disassemble_xml(self):
        tree = ET.parse(self.file)
        root = tree.getroot()

        # Нужно будет переделать
        for child in root:
            if len(child) > 0:
                child.attrib["Attributes"] = [atr.attrib for atr in child]

            if child.tag == "Class":
                self.classes.append(child.attrib)
            elif child.tag == "Aggregation":
                self.aggregations.append(child.attrib)


class FileConverter:
    def __init__(self):
        self.xml_storage = XMLStorage()
        self.xml_storage.disassemble_xml()
        if not self.xml_storage.classes or not self.xml_storage.aggregations:
            logger.warning("Storage data is empty. It may cause unexpected problems")

    def _open_file(self, path):
        file = Path(path)
        file.touch(exist_ok=True)

        return file

    def create_config(self):
        file = self._open_file("output/config.xml")

        root = ET.Element(self.xml_storage.classes[0]["name"])
        if "Attributes" in self.xml_storage.classes[0]:
            for atr in self.xml_storage.classes[0]["Attributes"]:
                name = ET.SubElement(root, atr["name"])
                name.text = atr["type"]


        tree = ET.ElementTree(root)
        tree.write(file, encoding='utf-8', xml_declaration=True, short_empty_elements=False)

