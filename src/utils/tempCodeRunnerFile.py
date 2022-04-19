dummy = {
    "<category>": {
        "attribute_1": "value_1",
        "attribute_2": "value_2",
    }
}
dict_to_klp("test", dummy)
result = klp_to_dict("src/scripts/test.klp")
assert result == dummy
