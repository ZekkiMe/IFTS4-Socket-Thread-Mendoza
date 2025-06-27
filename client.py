import socket
import threading
import os
HOST = "127.0.0.1"  # ip del servidor al cual me voy a conectar
PORT = 40123        # puerto de conexion
nombre = None
# Esta funcion recive los mensajes del servidor lo decodifica y evalua si esta vacio, caso contrario lo muestra en pantalla 
def recibir():
    while True:
        try:
            mensaje = cliente.recv(1024).decode("utf-8")
            print(mensaje)

        except Exception as e:
            print(e)
            cliente.close()
            break

# Esta funcion solicita ingresar un mensaje y luego lo envia codificado en caso de ser "/exit, "
def enviar():
    while True:
        mensaje = input("")
        if mensaje.lower() == "/clear":
            os.system('cls')
        else:
            try:
                if mensaje.lower() == "/exit":
                    print("Cerrando sesión...")
                    cliente.send(mensaje.encode("utf-8"))
                    cliente.close()
                    break
                elif mensaje.lower() == "/login":
                    nombre = input("Ingrese el nombre: ")
                    if nombre:
                        cliente.send(f"{mensaje}{nombre}".encode("utf-8"))
                    else:
                        print("\n [Server] El nombre de usuario no puede estar vacío.")
                elif mensaje.lower() == "/send":
                    usuario = input("Ingrese el Nombre del destinatario: ")
                    mensaje_privado = input("Ingrese su mensaje: ")
                    cliente.send(f"{mensaje} {usuario} {mensaje_privado}".encode("utf-8"))
                elif mensaje.lower() == "/sendall":
                    mensaje_all = input("ingrese su mensaje: ")
                    cliente.send(f"{mensaje} {mensaje_all}".encode("utf-8"))
                
                else:
                    cliente.send(mensaje.encode("utf-8"))
            except Exception as e:
                print(e)
                cliente.close()

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

recibir = threading.Thread(target=recibir)
recibir.start()

enviar = threading.Thread(target=enviar)
enviar.start()
