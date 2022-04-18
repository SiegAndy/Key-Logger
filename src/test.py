from Pattern import Repeat, Pattern
a = Repeat(1,)

pa = Pattern()
pa.create_pattern(["KeyPress TAB 1", "KeyPress 1 1", "Delay 2500", "KeyPress 2 1"])
result = pa.stringify()
pa.unstringify(result)
print(pa.stringify())
