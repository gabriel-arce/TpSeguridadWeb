import json
import os.path

JSON_FILE = './lib/proyectos.json'
JSON_FILE_PREFIX = './lib/proyectos_'
JSON_FILE_SUFIX  = '.json'

proyectos = []


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


class ProyectoEncoder(json.JSONEncoder):
	def default(self, obj):
		return obj.__dict__


class ProyectoDecoder(object):
	def __init__(self, j):
		self.__dict__ = json.loads(j)


def objCreator(d):
	return Proyecto(d['ProyectoUsuario'], d['ProyectoNombre'] ,d['ProyectoEmpresa'], d['ProyectoCosto'], d['ProyectoEmail'])


def getProyectos(Usuario):
	fd = JSON_FILE_PREFIX + Usuario + JSON_FILE_SUFIX

	with open(JSON_FILE, 'r') as file:
		proyectos = json.load(file, object_hook = objCreator)
		return proyectos


def getProyectosPorUsuario(Usuario):

	result 		= []
	proyectos 	= getProyectos(Usuario)

	if proyectos:
		for proyecto in proyectos:

			#Deserializar el proyecto
			#p = json.dumps(proyecto, cls=ProyectoEncoder, indent=4)

			#Deserializar el proyecto
			#p = ProyectoDecoder(proyecto)

			#Solo los proyectos del usuario
			if proyecto.ProyectoUsuario == Usuario:
				result.append(proyecto)

		return result

	return result
	
def agregarProyecto(Form, Usuario):
	aux = []

	ProyectoUsuario 	= Usuario
	ProyectoNombre 		= Form['ProyectoNombre']
	ProyectoEmpresa 	= Form['ProyectoEmpresa']
	ProyectoCosto 		= Form['ProyectoCosto']
	ProyectoEmail 		= Form['ProyectoEmail']

	#Crear instancia
	proyecto 	= Proyecto(ProyectoUsuario, ProyectoNombre, ProyectoEmpresa, ProyectoCosto, ProyectoEmail)

	#Buscar los proyectos del usuario y agregar el nuevo proyecto
	#proyectos = getProyectosPorUsuario(Usuario) 
	proyectos = getProyectos(Usuario)

	print proyectos

	proyectos.append(proyecto)

	#Actualizar JSON de proyectos
	for proy in proyectos:

		#Deserializar el proyecto
		#p = ProyectoDecoder(proy)

		#Solo los proyectos del usuario
		#if p.ProyectoUsuario == Usuario:
			serialize = json.dumps(proy, cls=ProyectoEncoder, indent=4)
			aux.append(serialize)
			print serialize

		#else:
		#	aux.append(proy)
		#	print proy 	

	fd = JSON_FILE_PREFIX + Usuario + JSON_FILE_SUFIX

	with open(JSON_FILE, 'w') as file:
		json.dump(aux, file)

	return proyectos


