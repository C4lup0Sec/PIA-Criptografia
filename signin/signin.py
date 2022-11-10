from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from sqlqueries import QueriesSQLite
from cryptography.fernet import Fernet

Builder.load_file('signin/signin.kv')

class SigninWindow(BoxLayout):
	def __init__(self, poner_usuario_callback, **kwargs):
		super().__init__(*kwargs)
		self.poner_usuario=poner_usuario_callback

	def verificar_usuario(self, username, password):
		connection = QueriesSQLite.create_connection("pdvDB.sqlite")
		users=QueriesSQLite.execute_read_query(connection, "SELECT * from usuarios")
		if users:
			if username=='' or password=='':
				self.ids.signin_notificacion.text='Falta nombre de usuario y/o contraseña'
			else:
				usuario={}
				for user in users:
					if user[1]==username:
						usuario['nombre']=user[1]
						usuario['username']=user[0]
						#Borrar
						print("Antes de desencriptar: ",user[2])
		
						f = Fernet(b'FINEHtwMUOxgvyYM9fOvpXcQHYDDZKb3-NkPWTrZN5g=')
						b_password = bytes(user[2], 'ascii')
						b_password_decrypt = f.decrypt(b_password)
						contra_D=b_password_decrypt.decode('ascii')
						
						#Borrar
						print("Despues de desencriptar: ",contra_D)
						usuario['password']=contra_D
						usuario['tipo']=user[3]
						break
				if usuario:
					if usuario['password']==password:
						self.ids.username.text=''
						self.ids.password.text=''
						self.ids.signin_notificacion.text=''
						if usuario['tipo']=='trabajador':
							self.parent.parent.current='scrn_ventas'
						else:
							self.parent.parent.current='scrn_admin'
						self.poner_usuario(usuario)
					else:
						self.ids.signin_notificacion.text='Usuario o contraseña incorrecta'
				else:
					self.ids.signin_notificacion.text='Usuario o contraseña incorrecta'
		else:
		    usuario_tuple=('usuario', 'Usuario Inicio', '123', 'admin')
		    crear_usuario = "INSERT INTO usuarios (username, nombre, password, tipo) VALUES (?,?,?,?);"
		    QueriesSQLite.execute_query(connection, crear_usuario, usuario_tuple)
		    self.ids.signin_notificacion.text='Se creo primer usuario. usuario 123'



class SigninApp(App):
	def build(self):
		return SigninWindow()

if __name__=="__main__":
	SigninApp().run()
