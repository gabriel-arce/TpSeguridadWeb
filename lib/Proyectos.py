import json

JSON_FILE = './lib/proyectos.json'


class ServerError(Exception): pass 

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

	def keys(self):
		return ('items')

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def objCreator(d):
	return Proyecto(d['ProyectoUsuario'], d['ProyectoNombre'] ,d['ProyectoEmpresa'], d['ProyectoCosto'], d['ProyectoEmail'])


def getProyectos():
	with open(JSON_FILE, 'r') as file:
		proyectos = json.load(file, object_hook = objCreator)

	return proyectos


def getProyectosPorUsuario(Usuario):

	result 		= []
	proyectos 	= getProyectos()

	for proyecto in proyectos:
		if proyecto.ProyectoUsuario == Usuario:
			result.append(proyecto)

	return result


def agregarProyecto(Form, Usuario):
	ProyectoUsuario 	= Usuario
	ProyectoNombre 		= Form['ProyectoNombre']
	ProyectoEmpresa 	= Form['ProyectoEmpresa']
	ProyectoCosto 		= Form['ProyectoCosto']
	ProyectoEmail 		= Form['ProyectoEmail']

	proyecto 	= Proyecto(ProyectoUsuario, ProyectoNombre, ProyectoEmpresa, ProyectoCosto, ProyectoEmail)
	s  			= json.dumps(proyecto.__dict__)

	print s
	proyectos 	= getProyectos()

	#inicializa
	#oldData = json.loads(open(JSON_FILE, 'r').read())

	proyectos.append(proyecto)
	print proyectos

	with open(JSON_FILE, 'w') as updateFile:
		json.dump(proyectos, updateFile)
		
	return 'creado'


