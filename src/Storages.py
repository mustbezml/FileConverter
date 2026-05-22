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

class JSONStorage:
    def __init__(self, file):
        self.file = file
        self.params = {}
        self.added_params = {}
        self.is_patched = False

        with open(file, 'r') as f:
            json_data: dict = json.load(f)
        
        for k, v in json_data.items():
            if k.startswith("added"):
                self.added_params[k] = v
            else:
                self.params[k] = v

        self.is_patched = len(self.added_params) > 0

    def find_deletions(self, patched_storage):
        config_params = set(self.params.keys())
        patched_params = set(patched_storage.params.keys())
        
        return list(set.symmetric_difference(config_params, patched_params))
    
    def form_updates(self, patched_storage):
        result = []
        for param, value in self.params.items():
            if param in patched_storage.params and value != patched_storage.params[param]:
                result.append(
                    {
                        "key": param,
                        "from": value,
                        "to": patched_storage.params[param]
                    }
                )
        return result


