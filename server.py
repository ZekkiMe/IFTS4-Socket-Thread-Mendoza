import socket

HOST = "127.0.0.1" # direccion de loopback
PORT = 40123        # usar puertos entre 1023 y 65535

help_msj = "\n\n/login \t\tPara ingresar\n/send \t\tEnviar mensaje a otro usuario\n/sendall  \tEnviar mensaje a todos los usuarios conectados\n/show  \t\tMostrar usuarios conectados\n/help \t\tVer los comandos\n/exit \t\tSalir\n"
primer_msj = f"Hola Bienvenido al Servidor!!{help_msj}"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

usuario = ""

def login(client):
    global usuario
    while usuario == "":
        client.send("Envie su nombre".encode("utf-8"))
        data = client.recv(1024)

        if not data:
            client.send("Campo vacio \ningrese nuevamente o /exit para salir".encode("utf-8"))
        elif data == "/exit":
            break
        else:
            usuario = data.decode("utf-8")
            client.send("Nombre Cargado".encode("utf-8"))

def exit(client, ip):
    global usuario
    print(f"Se desconectó > {usuario} > {ip} ")
    client.send("Desconectando del Servidor..".encode("utf-8"))
    client.close()
    usuario = ""

def help(client, ip):
    global usuario
    if usuario != "":
        print(f"{usuario} Solcitó /help")
    else:
        print(f"{ip} Solcitó /help")
    client.send(help_msj.encode("utf-8"))

def main(): 
    global usuario
    print("esperando conexion..")
    conexion_cliente, direccion = server.accept()
    conexion_cliente.send(primer_msj.encode("utf-8"))
    print(f"Conexion desde: {direccion}")


    while True:
        data = conexion_cliente.recv(1024)

        if not data:
            print(f"Se desconectó el cliente {direccion}")
            conexion_cliente.close()
            usuario = ""
            break
            
        mensaje_cliente = data.decode("utf-8")
        match mensaje_cliente:
            case "/login":
                login(conexion_cliente)
                if usuario != "":
                    print(f"{direccion} > {usuario} ")
            case "/exit":
                exit(conexion_cliente, direccion)
                break
            case "/help":
                help(conexion_cliente, direccion)
            case _:
                if usuario != "":
                    print(f"{usuario} >> " + mensaje_cliente)
                else:
                    print("Cliente >> " + mensaje_cliente)
                msj_server = "Recibido"
                conexion_cliente.send(msj_server.encode("utf-8"))


                

# print("esperando conexion..")
try:
    main()
except KeyboardInterrupt:
    print("\nServidor apagándose...")
    server.close()
except Exception as e:
    print(f"Ha ocurrido un error inesperado en el servidor: {e}")
    server.close()