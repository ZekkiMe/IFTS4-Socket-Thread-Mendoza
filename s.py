import socket
import threading

HOST = "127.0.0.1" # direccion de loopback
PORT = 40123        # usar puertos entre 1023 y 65535

PRIMER_MSJ = f"Hola Bienvenido al Servidor!!"

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
                pass


def handle_client(client):
    grupal = False
    nombre_cliente = None
    while True:
        try:
            mensaje = client.recv(1024)
            msj = mensaje.decode("utf-8")
            if msj.lower() == "/exit":
                break

            elif msj.lower() == "/show":
                if nombres != "":
                    mensaje = "\nUsuarios conectados:"
                    for nombre in nombres:
                        mensaje+= f"\n\t{nombre}"
                    client.send(mensaje.encode("utf-8"))

            elif msj.lower().startswith("/login"):
                data = msj[len("/login"):].strip()
                nombres.append(data)
                clientes.append(client)
                client.send("Recibido. Para ingresar al chat Grupal ingresa -> /sendall".encode("utf-8"))
                nombre_cliente = data
                broadcast(f"{data} se ha logeado".encode("utf-8"), client)

            elif msj.lower().startswith("/send"):
                if nombre_cliente is None:
                    client.send("Necesitas logearte para enviar mensajes privados.".encode("utf-8"))
                    continue
                else:
                    data = msj.split(' ', 2)
                    d_nombre = data[1]
                    d_mensaje = data[2]
                    if d_nombre == nombre_cliente:
                        client.send("No te puedes enviar un mensaje a ti mismo".encode("utf-8"))
                    else:    
                        if d_nombre in nombres:
                            index = clientes[nombres.index(d_nombre)]
                            index.send(f"{nombre_cliente}: {d_mensaje}".encode("utf-8"))
                        else:
                            client.send("No se encuetra ese usuario".encode("utf-8"))
            else:
                if nombre_cliente != None:
                    private = ""
                    if grupal == True:
                        if msj.lower().startswith("/private"):
                            grupal = False
                            private = msj[len("/private"):].strip()
                            if private == nombre_cliente:
                                client.send("No te puedes enviar un mensaje a ti mismo".encode("utf-8"))
                                continue
                            else:    
                                if private in nombres:
                                    index = clientes[nombres.index(private)]
                                    client.send(f"Conectado a {private}")
                                    private = index
                                else:
                                    client.send("No se encuetra ese usuario".encode("utf-8"))
                        else:    
                            broadcast(f"{nombre_cliente}: {msj}".encode("utf-8") ,client)
                    elif grupal == False:
                        if msj.lower() == "/sendall":
                            grupal = True
                            client.send("Entrendo a chat Grupal".encode("utf-8"))
                        else:
                            private.send(f"[PRIVADO]{nombre_cliente}: {msj}".encode("utf"))

                    


                else:
                    print(msj)
                    client.send("Necesitas logearte".encode("utf-8"))

        except:
            index = clientes.index(client)
            nombre = nombres[index]
            broadcast(f"ChatBot: {nombre} disconnected".encode('utf-8'), client)
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

            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()

    except:
        server.close()

print("Servidor esperando conexiones.")
receive()