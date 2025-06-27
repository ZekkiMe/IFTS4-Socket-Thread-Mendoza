import socket
import threading

HOST = "127.0.0.1" # direccion de loopback
PORT = 40123        # usar puertos entre 1023 y 65535

HELP_MSJ = '''
/help                                   Muestra las funciones
/show                                   Muestra los usuarios conectados
/exit                                   Te desconecta del servidor
/login <nombre>                         Ingresa a al servicio de chat
/sendall <Mensaje>                      Envia un mensaje a todos los usuario conectados
/send <nombre_destinatario> <mensaje>   Envia un mensaje directo a el usuario seleccionado
/clear                                  Limpia la terminal
'''
PRIMER_MSJ = f"Hola Bienvenido al Servidor!!\n{HELP_MSJ}"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

clientes =[]
nombres = []

def broadcast(mensaje, cliente_enviador):
    for cliente in clientes:
        if cliente != cliente_enviador:
            try:
                cliente.send(mensaje)
            except:
                if cliente in clientes:
                    idx = clientes.index(cliente)
                    if idx < len(nombres):
                        desconectado = nombres[idx]
                        print(f"[Server] {desconectado} desconectado (error al enviar).")
                        clientes.remove(cliente)
                        nombres.remove(desconectado)
                    else:
                        clientes.remove(cliente)
                else:
                    pass

def handle_client(client, addr):
    nombre_cliente = None

    while True:
        try:
            mensaje = client.recv(1024)
            msj = mensaje.decode("utf-8")

            if msj.lower() == "/exit":
                break

            elif msj.lower() == "/help":
                client.send(HELP_MSJ.encode("utf-8"))

            elif msj.lower() == "/show":
                mensaje = "\nUsuarios conectados:"
                for nombre in nombres:
                    mensaje+= f"\n\t{nombre}"
                client.send(f"{mensaje}\n".encode("utf-8"))

            elif msj.lower().startswith("/login"):
                data = msj[len("/login"):].strip()
                if data in nombres: 
                    client.send("\n [Server] Ese nombre ya se encuentra en uso".encode("utf-8"))
                else:
                    nombres.append(data)
                    clientes.append(client)
                    client.send("\n [Server] Recibido. Para enviar al chat Grupal ingresa -> /sendall <mensaje>\n\tPara un mensaje directo -> /send <nombre_destinatario> <mensaje>".encode("utf-8"))
                    nombre_cliente = data
                    broadcast(f"{data} se ha logeado".encode("utf-8"), client)

            elif msj.lower().startswith("/sendall"):
                if nombre_cliente is None:
                    client.send("\n [Server] Necesitas logearte para enviar mensajes.".encode("utf-8"))
                    continue
                else:
                    data = msj[len("/sendall"):].strip()
                    broadcast(f"{nombre_cliente}: {data}".encode("utf-8"), client)

            else:
                if msj.lower().startswith("/send"):
                    if nombre_cliente is None:
                        client.send("\n [Server] Necesitas logearte para enviar mensajes.".encode("utf-8"))
                        continue
                    else:
                        data = msj.split(' ', 2)
                        if len(data) < 3:
                            client.send("\n [Server] Formato incorrecto para /send. Usa: /send <nombre> <mensaje>".encode("utf-8"))
                            continue
                        d_nombre = data[1]
                        d_mensaje = data[2]
                        if d_nombre == nombre_cliente:
                            client.send("\n [Server] No te puedes enviar un mensaje a ti mismo".encode("utf-8"))
                            continue
                        else:    
                            if d_nombre in nombres:
                                index = clientes[nombres.index(d_nombre)]
                                index.send(f"[DIRECTO]{nombre_cliente}: {d_mensaje}".encode("utf-8"))
                                client.send(f"\n [Server] Mensaje directo enviado a {d_nombre}.".encode("utf-8"))
                            else:
                                client.send("\n [Server] No se encuetra ese usuario".encode("utf-8"))
                else:
                    if nombre_cliente is None:
                        client.send("\n [Server] Necesitas iniciar sesión con /login <nombre> para chatear.\n".encode("utf-8"))
                        print(f"Mensaje no logeado de {addr[0]}: {msj}")
                    else:
                        client.send("\n [Server] Comando no reconocido. Usa /help para ver los comandos.\n".encode("utf-8"))
                        print(f"Comando desconocido de {nombre_cliente}: {msj}")

        except:
            index = clientes.index(client)
            nombre = nombres[index]
            broadcast(f"\n [Server] <{nombre}> Se Desconectó".encode('utf-8'), client)
            clientes.remove(client)
            nombres.remove(nombre)
            client.close()
            break

def receive():
    try:
        while True:
            client, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            client.send(PRIMER_MSJ.encode("utf-8"))

            thread = threading.Thread(target=handle_client, args=(client,addr,))
            thread.start()
    except KeyboardInterrupt: # Cuando se presiona Ctrl+C
        print("\nServidor apagándose...")
    except Exception as e: # Para otros errores inesperados
        print(f"Error inesperado en receive: {e}")
    finally: # Por ultimo Cierra el Server
        server.close()
        print("Servidor cerrado.")

print("Servidor esperando conexiones.")
receive()