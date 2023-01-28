import socket,select

def convertUtf(data):
    return(bytes(data, 'utf-8'))


port = 12345
socket_list = []
users = {}
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('',port))
server_socket.listen(5)
socket_list.append(server_socket)
while True:
    ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)
    for sock in ready_to_read:
        if sock == server_socket:
            connect, addr = server_socket.accept()
            socket_list.append(connect)
            connect.send( convertUtf("You are connected from:" + str(addr)))
        else:
            try:
                data = sock.recv(2048)
                data = data.decode()
                print (data)
                if data.startswith("#"):
                    users[data[1:].lower()]=connect
                    print ("User " + data[1:] +" added.")
                    connect.send(convertUtf("Your user detail saved as : "+str(data[1:])))
                elif data.startswith('@song'):
                     for user in users:
                        # users[data[1:data.index(':')].lower()].send(convertUtf(data[data.index(':')+1:]))
                        users[user].send(convertUtf(data))
                else:
                    for user in users:
                        # users[data[1:data.index(':')].lower()].send(convertUtf(data[data.index(':')+1:]))
                        print (user)
                        users[user].send(convertUtf(data))

            except:
                continue

server_socket.close()