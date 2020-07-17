import sys

for arg in sys.argv:
	print(f'tipo: {type(arg)} conteúdo: {arg}')

if( len(sys.argv) <= 1):
	print("Empty")

print(len(sys.argv))