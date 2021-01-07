import curses

WHITE = 0
CYAN = 1
RED = 2

def init_colors():
    curses.init_pair(WHITE, curses.COLOR_WHITE, -1)
    curses.init_pair(CYAN, curses.COLOR_CYAN, -1)
    curses.init_pair(RED, curses.COLOR_RED, -1)

class ScrollView:
    def __init__(self, w, h, x, y):
        self.win = curses.newwin(h, w, y, x)
        self.yoff = 0
        self.w = w
        self.h = h
        self.lines = []

    def set_text(self, text):
        self.lines = text

    def refresh(self):
        self.win.clear()

        lines_intersect = self.lines[self.yoff:self.h]
        for yd, line in reversed(list(enumerate(lines_intersect))):
            y = + self.h - len(lines_intersect) + yd
            self.win.addstr(y, 0, line)

        self.win.refresh()

class StatusView:
    def __init__(self, w, y):
        self.win = curses.newwin(4, w, y, 0)
        self.win.keypad(True)
        self.win.timeout(100)
        self.msg = ":)"
        self.location = "/"
        self.inl = "? "

    def refresh(self):
        self.win.clear()
        self.win.addstr(1, 0, self.msg)
        self.win.addstr(2, 0, self.location)
        self.win.addstr(3, 0, self.inl)
        self.win.move(3, len(self.inl))
        self.win.refresh()

class Gui:
    def __init__(self):
        #init_colors()

        self.status = StatusView(curses.COLS, curses.LINES - 4)
        self.messages = ScrollView((curses.COLS + 1) // 2, curses.LINES - 4,
                0, 0)
        self.tabs = ScrollView(curses.COLS // 2, curses.LINES - 4,
                (curses.COLS + 1) // 2, 0)

        self.status.msg = "Connecting..."

        self.messages.refresh()
        self.tabs.refresh()
        self.status.refresh()

    def getch(self):
        return self.status.win.getch()

    def set_msg(self, msg):
        self.status.msg = msg
        self.status.refresh()
