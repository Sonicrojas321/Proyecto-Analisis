Proyecto de Analisis de protocolos - Creación de servidor HTTP con Sockets
import socket

host = '192.168.20.10'
port = 8080

servidorSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidorSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

servidorSocket.bind((host, port))

servidorSocket.listen(1)

print('Servidor en el puerto', port)

while True:
    connection , address = servidorSocket.accept()
    request = connection.recv(1024).decode('utf-8')
    #print(request)
    lista_String = request.split(' ')
    metodo = lista_String[0]
    archivo_solicitado = lista_String[1]
    
    print('Petición: ', archivo_solicitado)

    miarchivo = archivo_solicitado.split('?')[0]
    miarchivo = miarchivo.lstrip('/')

    if(miarchivo == ''):
        miarchivo = 'index.html'

    try:
        archivo = open(miarchivo , 'rb')
        response = archivo.read()
        archivo.close()

        cabezera = 'HTTP/1.1 200 OK\n'

        if(miarchivo.endswith('.jpg')):
            mimetype = 'image/jpg'
        elif(miarchivo.endswith('.pdf')):
            mimetype = 'application/pdf'
        else:
            mimetype = 'text/html'
        cabezera += 'Content-Type: ' +str(mimetype)+'\n\n'

    except Exception as e:
        cabezera = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body> Error 404: Archivo no encontrado </body></html>'.encode('utf-8')
    
    final_response = cabezera.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()
