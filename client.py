import socket, threading   
from pydub import AudioSegment
from pydub.playback import play

client_socket = ''

def convertUtf(data):
    return(bytes(data, 'utf-8'))

def connection():
    global client_socket
    client_socket = socket.socket()
    port = 12345
    client_socket.connect(('127.0.0.1',port))
    
        

    #recieve connection message from server
    

def reader():
    while True:
        try:
            recv_msg = client_socket.recv(1024)
            recv_msg = recv_msg.decode()
            if recv_msg.startswith('@song'):
                path = recv_msg[recv_msg.index('@song'):]
                song = AudioSegment.from_wav(path)
                play(song)
            print (recv_msg)
        except: pass

def sender():
    #send user details to server
    while 1:
        send_msg = input("Send your message in format [@user:message] ")
        if send_msg == 'exit':
            client_socket.close()
        elif send_msg == '@song':
            client_socket.send(convertUtf(send_msg))
        else:
            client_socket.send(convertUtf(send_msg))


if __name__ == "__main__":
    t1 = threading.Thread(target=connection)
    t2 = threading.Thread(target=reader)
    t3 = threading.Thread(target=sender)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()