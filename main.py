import curses, discord, threading, os

from queue import Queue, Empty

from gui import *

from_dc_q, to_dc_q = Queue(10), Queue(10)

class FromDCMsg:
    STATUS_CHANGE = 0

    def __init__(self, msgtype, msg):
        self.type = msgtype
        self.msg = msg

class Mode:
    NORMAL = 0
    INSERT = 1
    VISUAL = 2

def handle_message(gui, mode, ob):
    if ob.type == FromDCMsg.STATUS_CHANGE:
        gui.set_msg(ob.msg)

def handle_messages(gui, mode):
    while True:
        try:
            handle_message(gui, mode, from_dc_q.get_nowait())

        except Empty:
            return

def main_loop(stdscr):
    gui = Gui()
    mode = Mode.NORMAL

    while True:
        handle_messages(gui, mode)

        c = gui.getch() # blocks for up to 100 ms
        if c == -1:
            continue

        c = chr(c)

        if mode == Mode.NORMAL:
            if c == 'q':
                curses.nocbreak()
                curses.echo()
                curses.endwin()
                os._exit(0)

def main():
    curses.wrapper(main_loop)

t = threading.Thread(target=main, args=())
t.start()

client = discord.Client()

@client.event
async def on_ready():
    from_dc_q.put(FromDCMsg(FromDCMsg.STATUS_CHANGE, "Connected."))

try:
    client.run(__import__("secret").secret)

except:
    curses.nocbreak()
    curses.echo()
    curses.set_curs(1)
    curs.endwin()
