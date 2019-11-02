import sys
import json
catched = json.loads(str(sys.argv[1]))

x1 = catched[0]
x2 = catched[1]
x3 = catched[2]


u1 = 2 * x1 + x2 - x3 + 1 
u2 = -3 * x1 - 2 * x2 + 2 * x3 - 1
u3 = x1 + 4 * x2 - 7 * x3 + 3

little = 0.0000001

# чем ближе результаты уравнения к 0 тем больше цифра
print(1.0 / (u1 + little) + 1.0 / (u2 + little) + 1.0 / (u3 + little))
