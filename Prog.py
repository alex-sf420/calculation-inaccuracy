from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import ttk
from ttkthemes import ThemedTk
from math import sqrt
from decimal import Decimal, ROUND_HALF_UP

PADX = 8
PADY = 8

class Main():
    """Содержит функции для расчета погрешности и отображения необходимого
    количества строк для частей/помещений
    """
    def __init__(self):
        """Определяем текущее значение точности, отображенных строк,
        списка отображаемых строк и значение погрешности
        """
        self.accuracy = 0.01
        self.totalrows = 0
        self.listrows = []
        self.result = 0

    def set_row(self):
        """Выполняет отображение необходимого количества строк для
        частей/помещений
        """
        self.number_row_to_paste = self.totalrows + 7
        try:
            self.row_add = int(sbox1.sbox.get())
        except ValueError:
            return
        if self.row_add < 1:
            return
        if self.row_add > self.totalrows:
            for i in range(self.row_add - self.totalrows):
                label10 = ttk.Label(frame1,
                                    text = ("{}".format(self.totalrows + i + 1)))
                label10.grid(row = (self.number_row_to_paste + i), column = 0,
                             padx = 0, pady = 0, ipadx = 40, sticky = W)
                ent3 = Entries((self.number_row_to_paste + i), 0, E)
                ent4 = Entries((self.number_row_to_paste + i), 1, W)
                self.listrows.append((ent3, ent4, label10))
            if self.row_add <= 14:
                draw.configure(height = ent1.ent.winfo_height() * self.row_add,
                               scrollregion = (0, 0, 0, 0))
            else:
                draw.configure(height = 310, scrollregion = (0, 0, 0,
                               ent1.ent.winfo_height() * self.row_add))
            self.totalrows = self.row_add
            sep3.sep.grid(row = self.totalrows + 7, column = 0, columnspan = 4,
                      padx = PADX, pady = PADY, sticky = EW)
        elif self.row_add > self.totalrows:
            return
        else:
            self.number_row_to_paste = self.totalrows - self.row_add
            for i in range(self.totalrows - self.row_add):
                self.listrows[-1][0].ent.destroy()
                self.listrows[-1][1].ent.destroy()
                self.listrows[-1][2].destroy()
                self.listrows.pop()
            self.totalrows = self.row_add
            sep3.sep.grid(row = self.totalrows + 7, column = 0, columnspan = 4,
                      padx = PADX, pady = PADY, sticky = EW)
            if self.row_add <= 14:
                draw.configure(height = ent1.ent.winfo_height() * self.row_add,
                               scrollregion = (0, 0, 0, 0))
            else:
                draw.configure(height = 310, scrollregion = (0, 0, 0,
                               ent1.ent.winfo_height() * self.row_add))

    def calc_result(self):
        """Производит рассчет погрешности и выводит полученное значение в
        соответствующей метке
        """
        try:
            levels = int(sbox2.sbox.get())
        except ValueError:
            return
        if levels < 1:
            return
        parameters = []
        try:
            for ent in self.listrows:
                width = (ent[0].ent.get())
                if not width and len(parameters) == 0:
                    return
                if not width:
                    break
                if "," in width:
                    width = width.replace("," ,".")
                width = float(width)
                height = (ent[1].ent.get())
                if "," in height:
                    height = height.replace(",",".")
                height = float(height)
                parameters.append(width**2 + height**2)
        except ValueError:
            return
        self.result = Decimal('{}'.format(self.accuracy*sqrt(sum(parameters)*levels)))
        self.result = self.result.quantize(Decimal("1.0"), ROUND_HALF_UP)
        if self.result == 0.0:
            label9.lab["text"] = ("0,1 кв.м.")
        else:
            label9.lab["text"] = (str(self.result) + " " + "кв.м.")

        print(self.result)


    def check_accurasy(self, event):
        """Регулирует значение кривизны стен"""
        if event == "1 см":
            self.accuracy = 0.01
        elif event == "2 см":
            self.accuracy = 0.02
        elif event == "3 см":
            self.accuracy = 0.03

    def calc_built_up(self):
        """Рассчитывает погрешность определения площади застройки на
        основе загруженных координат
        """
        try:
            file_name = fd.askopenfilename()  # загружаем координаты в
            with open(file_name) as f:        # формате .txt
                coords = f.readlines()
        except FileNotFoundError:
            return
        coords.pop()
        for i in range(len(coords)):          # меняем запятые на точки,
            if "," in coords[i]:
                coords[i] = coords[i].replace("," ,".")
            coords[i] = coords[i].rstrip('\n')
            coords[i] = coords[i].split()
        coords.insert(0, coords[-1])          # дополняем список первым и
        coords.append(coords[1])              # последним элементом
        tmp_list = []
        for i in range(1, len(coords)-1):
            tmp_list.append((float(coords[i-1][1]) - float(coords[i+1][1]))**2 +\
                    (float(coords[i-1][2]) - float(coords[i+1][2]))**2)
        result = Decimal('{}'.format(0.35*0.1*sqrt(sum(tmp_list))))
        result = result.quantize(Decimal("1.0"), ROUND_HALF_UP)
        if result == 0.0:
            label9.lab["text"] = ("0,1 кв.м.")
        else:
            label9.lab["text"] = (str(result) + " " + "кв.м.")


class Buttons:
    """Отображает кнопки"""
    def __init__(self, text, command, row, column, padx = PADX, pady = PADY):
        self.but = ttk.Button(frame, text = text, command = command)
        self.but.grid(row = row, column = column, padx = padx,
                    pady = pady)


class Lables:
    """Отображает метки"""
    def __init__(self, text, row, column, sticky = None, columnspan = None,
                 padx = PADX, pady = PADY, font = None):
        self.lab = ttk.Label(frame, text = text, font = font)
        self.lab.grid(row = row, column = column,
                    columnspan = columnspan, padx = padx,
                    pady = pady, sticky = sticky)


class Entries:
    """Отображает поля"""
    def __init__(self, row, column, sticky):
        self.ent = ttk.Entry(frame1, width = 12)
        self.ent.grid(row = row, column = column,
                    sticky = sticky)


class Separators:
    """Отображает разделительные линии"""
    def __init__(self, row, column, rowspan = None, columnspan = None,
                 padx = None, pady = None, orient = None):
        self.sep = ttk.Separator(frame, orient = orient)
        self.sep.grid(row = row, column = column,
                      rowspan = rowspan, columnspan = columnspan,
                      padx = padx, pady = pady, sticky = (N,E,S,W))


class Sboxes:
    """Отображает поля выбора значений"""
    def __init__(self, from_, to, row, column, padx = PADX, pady = PADY):
        self.sbox = ttk.Spinbox(frame, width = 5, from_ = from_,
                                to = to)
        self.sbox.insert(0, 1)
        self.sbox.grid(row = row, column = column, padx = padx,
                   pady = pady)
list
root = ThemedTk(theme = "itft1")
root.title("Расчет СКП площади")

table = Main()


frame = ttk.Frame()
frame.grid(sticky=(N,E,S,W))


draw = Canvas(frame, width = 173, height = 20, bd=0, highlightthickness=0)
draw.config(scrollregion = draw.bbox("ALL"))
draw.sbar = Scrollbar(frame, orient=VERTICAL)
frame1 = ttk.Frame(draw)
draw.create_window(0, 0, window=frame1, width=173, anchor=N+W)

draw['yscrollcommand'] = draw.sbar.set
draw.sbar['command'] = draw.yview
draw.sbar.grid(row = 7, column = 1, sticky = N+S+E, padx = 0, pady = 0)
draw.grid(row = 7, column = 0, columnspan = 2, sticky = E, padx = 0, pady = 0)

label1 = Lables("Количество частей/помещений:", 1, 0, E)
label2 = Lables("Количество этажей:", 2, 0, E)
label3 = Lables("Кривизна стен:", 3, 0, E)
label4 = Lables("Размеры частей/помещений:", 5, 0, SE, columnspan = 2, pady = 5)
label5 = Lables("Длина, м", 6, 0, SE, pady = 0)
label6 = Lables("Ширина, м", 6, 1, SW, pady = 0)
label7 = ttk.Label(frame1, text = "1")
label7.grid(row = 7, column = 0, padx = 0, pady = 0, ipadx = 40, sticky = W)
label8 = Lables("Результат:", 5, 3, font = ('Sans','10','bold'))
label9 = Lables((str(table.result) + " " + "кв.м."), 6, 3,
                 font = ('Sans','15','bold'))

button1 = Buttons("Отобразить", table.set_row, 1, 3)
button2 = Buttons("Рассчитать", table.calc_result, 2, 3)
button3 = Buttons("S застройки", table.calc_built_up, 3, 3)

sbox1 = Sboxes(1, 100, 1, 1)
sbox2 = Sboxes(1, 50, 2, 1)

variable = StringVar()
options = ["1 см", "2 см", "3 см"]
variable.set(options[0])
opt = ttk.OptionMenu(frame, variable, '', *options, command = table.check_accurasy)
opt.grid(row = 3, column = 1, padx = PADX, pady = PADY)

ent1 = Entries(7, 0, E)
ent2 = Entries(7, 1, W)
table.listrows.append((ent1, ent2))
Main.totalrows = 1


sep1 = Separators(0, 2, rowspan = 100, orient = VERTICAL)
sep2 = Separators(4, 0, columnspan = 4, padx = PADX, pady = PADY)
sep3 = Separators(8, 0, columnspan = 4, padx = PADX, pady = PADY)


root.update_idletasks()
s = root.geometry()
s = s.split('+')
s = s[0].split('x')
width_root = int(s[0])
height_root = int(s[1])
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2
h = h // 2
w = w - width_root // 2
h = h - height_root // 2
root.geometry('+{}+{}'.format(w, h))
root.resizable(False, False)

root.mainloop()
