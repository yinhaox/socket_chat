from tkinter import *
from socket import *
from random import choice
from json import dumps
from threading import Thread

class ReceiveThread(Thread):
    def __init__(self, tcpCliSock, BUFSIZ=1024):
        Thread.__init__(self)
        self.daemon = True  # 守护线程
        self.tcpCliSock = tcpCliSock
        self.BUFSIZ = BUFSIZ

    def run(self):
        while True:
            data = tcpCliSock.recv(self.BUFSIZ)
            if not data:
                tcpCliSock.close()
                root.destroy()
            else:
                Output.insert(END, data.decode('utf-8'))


def sendMessage():
    # 发送消息
    msg = Input.get('1.0', END)
    tcpCliSock.send(dumps({
        'name': NAME,
        'msg' : msg
    }).encode('utf-8'))
    Input.delete('1.0', END)


def onClosing():
    tcpCliSock.shutdown(SHUT_WR)


HOST = 'localhost'
POST = 3000
BUFSIZ = 1024
ADDR = (HOST, POST)
NAME = choice(['业冰蝶','同静槐','骑婷然','牧建章','锐理全','达悠逸','倪长逸','侨玉书','符天韵','树修敏'])

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

root = Tk()
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.geometry('+{}+{}'.format((sw-430)//2, (sh-340)//2))
root.title('Python聊天群 ({})'.format(NAME))

frameT = Frame(root, width=460, height=320)
frameB = Frame(root, width=460, height=80)
frameT.pack(expand='yes', fill='both')
frameB.pack(expand='yes', fill='both')

Input = Text(frameB, height=6)
Output = Text(frameT)
Input.pack(expand='yes', fill='both')
Output.pack(expand='yes', fill='both')

btnFrame = Frame(frameB, height=24, background='White')
btnFrame.pack(expand='yes', fill='both')

Button(btnFrame, text='发送', width=8, bg='DodgerBlue', fg='White', command=sendMessage).pack(side=RIGHT)

ReceiveThread(tcpCliSock).start()  # 启动消息接收线程
root.protocol("WM_DELETE_WINDOW", onClosing)  # 退出时处理
root.mainloop()