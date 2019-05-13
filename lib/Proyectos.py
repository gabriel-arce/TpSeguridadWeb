import json


class ServerError(Exception): pass 

class Proyecto:
	def __init__(self, Usuario, Nombre, Empresa, Costo, Email):
		self.Usuario 	= Usuario
		self.Nombre 	= Nombre
		self.Empresa 	= Empresa
		self.Costo 		= Costo
		self.Email 		= Email

	def __str__(self):
		return '{{"ProyectoUsuario" = "{0}", "ProyectoNombre" = "{1}", "ProyectoEmpresa" = "{2}", "ProyectoCosto" = "{3}", "ProyectoEmail" = "{4}"}}'.format(self.Usuario, self.Nombre, self.Empresa, self.Costo, self.Email)

	def __getitem__(self, key):
		return getattr(self, key)

	def keys(self):
		return ('items')


def objCreator(d):
	return Proyecto(d['ProyectoUsuario'], d['ProyectoNombre'] ,d['ProyectoEmpresa'], d['ProyectoCosto'], d['ProyectoEmail'])

def getProyectos():
	with open('./lib/proyectos.json', 'r') as file:
		proyectos = json.load(file, object_hook = objCreator)

	return proyectos

def getProyectosPorUsuario(usuario):

	aux = {}

	proyectos = getProyectos()

	for proyecto in proyectos:
		print proyecto['items']
		#if proyecto['Usuario'] == usuario: 
		#	aux.append(proyecto)

	return aux


