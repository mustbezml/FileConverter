from src.Converter import FileConverter
import json

def test_create_config():
    test_converter = FileConverter(config="tests/input/config.json", patched_config="tests/input/patched_config.json")

    test_converter.create_config(output_file="tests/output/config.xml")
    output = test_converter.xml_storage.open_xml(file="tests/output/config.xml")
    
    assert output.tag == "BTS"

    children = [ch for ch in output]
    children_tags = [ch.tag for ch in output]

    assert "id" in children_tags
    assert "name" in children_tags

    assert "MGMT" in children_tags
    assert "HWE" in children_tags
    assert "COMM" in children_tags

    mgmt_tag = children[children_tags.index("MGMT")]

    assert mgmt_tag.find("MetricJob") is not None
    assert mgmt_tag.find("CPLANE") is not None

def test_create_meta():
    test_converter = FileConverter(config="tests/input/config.json", patched_config="tests/input/patched_config.json")

    test_converter.create_meta(output_file="tests/output/meta.json", config_path="tests/output/config.xml")
    with open("tests/output/meta.json", 'r') as f:
        test_data = json.load(f)

    for test_object in test_data:
        assert "class" in test_object
        assert "documentation" in test_object
        assert "isRoot" in test_object

        assert isinstance(test_object["isRoot"], bool)

        assert "max" in test_object if not test_object["isRoot"] else "max" not in test_object
        assert "min" in test_object if not test_object["isRoot"] else "min" not in test_object
        assert "parameters" in test_object

        assert isinstance(test_object["class"], str)
        assert isinstance(test_object["documentation"], str)
        assert isinstance(test_object["max"], str) if "max" in test_object else True
        assert isinstance(test_object["min"], str) if "min" in test_object else True
        assert isinstance(test_object["parameters"], list)

def test_create_delta():
    test_converter = FileConverter(config="tests/input/config.json", patched_config="tests/input/patched_config.json")
    test_converter.config.create_deltas(test_converter.patched_config, output_file="tests/output/delta.json")

    with open("tests/output/delta.json", 'r') as f:
        test_data = json.load(f)

    assert "additions" in test_data
    assert "deletions" in test_data
    assert "updates" in test_data

    assert isinstance(test_data["additions"], list)
    assert isinstance(test_data["deletions"], list)
    assert isinstance(test_data["updates"], list)

def test_create_res_patched():
    test_converter = FileConverter(config="tests/input/config.json", patched_config="tests/input/patched_config.json")
    test_converter.config.create_res_patched("tests/output/delta.json", output_file="tests/output/res_patched_config.json")

    with open("tests/output/res_patched_config.json", 'r') as f:
        test_data = json.load(f)

    with open("tests/input/patched_config.json", 'r') as f:
        data_to_comapre = json.load(f)

    assert test_data == data_to_comapre