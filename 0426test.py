# -*- coding: utf-8 -*-
import socketserver
import threading
## 0504 test
import pymysql as ps
from datetime import datetime
import re

HOST = '0.0.0.0'
PORT = 8787
lock = threading.Lock()  # syncronized 동기화 진행하는 스레드 생성
messages = [] #추가내용 0503

sql = 'insert into 0404test (time, temp, mor) values ("%s", "%s", "%s")'

class UserManager:  

    def __init__(self):
        self.users = {}  # 사용자의 등록 정보를 담을 사전 {사용자 이름:(소켓,주소),...}

    def addUser(self, username, conn, addr):  # 사용자 ID를 self.users에 추가하는 함수
        if username in self.users:  # 이미 등록된 사용자라면
            conn.send('이미 등록된 사용자입니다.\n'.encode())
            return None

        # 새로운 사용자를 등록함
        lock.acquire()  # 스레드 동기화를 막기위한 락
        self.users[username] = (conn, addr)
        lock.release()  # 업데이트 후 락 해제

        self.sendMessageToAll('[%s]님이 입장했습니다.' % username)
        print('+++ 대화 참여자 수 [%d]' % len(self.users))

        return username

    def removeUser(self, username):  # 사용자를 제거하는 함수
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        self.sendMessageToAll('[%s]님이 퇴장했습니다.' % username)
        print('--- 대화 참여자 수 [%d]' % len(self.users))

    def messageHandler(self, username, msg):  # 전송한 msg를 처리하는 부분
        if msg[0] != '/':  # 보낸 메세지의 첫문자가 '/'가 아니면
            self.sendMessageToAll('[%s] %s' % (username, msg))
            if username == 'aa':
                num = re.sub(r'[^0-9]','',msg)
                if len(num) >= 8:
                    hum = num[0:2] + "." + num[2:4]
                    tem = num[4:6] + "." + num[6:8]
                    print(hum,tem)
                else:
                    print(num)
            return

        if msg.strip() == '/quit':  # 보낸 메세지가 'quit'이면
            self.removeUser(username)
            return -1

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())

#0503추가내용
    def addMessage(self,message):
        messages.append(message)

class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    def handle(self):  # 클라이언트가 접속시 클라이언트 주소 출력
        print('[%s] 연결됨' % self.client_address[0])

        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)

            while msg:
                print(msg.decode())

                self.userman.addMessage('[%s] %s' % (username, msg.decode())) #0503test

                if self.userman.messageHandler(username, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)

        except Exception as e:
            print(e)

        print('[%s] 접속종료' % self.client_address[0])
        self.userman.removeUser(username)

    def registerUsername(self):
        while True:
            self.request.send('로그인ID:'.encode())
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.userman.addUser(username, self.request, self.client_address):
                return username

class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def runServer():
    print('+++ 채팅 서버를 시작합니다.')
    print('+++ 채팅 서버를 끝내려면 Ctrl-C를 누르세요.')

    try:
        global server
        server = ChatingServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('--- 채팅 서버를 종료합니다.')
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    
    con = ps.connect(host = str("211.253.11.217"),
                     port = 11000,
                     user = str("kkamduo"),
                     password = str("ghdwotjr12"),
                     db = str("test"),
                     charset = "utf8")

    cur = con.cursor()
    cur.execute("show tables")
    test = cur.fetchall()
    
    if "0404test" not in test[0]:
        pass
    
    runServer()
    
    # cur.execute(sql%(str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second), temp, hum))
    con.commit()

