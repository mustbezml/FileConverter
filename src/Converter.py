import json
import xml.etree.ElementTree as ET

from logging import Logger
from pathlib import Path

from .Storages import *

logger = Logger("Converter")

class FileConverter:
    def __init__(self, config="./input/config.json", patched_config="./input/patched_config.json"):
        self.xml_storage = XMLStorage()
        self.config = JSONStorage(config)
        self.patched_config = JSONStorage(patched_config)

        self.xml_storage.disassemble_xml()

        if not self.xml_storage.classes or not self.xml_storage.aggregations:
            logger.warning("Storage data is empty. It may cause unexpected problems")

    def _open_file(self, path):
        file = Path(path)
        file.touch(exist_ok=True)

        return file
    
    def convert(self):
        self.create_config()
        self.config.create_deltas(self.patched_config)
        self.config.create_res_patched("./output/delta.json")
        self.create_meta()

    def create_meta(self, output_file="output/meta.json", config_path="output/config.xml"):
        aggregations = self.xml_storage.aggregations[::-1]
        aggregations.append({"source": "BTS", "target": None})
        classes = self.xml_storage.classes

        result = []
        root = self.xml_storage.open_xml(config_path)

        for aggr in aggregations:
            class_name = aggr["source"]
            current_class = classes[class_name]

            class_data = {
                "class": class_name,
                "documentation": current_class["documentation"],
                "isRoot": current_class["isRoot"] == "true",
                
            }

            if "sourceMultiplicity" in aggr:
                amplittude = aggr["sourceMultiplicity"].split('..')
                class_data["max"] = amplittude[1] if len(amplittude) > 1 else amplittude[0]
                class_data["min"] = amplittude[0]


            children = [{"name": n["source"], "type": "class"} for n in aggregations if n["target"] == class_name]
            
            if "Attributes" in current_class:
                attributes = [{"name": n, "type": t} for n, t in current_class["Attributes"]]
            else:
                attributes = []

            class_data["parameters"] = [*children, *attributes]
            result.append(class_data)

        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)

    def create_config(self, output_file="output/config.xml"):
        file = self._open_file(output_file)
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
        logger.info(f"File {output_file} created...")