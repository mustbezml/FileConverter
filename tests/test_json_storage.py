from src.Storages import JSONStorage
import json

def test_init_storage():
    test_data = JSONStorage("input/config.json")

    assert not test_data.is_patched
    
    with open("input/config.json", 'r') as f:
        input_data = json.load(f)

    for key in input_data:
        assert key in test_data.params

def test_init_patched_storage():
    test_patched_data = JSONStorage("input/patched_config.json")

    assert test_patched_data.is_patched
    
    with open("input/patched_config.json", 'r') as f:
        input_data = json.load(f)

    for key in input_data:
        if key.startswith("added"):
            assert key in test_patched_data.added_params
        else:
            assert key in test_patched_data.params

def test_deletions():
    test_data = JSONStorage("input/config.json")
    test_patched_data = JSONStorage("input/patched_config.json")

    with open("input/config.json", 'r') as f:
        input_data = json.load(f)

    with open("input/patched_config.json", 'r') as f:
        patched_input_data = json.load(f)

    json_compare_data = set.symmetric_difference(set(input_data.keys()), list({k for k in patched_input_data if not k.startswith("added")}))
    json_compare_data = list(json_compare_data)
    assert test_data.form_deletions(test_patched_data) == json_compare_data

def test_res_patched_formation():
    with open("input/patched_config.json", 'r') as f:
        input_data = json.load(f)

    with open("output/res_patched_config.json", 'r') as f:
        patched_input_data = json.load(f)

    assert input_data == patched_input_data