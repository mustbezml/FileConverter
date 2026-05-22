from src.Storages import XMLStorage
from src.Converter import FileConverter

import xml.etree.ElementTree as ET

def test_disassembly_classes_values():
    test_storage = XMLStorage()
    test_storage.disassemble_xml()
    classes = test_storage.classes
    
    for class_data in classes.values():
        assert isinstance(class_data, dict)

        assert "name" not in class_data
        assert "isRoot" in class_data
        assert "documentation" in class_data

def test_disassembly_aggregations_values():
    test_storage = XMLStorage()
    test_storage.disassemble_xml()
    aggregations = test_storage.aggregations

    for aggregation_data in aggregations:
        assert isinstance(aggregation_data, dict)

        assert "source" in aggregation_data
        assert "target" in aggregation_data
        assert "sourceMultiplicity" in aggregation_data
        assert "targetMultiplicity" in aggregation_data