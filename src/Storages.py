import json
import xml.etree.ElementTree as ET

from logging import Logger

logger = Logger("Storages")

class XMLStorage:
    def __init__(self, file="input/impulse_test_input.xml"):
        self.classes = {}
        self.aggregations = []
        self.file = file

    def open_xml(self, file):
        tree = ET.parse(file)
        return tree.getroot()

    def disassemble_xml(self):
        root = self.open_xml(self.file)

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

    def form_added(self, patched_storage):
        result = []
        for k, v in patched_storage.added_params.items():
            result.append(
                {
                    "key": k,
                    'value': v
                }
            )
        
        return result

    def form_deletions(self, patched_storage):
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

    def create_deltas(self, patched_storage, output="output/delta.json"):
        with open(output, "w") as f:
            json.dump(
                {
                    "additions": self.form_added(patched_storage),
                    "deletions": self.form_deletions(patched_storage),
                    "updates": self.form_updates(patched_storage)
                },
                f, indent=2
            )
        logger.info(f"File {output} created...")

    # Немного не понял зачем нужен этот выходной файл, потому что если есть входной
    # patched_config.json, то почему бы его просто не скопировать как выходной?
    # На всякий случай написал алгоритм для обработки, но самый логичный вариант - это
    # просто скопировать patched_config.json в res_patched_config.json
    def create_res_patched(self, deltas, output="output/res_patched_config.json"):
        data = {}
        if isinstance(deltas, str):
            with open(deltas, "r") as f:
                data = json.load(f)
        else:
            data = deltas

        additions = {obj["key"]: obj["value"] for obj in data["additions"]}
        deletions = data["deletions"]
        updates = {obj["key"]: obj["to"] for obj in data["updates"]}

        result = {**self.params, **additions}

        for k in self.params.keys():
            if k in deletions:
                result.pop(k)

            updated_value = updates.get(k)

            if updated_value is not None:
                result[k] = updated_value
        
        with open(output, 'w') as f:
            json.dump(result, f, indent=2)