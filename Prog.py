from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from ttkthemes import ThemedTk
from math import sqrt
from decimal import Decimal, ROUND_HALF_UP


class Frames:
    """Создает фреймы"""

    def __init__(self):
        self.frame1 = ttk.Frame()
        self.frame1.grid(sticky=(N, E, S, W))

        self.draw = Canvas(self.frame1, width=173, height=20, bd=0, highlightthickness=0)
        self.frame2 = ttk.Frame(self.draw)
        self.draw.config(scrollregion=(0, 0, 0, 20))
        self.draw.sbar = ttk.Scrollbar(self.frame1, orient=VERTICAL)

        self.draw.create_window(0, 0, window=self.frame2, anchor=N + W)
        self.draw['yscrollcommand'] = self.draw.sbar.set
        self.draw.sbar['command'] = self.draw.yview
        self.draw.sbar.grid(row=7, column=1, sticky=N + S + E, padx=0, pady=0)
        self.draw.grid(row=7, column=0, columnspan=2, sticky=E, padx=0, pady=0)


class Buttons:
    """Отображает кнопки"""

    def __init__(self, parent, main):
        self.parent = parent

        self.but1 = ttk.Button(self.parent, text="Отобразить", command=main.set_row)
        self.but1.grid(row=1, column=3, padx=Main.padx)
        self.but2 = ttk.Button(self.parent, text="Рассчитать", command=main.calc_result)
        self.but2.grid(row=2, column=3, padx=Main.padx)
        self.but3 = ttk.Button(self.parent, text="S застройки", command=main.calc_built_up)
        self.but3.grid(row=3, column=3, padx=Main.padx)


class Lables:
    """Отображает метки, динамическая перерисовка производится
    в методе set_row класса Main"""

    def __init__(self, parent1, parent2, main):
        self.parent1 = parent1
        self.parent2 = parent2
        self.label1 = ttk.Label(self.parent1, text="Количество частей/помещений:")
        self.label1.grid(row=1, column=0, sticky=E, padx=Main.padx, pady=Main.pady)
        self.label2 = ttk.Label(self.parent1, text="Количество этажей:")
        self.label2.grid(row=2, column=0, sticky=E, padx=Main.padx, pady=Main.pady)
        self.label3 = ttk.Label(self.parent1, text="Кривизна стен:")
        self.label3.grid(row=3, column=0, sticky=E, padx=Main.padx, pady=Main.pady)
        self.label4 = ttk.Label(self.parent1, text="Размеры частей/помещений:")
        self.label4.grid(row=5, column=0, columnspan=2, sticky=SE, padx=Main.padx, pady=5)
        self.label5 = ttk.Label(self.parent1, text="Длина, м")
        self.label5.grid(row=6, column=0, sticky=SE, padx=Main.padx)
        self.label6 = ttk.Label(self.parent1, text="Ширина, м")
        self.label6.grid(row=6, column=1, sticky=SW, padx=Main.padx)
        self.label7 = ttk.Label(self.parent2, text="1")
        self.label7.grid(row=7, column=0, sticky=W, ipadx=40)
        self.label8 = ttk.Label(self.parent1, text="Результат:", font=('Sans', '10', 'bold'))
        self.label8.grid(row=5, column=3, padx=Main.padx, pady=Main.pady)
        self.label9 = ttk.Label(self.parent1, text=(str(main.result) + " " + "кв.м."),
                                font=('Sans', '15', 'bold'))
        self.label9.grid(row=6, column=3, padx=Main.padx, pady=Main.pady)
        

class Entries:
    """Отображает поля, динамическая перерисовка производится
    в методе set_row класса Main"""

    def __init__(self, parent, main):
        self.parent = parent
        self.width = 12
        self.ent1 = ttk.Entry(self.parent, width=self.width)
        self.ent1.grid(row=7, column=0, sticky=E)
        self.ent2 = ttk.Entry(self.parent, width=self.width)
        self.ent2.grid(row=7, column=1, sticky=W)

        main.listrows.append((self.ent1, self.ent2))
        main.totalrows = 1


class Separators:
    """Отображает разделительные линии, динамическая перерисовка производится
    в методе set_row класса Main
    """

    def __init__(self, parent):
        self.parent = parent
        self.sep1 = ttk.Separator(self.parent, orient=VERTICAL)
        self.sep1.grid(row=0, column=2, rowspan=100, sticky=(N, E, S, W))
        self.sep2 = ttk.Separator(self.parent)
        self.sep2.grid(row=4, column=0, columnspan=4, padx=Main.padx, pady=Main.pady,
                       sticky=(N, E, S, W))
        self.sep3 = ttk.Separator(self.parent)
        self.sep3.grid(row=8, column=0, columnspan=4, padx=Main.padx, pady=Main.pady,
                       sticky=(N, E, S, W))


class Sboxes:
    """Отображает поля выбора значений"""

    def __init__(self, parent):
        self.parent = parent
        self.width = 5
        self.sbox1 = ttk.Spinbox(self.parent, width=self.width, from_=1, to=100)
        self.sbox1.insert(0, 1)
        self.sbox1.grid(row=1, column=1, padx=Main.padx, pady=Main.pady)
        self.sbox2 = ttk.Spinbox(self.parent, width=self.width, from_=1, to=50)
        self.sbox2.insert(0, 1)
        self.sbox2.grid(row=2, column=1, padx=Main.padx, pady=Main.pady)


class Optionmenu:
    def __init__(self, parent, main):
        self.parent = parent
        self.variable = StringVar()
        self.options = ["1 см", "2 см", "3 см"]
        self.variable.set(self.options[0])
        self.opt = ttk.OptionMenu(self.parent, self.variable, '', *self.options,
                                  command=main.check_accurasy)
        self.opt.grid(row=3, column=1, padx=Main.padx, pady=Main.pady)


class Main:
    """Содержит функции для расчета погрешности и отображения необходимого
    количества строк для частей/помещений
    """

    padx = 8
    pady = 8
    
    def __init__(self, parent):
        self.parent = parent
        self.number_row_to_paste = 0
        self.accuracy = 0.01  # точность
        self.totalrows = 0  # количество отображаемых строк/полей
        self.listrows = []  # список строк/полей
        self.result = 0  # результат рассчета погрешности
        self.frames = Frames()
        self.buttons = Buttons(parent=self.frames.frame1, main=self)
        self.lables = Lables(parent1=self.frames.frame1, parent2=self.frames.frame2, main=self)
        self.entries = Entries(parent=self.frames.frame2, main=self)
        self.separators = Separators(parent=self.frames.frame1)
        self.sboxes = Sboxes(parent=self.frames.frame1)
        self.optionmenu = Optionmenu(parent=self.frames.frame1, main=self)


    def set_row(self):
        """Выполняет отображение необходимого количества строк для
        частей/помещений
        """

        self.number_row_to_paste = self.totalrows + 7  # номер row в grid(), в которое будет
                                                       # добавляться следующаая строка/поле
        try:
            row_add = int(self.sboxes.sbox1.get())   # количество строк/полей, которое нужно отразить
        except ValueError:
            return
        if row_add < 1:
            return
        if row_add > self.totalrows:
            for i in range(row_add - self.totalrows):
                label10 = ttk.Label(self.frames.frame2,
                                    text=("{}".format(self.totalrows + i + 1)))
                label10.grid(row=(self.number_row_to_paste + i), column=0,
                             padx=0, pady=0, ipadx=40, sticky=W)
                ent3 = ttk.Entry(self.frames.frame2, width=self.entries.width)
                ent3.grid(row=(self.number_row_to_paste + i), column=0, sticky=E)
                ent4 = ttk.Entry(self.frames.frame2, width=self.entries.width)
                ent4.grid(row=(self.number_row_to_paste + i), column=1, sticky=W)
                self.listrows.append((ent3, ent4, label10))
            if row_add <= 14:
                self.frames.draw.configure(height=self.entries.ent1.winfo_height() * row_add,
                                      scrollregion=(0, 0, 0, self.entries.ent1.winfo_height() * row_add))
            else:
                self.frames.draw.configure(height=310,
                                      scrollregion=(0, 0, 0, self.entries.ent1.winfo_height() * row_add))

            self.totalrows = row_add
            self.separators.sep3.grid(row=self.totalrows + 7, column=0, columnspan=4,
                                 padx=Main.padx, pady=Main.pady, sticky=EW)

        elif row_add > self.totalrows:
            return
        else:
            self.number_row_to_paste = self.totalrows - row_add
            for i in range(self.totalrows - row_add):
                self.listrows[-1][0].destroy()
                self.listrows[-1][1].destroy()
                self.listrows[-1][2].destroy()
                self.listrows.pop()
            self.totalrows = row_add
            self.separators.sep3.grid(row=self.totalrows + 7, column=0, columnspan=4,
                                 padx=Main.padx, pady=Main.pady, sticky=EW)
            if row_add <= 14:
                self.frames.draw.configure(height=self.entries.ent1.winfo_height() * row_add,
                                      scrollregion=(0, 0, 0, self.entries.ent1.winfo_height() * row_add))
            else:
                self.frames.draw.configure(height=310,
                                      scrollregion=(0, 0, 0, self.entries.ent1.winfo_height() * row_add))

    def calc_result(self):
        """Производит рассчет погрешности и выводит полученное значение в
        соответствующей метке
        """
        try:
            levels = int(self.sboxes.sbox2.get())
        except ValueError:
            return
        if levels < 1:
            return
        parameters = []
        try:
            for ent in self.listrows:
                width = (ent[0].get())
                if not width and len(parameters) == 0:
                    return
                if not width:
                    break
                if "," in width:
                    width = width.replace(",", ".")
                width = float(width)
                height = (ent[1].get())
                if "," in height:
                    height = height.replace(",", ".")
                height = float(height)
                parameters.append(width ** 2 + height ** 2)
        except ValueError:
            return
        result = Decimal('{}'.format(self.accuracy * sqrt(sum(parameters) * levels)))
        result = result.quantize(Decimal("1.0"), ROUND_HALF_UP)
        if result == 0.0:
            self.lables.label9["text"] = "0,1 кв.м."
        else:
            self.lables.label9["text"] = (str(result) + " " + "кв.м.")

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
            with open(file_name) as f:  # формате .txt
                coords = f.readlines()
        except FileNotFoundError:
            return
        coords.pop()
        for i in range(len(coords)):  # меняем запятые на точки,
            if "," in coords[i]:
                coords[i] = coords[i].replace(",", ".")
            coords[i] = coords[i].rstrip('\n')
            coords[i] = coords[i].split()
        coords.insert(0, coords[-1])  # дополняем список первым и
        coords.append(coords[1])      # последним элементом
        tmp_list = []
        for i in range(1, len(coords) - 1):
            tmp_list.append((float(coords[i - 1][1]) - float(coords[i + 1][1])) ** 2 +
                            (float(coords[i - 1][2]) - float(coords[i + 1][2])) ** 2)
        result = Decimal('{}'.format(0.35 * 0.1 * sqrt(sum(tmp_list))))
        result = result.quantize(Decimal("1.0"), ROUND_HALF_UP)
        if result == 0.0:
            self.lables.label9["text"] = "0,1 кв.м."
        else:
            self.lables.label9["text"] = (str(result) + " " + "кв.м.")


class Start:
    def __init__(self):
        self.root = ThemedTk(theme="itft1")
        self.root.title("Расчет СКП площади")
        
        self.main = Main(self)

        self.centering()
        self.root.mainloop()

    def centering(self):
        self.root.update_idletasks()
        sizes = self.root.geometry()
        sizes = sizes.split('+')
        sizes = sizes[0].split('x')
        width_root = int(sizes[0])
        height_root = int(sizes[1])
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - width_root // 2
        height = height - height_root // 2
        self.root.geometry('+{}+{}'.format(width, height))
        self.root.resizable(False, False)


if __name__ == "__main__":
    Start()

