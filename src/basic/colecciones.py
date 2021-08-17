usuarios = {'Marta', 'Elvira', 'Juan', 'Marcos'}
admin = {'Juan', 'Marta'}

admin.discard('Juan')
admin.add('Marcos')

for usuario in usuarios:
	if usuario in admin:
		print usuario, 'es adminitrador'
	else:
		print usuario, 'no es admin'

##########################################################################

caballero = {'vida':2, 'ataque':2, 'defensa':2, 'alcance':2}
guerrero = {'vida':2, 'ataque':2, 'defensa':2, 'alcance':2}
arquero = {'vida':2, 'ataque':2, 'defensa':2, 'alcance':2}

caballero['vida'] = guerrero['vida']*2
caballero['defensa'] = guerrero['defensa']*2

guerrero['ataque'] = caballero['ataque'] *2
guerrero['alcance'] = caballero['alcance'] *2

arquero['vida'] = guerrero['vida']
arquero['ataque'] = guerrero['ataque']
arquero['defensa'] = guerrero['defensa']/2
arquero['alcance'] = guerrero['alcance']*2

print 'Caballero\t', caballero
print 'Guerrero\t', guerrero
print 'Arquero\t', arquero

##########################################################################

tareas = [
	[6, 'Distribucion'],
	[2, 'Disenio'], 
	[1, 'Concepcion'], 
	[7, 'Mantenimiento'],
	[4, 'Produccion'], 
	[3, 'Planificacion'], 
	[5, 'Pruebas']
]

print("==Tareas desordenadas")

for t in tareas:
	print t[0], t[1]

from collections import deque

tareas.sort()

cola = deque()

for t in tareas:
	cola.append(t[1])

print("\n==Tareas desordenadas")
for t in cola:
	print t








