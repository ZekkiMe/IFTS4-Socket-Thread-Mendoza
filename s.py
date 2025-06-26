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
            elif msj.lower().startswith("/login"):
                data = msj[len("/login"):].strip()
                nombres.append(data)
                clientes.append(client)
                client.send("Recibido".encode("utf-8"))
                nombre_cliente = data
                broadcast(f"{data} se ha logeado".encode("utf-8"), client)
            else:
                if nombre_cliente != None:
                    if grupal == True:
                        broadcast(f"{nombre_cliente}: {msj}".encode("utf-8") ,client)
                    elif grupal == False:
                        if msj.lower() == "/sendall":
                            grupal = True
                            client.send("Entrendo a chat Grupal".encode("utf-8"))
                    if msj.lower().startswith("/send"):
                        data = msj[len("/send")].strip()
                        if data in nombres:
                            index = clientes[nombres.index(data)]
                            index.send("te hablaron".encode("utf-8"))
                        else:
                            client.send("No se encuetra ese usuario".encode("utf-8"))


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