# Ejercicio Socket - Thread

>Realizar un programa con sockets y threading que realice lo siguiente

#### Servidor

Permita multiples conexiones lleve la cuenta de las conexiones
Cuando un cliente se conecta le debe enviar un menu con 5 opciones.
```
    /login         Login
    /send          Enviar mensaje a otro usuario
    /sendall       Enviar mensaje a todos los usuarios conectados
    /show          Mostrar usuarios conectados
    /exit          Salir 
```
#### Cliente

El cliente tiene que poder conectarse al servidor y recibir el menú y poder ingresar una opción.

#### Ambas deben ser con dos hilos uno para envio y otro para recepcion.

>COSAS AGREGADAS POR EL ALUMNO:
>+ Se adicionó un comando ```/help``` para poder visualizar los comandos