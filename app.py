import tkinter as tk
from tkinter import font
from tkinter import messagebox
from cuckoohash import CockooHash


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hashing")
        self.root.geometry("800x600")

        self.key = tk.StringVar()
        self.value = tk.StringVar()

        # 添加标签
        self.label1 = tk.Label(self.root, text="键")
        self.label2 = tk.Label(self.root, text="值")
        self.entry1 = tk.Entry(self.root, textvariable=self.key)
        self.entry2 = tk.Entry(self.root, textvariable=self.value)

        self.btnInsert = tk.Button(self.root, text="插入", command=self.insert)
        self.btnRemove = tk.Button(self.root, text="删除", command=self.remove)

        self.label3 = tk.Label(self.root, text="H1(x) = x mod 8")
        self.label4 = tk.Label(self.root, text="H2(x) = (x div 8) mod 8")

        self.canvas = tk.Canvas(self.root)
        self.canvas.bind("<Button-1>", self.continue_show)
        self.pause = False

        self.ch = CockooHash(8)
        # self.ch.set(89, 0)
        # self.ch.set(50, 0)
        # self.ch.set(3, 0)
        # self.ch.set(93, 0)
        # self.ch.set(13, 0)

    def run(self):
        self.place()
        self.root.mainloop()

    def place(self):
        self.label1.place(x=100, y=50, height=20)
        self.label2.place(x=300, y=50, height=20)
        self.entry1.place(x=130, y=50, height=20)
        self.entry2.place(x=330, y=50, height=20)
        self.btnInsert.place(x=500, y=50, width=70, height=20)
        self.btnRemove.place(x=600, y=50, width=70, height=20)

        self.label3.place(x=200, y=120)
        self.label4.place(x=400, y=120)
        self.canvas.place(x=200, y=150, width=400, height=400)

        self.init_canvas()

    def init_canvas(self):
        for i in self.canvas.find_all():
            self.canvas.delete(i)

        self.create_board(x=30, y=30)
        self.create_board(x=260, y=30)

        self.init_text(x=15, y=30)
        self.init_text(x=315, y=30)

        self.refresh_text()

    def create_board(self, x, y):
        self.canvas.create_line(x, y, x, y + 40 * 8)
        self.canvas.create_line(x + 40, y, x + 40, y + 40 * 8)
        for i in range(9):
            self.canvas.create_line(x, y + i * 40, x + 40, y + i * 40)

    def init_text(self, x, y):
        for i in range(8):
            self.canvas.create_text(x, y + 40 * i + 20, text=str(i))

    def set_text(self, bn, arr):
        for i in range(8):
            x = 30 if bn == 0 else 260
            y = 30 + i * 40
            x += 20
            y += 20
            if arr[i] is not None:
                self.canvas.create_text(x, y, text=str(arr[i]), font=font.Font(size=18))

    def refresh_text(self):
        self.set_text(0, self.get_keys(0))
        self.set_text(1, self.get_keys(1))

    def create_beginning_arrow(self, index, key):
        x0 = 170
        y0 = 350
        x1 = 70
        y1 = 50 + index * 40
        self.canvas.create_line(x0, y0, x1, y1, arrow=tk.LAST, width=2)
        self.canvas.create_text(x0, y0+20, text="H1({})={}".format(key, index))

    def create_arrow(self, begin_index, end_index, direction):
        x0 = 70
        y0 = 50 + begin_index * 40
        x1 = 260
        y1 = 50 + end_index * 40
        d = tk.LAST if direction == 1 else tk.FIRST
        self.canvas.create_line(x0, y0, x1, y1, arrow=d, width=2)

    def insert(self):
        # print(self.key.get(), self.value.get())
        try:
            key = int(self.key.get())
            val = int(self.value.get())
        except ValueError:
            messagebox.showwarning("提示", "输入键值不正确")
            return
        self.ch.set(key, val)
        records = self.ch.change_list
        if len(records) > 1:
            self.create_beginning_arrow(records[len(records)-1].index, records[len(records)-1].key)
            for i in range(0, len(records) - 1):
                bi, ei = records[i].index, records[i + 1].index
                if records[i].bucket_num == 1:
                    bi, ei = ei, bi
                self.create_arrow(bi, ei, records[i].bucket_num)
                self.root.update()
            self.pause = True
        else:
            self.init_canvas()

    def remove(self):
        try:
            key = int(self.key.get())
        except ValueError:
            messagebox.showwarning("提示", "请输入正确的键")
            return

        self.ch.remove(key)
        self.init_canvas()

    def get_keys(self, bn):
        return list(map(lambda item: item.key, self.ch.containers[bn]))

    def continue_show(self, event):
        if self.pause:
            self.pause = False
            for i in self.canvas.find_all():
                self.canvas.delete(i)
            self.init_canvas()


if __name__ == '__main__':
    app = App()
    app.run()
