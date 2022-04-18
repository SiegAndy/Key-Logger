from Pattern import Repeat, Pattern


# category_pattern = r"\[(.*)\]"
# attribute_pattern = r"(.*)=(.*)"
# a = re.compile(category_pattern)
# b = re.compile(attribute_pattern)
# print(a.match("[mycategory]").group(1))
# bb = b.match("mytest=tesvalue")
# print(a.match(attribute_pattern))
# print(bb.group(1), bb.group(2))


# dummy = {
#     "scripts":[
#             "aaa",
#             "bbb"
#         ],
#         "<category>": {
#             "attribute_1": "value_1",
#             "attribute_2": "value_2",
#         },
        
#     }
# dict_to_klp("test", dummy)
# result = klp_to_dict("src/scripts/test.klp")
# assert result == dummy


# a = Repeat(1,)

# pa = Pattern("name")
# pa.create_pattern(["KeyPress TAB 1", "KeyPress 1 1", "Delay 2500", "KeyPress 2 1"])
# result = pa.toDict()
# print(result)
# pa.fromDict(result)
# print(pa.toDict())
# print(result == pa.toDict())

a = {
    '1':{
        '2':{
            '3':4
        }
    }
}

b = a['1']['2']['3']
print(b)
b = 5
print(a, b)