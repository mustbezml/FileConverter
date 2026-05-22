import json
import xml.etree.ElementTree as ET

class XMLStorage:
    def __init__(self, file="input/impulse_test_input.xml"):
        self.classes = {}
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
                class_name = child.attrib.pop("name")
                self.classes[class_name] = child.attrib
            elif child.tag == "Aggregation":
                self.aggregations.append(child.attrib)