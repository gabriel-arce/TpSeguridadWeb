import json

table = [[]]

with open('proyectos.json') as file:
	raw_data = file.read()

#	proyectos = raw_data['Proyectos']

#	for p in proyectos:
#		print('Nombre: ' + p['ProyectoNombre'])
#		print('')


#def dictList(d, column_name=''):
#	for k, v in d.items():
#		if isinstance(v, dict):
#			dictList(v, column_name = k)
#			continue

#		if column_name:
#			column_name +='.'

#		column_name += k
		#table[0].append(column_name)
#		table[0].append(v)

data_string = json.dumps(raw_data, indent=4)
users_dict  = json.loads(data_string)

print users_dict

#dictList(raw_data)

#for row in table:
#	print (row)

proyecto = json.loads('{ "ProyectoNombre": "Actualizacion de logistica", "ProyectoEmpresa": "Edesur S.A.", "ProyectoCosto": 1500, "ProyectoEmail": "info@edesur.com.ar" }')
print json.dumps(proyecto)
