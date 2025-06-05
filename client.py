import socket

HOST = "127.0.0.1"  # ip del servidor al cual me voy a conectar
PORT = 40123        # puerto de conexion


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

def main():
    data = cliente.recv(1024)
    print(data.decode("utf-8"))

    msj = ""
    while msj != "/exit":
        msj = input("Tu >> ")
        cliente.send(msj.encode("utf-8"))
        msj_server = cliente.recv(1024).decode("utf-8")
        print("Server >> " + msj_server)
    cliente.close()

main()
