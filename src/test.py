from Pattern import Repeat, Pattern
a = Repeat(1,)

pa = Pattern("name")
pa.create_pattern(["KeyPress TAB 1", "KeyPress 1 1", "Delay 2500", "KeyPress 2 1"])
result = pa.toDict()
print(result)
pa.fromDict(result)
print(pa.toDict())
print(result == pa.toDict())
