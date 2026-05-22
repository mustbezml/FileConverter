import json
import xml.etree.ElementTree as ET

from logging import Logger
from pathlib import Path

from .Storages import *

logger = Logger("Converter")

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
        root_name, root_values = list(self.xml_storage.classes.items())[0]
        root = ET.Element(root_name)

        if "Attributes" in root_values:
            for atr in root_values["Attributes"]:
                name = ET.SubElement(root, atr["name"])
                name.text = atr["type"]

        for aggregation in self.xml_storage.aggregations:
            if aggregation["target"] == root_name:
                target_root = root
            else:
                target_root = root.find(aggregation["target"])
            source_name = aggregation["source"]
            element = self.xml_storage.classes[source_name]
            
            new_element = ET.SubElement(target_root, source_name)

            if "Attributes" in element:
                for atr in element["Attributes"]:
                    name = ET.SubElement(new_element, atr["name"])
                    name.text = atr["type"]

        ET.indent(root, space="    ")

        tree = ET.ElementTree(root)
        tree.write(file, encoding='utf-8', xml_declaration=True, short_empty_elements=False)