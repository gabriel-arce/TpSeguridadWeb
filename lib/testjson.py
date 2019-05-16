import json

JSON_FILE = '../lib/proyectos3.json'
JSON_FILE2 = '../lib/proyectos.json'

class Proyecto:
	def __init__(self, Usuario, Nombre, Empresa, Costo, Email):
		self.ProyectoUsuario 	= Usuario
		self.ProyectoNombre 	= Nombre
		self.ProyectoEmpresa 	= Empresa
		self.ProyectoCosto 		= Costo
		self.ProyectoEmail 		= Email

	def __str__(self):
		return '{{"ProyectoUsuario" = "{0}", "ProyectoNombre" = "{1}", "ProyectoEmpresa" = "{2}", "ProyectoCosto" = "{3}", "ProyectoEmail" = "{4}"}}'.format(self.ProyectoUsuario, self.ProyectoNombre, self.ProyectoEmpresa, self.ProyectoCosto, self.ProyectoEmail)

	def __getitem__(self, key):
		return getattr(self, key)

class ProyectoEncoder(json.JSONEncoder):
	def default(self, obj):
		return obj.__dict__


def objCreator(d):
	return Proyecto(d['ProyectoUsuario'], d['ProyectoNombre'] ,d['ProyectoEmpresa'], d['ProyectoCosto'], d['ProyectoEmail'])


with open(JSON_FILE, 'r') as file:
	proyectos = json.load(file, object_hook = objCreator)


#print proyectos[0]['ProyectoNombre']

#proyecto = Proyecto('test2', 'tester de proyecto', 'rondamori house', 15000, 'rondamori@me.com')
#proyectos.append(proyecto)

print proyectos
proyecto = json.dumps(proyectos[4], cls=ProyectoEncoder, indent=2)
print proyecto 
#print proyectos[4]

#print proyecto
#print type(proyecto)
#print proyecto['ProyectoUsuario']

#aux  = []
#aux2 = None

for proy in proyectos:

	serialize = json.dumps(proy, cls=ProyectoEncoder, indent=2)
#	aux.append(serialize)
#	print serialize[0]

#print aux
#with open(JSON_FILE2, 'w') as file2:
#	json.dump(aux, file2) 



