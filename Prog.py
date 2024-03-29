from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from ttkthemes import ThemedTk
from math import sqrt
from decimal import Decimal, ROUND_HALF_UP
import csv

class MainFrame:
    """
    Создает основное окно и виджеты
    """
    def __init__(self, main):
        self.make_frame()
        self.make_buttons(main)
        self.make_lables(main)
        self.make_entries(main)
        self.make_separators()
        self.make_sboxes(main)
        self.make_option_menu(main)
        self.make_text_area()
        self.make_tooltips()

    def make_frame(self):
        """
        Создает фреймы
        """
        self.frame1 = ttk.Frame()
        self.frame1.grid(sticky=(N, E, S, W))

        self.draw = Canvas(self.frame1, width=180, height=63, bd=0, highlightthickness=0)
        self.frame2 = ttk.Frame(self.draw)
        self.draw.config(scrollregion=(0, 0, 0, 63))
        self.draw.sbar1 = ttk.Scrollbar(self.frame1, orient=VERTICAL)

        self.draw.create_window(0, 0, window=self.frame2, anchor=N + W)
        self.draw['yscrollcommand'] = self.draw.sbar1.set
        self.draw.sbar1['command'] = self.draw.yview
        self.draw.sbar1.grid(row=7, column=1, sticky=N + S + E, padx=0, pady=0)
        self.draw.grid(row=7, column=0, columnspan=2, sticky=E, padx=0, pady=0)

    def make_buttons(self, main):
        """
        Создает кнопки
        """
        self.but1 = ttk.Button(self.frame1, text="Отобразить", command=main.set_row)
        self.but1.grid(row=3, column=3, padx=Main.padx, pady=Main.pady)
        self.but2 = ttk.Button(self.frame1, text="Рассчитать", command=main.calc_result)
        self.but2.grid(row=1, column=3, padx=Main.padx, pady=Main.pady)
        self.but3 = ttk.Button(self.frame1, text="S застройки", command=main.calc_built_up)
        self.but3.grid(row=2, column=3, padx=Main.padx, pady=Main.pady)

    def make_lables(self, main):
        """
        Создает метки, динамическая перерисовка производится
        в методе set_row класса Main
        """
        self.label1 = ttk.Label(self.frame1, text="Количество пар длина/ширина:")
        self.label1.grid(row=3, column=0, sticky=E, padx=Main.padx, pady=Main.pady)
        self.label2 = ttk.Label(self.frame1, text="Количество этажей:")
        self.label2.grid(row=2, column=0, sticky=E, padx=Main.padx, pady=Main.pady)
        self.label3 = ttk.Label(self.frame1, text="Кривизна стен:")
        self.label3.grid(row=1, column=0, sticky=E, padx=Main.padx, pady=Main.pady)
        self.label4 = ttk.Label(self.frame1, text="Размеры помещений:  ")
        self.label4.grid(row=5, column=0, columnspan=2, sticky=E, padx=16, pady=5)
        self.label5 = ttk.Label(self.frame1, text="Длина, м  ")
        self.label5.grid(row=6, column=0, sticky=SE)
        self.label6 = ttk.Label(self.frame1, text="Ширина, м")
        self.label6.grid(row=6, column=1, sticky=SW, padx=Main.padx)
        self.label8 = ttk.Label(self.frame1, text="Результат:", font=('Sans', '11', 'bold'))
        self.label8.grid(row=5, column=3, sticky=S, padx=Main.padx, pady=Main.pady)
        self.label9 = ttk.Label(self.frame1, text=(str(main.result) + " " + "кв.м."),
                                font=('Sans', '15', 'bold'))
        self.label9.grid(row=6, column=3, padx=0, pady=0)
        self.label10 = ttk.Label(self.frame1, text="Формула:")
        self.label10.grid(row=10, column=0, sticky=W, padx=15, pady=2)

    def make_entries(self, main):
        """
        Создает поля, динамическая перерисовка производится
        в методе set_row класса Main
        """
        self.entry_width = 11
        for i in range(3):
            label = ttk.Label(self.frame2, text=i + 1)
            label.grid(row=7 + i, column=0, sticky=W, ipadx=43)
            ent1 = ttk.Entry(self.frame2, width=self.entry_width)
            ent1.grid(row=7 + i, column=0, sticky=E)
            ent1.bind("<Return>", main.calc_result)
            ent2 = ttk.Entry(self.frame2, width=self.entry_width)
            ent2.grid(row=7 + i, column=1, sticky=W)
            ent2.bind("<Return>", main.calc_result)
            main.listrows.append((ent1, ent2, label))
        main.totalrows = 3

    def make_separators(self):
        """
        Создает разделительные линии, динамическая перерисовка производится
        в методе set_row класса Main
        """
        self.sep1 = ttk.Separator(self.frame1, orient=VERTICAL)
        self.sep1.grid(row=0, column=2, rowspan=11, sticky=(N, E, S, W))
        self.sep2 = ttk.Separator(self.frame1)
        self.sep2.grid(row=4, column=0, columnspan=4, padx=Main.padx,
                       sticky=(N, E, S, W))
        self.sep3 = ttk.Separator(self.frame1)
        self.sep3.grid(row=12, column=0, columnspan=4, padx=Main.padx, pady=Main.pady,
                       sticky=(N, E, S, W))

    def make_sboxes(self, main):
        """
       Создает поля выбора значений
        """
        self.width = 5
        self.sbox1 = ttk.Spinbox(self.frame1, width=self.width, from_=3, to=100)
        self.sbox1.insert(0, 3)
        self.sbox1.grid(row=3, column=1, sticky=W, padx=Main.padx, pady=Main.pady)
        self.sbox1.bind("<Return>", main.set_row)
        self.sbox2 = ttk.Spinbox(self.frame1, width=self.width, from_=1, to=50)
        self.sbox2.insert(0, 1)
        self.sbox2.grid(row=2, column=1, sticky=W, padx=Main.padx, pady=Main.pady)
        self.sbox2.bind("<Return>", main.calc_result)

    def make_option_menu(self, main):
        """
        Создает всплывающие меню
        """
        self.variable = StringVar()
        self.options = ["1 см", "2 см", "3 см"]
        self.variable.set(self.options[0])
        self.opt = ttk.OptionMenu(self.frame1, self.variable, '', *self.options,
                                  command=main.check_accurasy)
        self.opt.grid(row=1, column=1, padx=Main.padx, pady=Main.pady)

    def make_text_area(self):
        """
        Создает тектовое поле
        """
        self.text1 = Text(self.frame1, width=45, height=4)
        self.text1.grid(row=11, column=0, columnspan=4, padx=15, pady=2, )
        sbar2 = ttk.Scrollbar(self.frame1, command=self.text1.yview)
        sbar2.grid(row=11, column=3, sticky=N + S + E, padx=0, pady=2)
        self.text1.config(yscrollcommand=sbar2.set)

    def make_tooltips(self):
        class ToolTip:
            """
            Отображает всплывающие подсказки
            """

            def __init__(self, widget=None, text='widget info'):
                if widget:
                    self.waittime = 1000
                    self.wraplength = 180
                    self.widget = widget
                    self.text = text
                    self.widget.bind("<Enter>", self.enter)
                    self.widget.bind("<Leave>", self.leave)
                    self.widget.bind("<ButtonPress>", self.leave)
                    self.id = None
                    self.tip = None

            @staticmethod
            def create_tips(main):
                ToolTip(main.but1, '''Отображает количество строк раздела "Размеры помещений" на основании значения, указанного в поле "Количество пар длина/ширина"''')
                ToolTip(main.but2, '''Выводит результат расчета СКП площади на основании данных раздела "Размеры помещений" с учетом заданного количества этажей и кривизны стен''')
                ToolTip(main.but3, '''Выводит результат расчета СКП площади застройки для выбранного каталога координат в формате .txt (только для одноконтурного объекта)''')
                ToolTip(main.label1, 'Укажите количество пар длина/ширина помещений')
                ToolTip(main.label2, 'Укажите количество этажей объекта, в т.ч. подземных')
                ToolTip(main.label3, 'Выберите значение кривизны стен')

            def enter(self, event):
                self.id = self.widget.after(self.waittime, self.showtip)

            def leave(self, event):
                self.widget.after_cancel(self.id)
                if self.tip:
                    self.tip.destroy()

            def showtip(self):
                x, y = self.widget.bbox("insert")[:2]
                x += self.widget.winfo_rootx() + 45
                y += self.widget.winfo_rooty() + 30
                self.tip = Toplevel(self.widget)
                self.tip.wm_overrideredirect(True)
                self.tip.wm_geometry("+%d+%d" % (x, y))
                label = Label(self.tip, text=self.text, justify='left',
                              background="#ffffff", relief='solid', borderwidth=1,
                              wraplength=self.wraplength)
                label.pack(ipadx=1)
        ToolTip().create_tips(main=self)


class Main:
    """
    Содержит функции для расчета погрешности и отображения необходимого
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
        self.window = MainFrame(main=self)

    def set_row(self, event=None):
        """
        Выполняет отображение необходимого количества строк для
        пар длина/ширина
        """

        self.number_row_to_paste = self.totalrows + 7  # номер row в grid(), в которое будет
                                                       # добавляться следующаая строка/поле
        try:
            row_add = int(self.window.sbox1.get())   # количество строк/полей, которое нужно отразить
        except ValueError:
            return
        if row_add < 1:
            return
        if row_add > self.totalrows:
            for i in range(row_add - self.totalrows):
                label11 = ttk.Label(self.window.frame2,
                                    text=("{}".format(self.totalrows + i + 1)))
                label11.grid(row=(self.number_row_to_paste + i), column=0,
                             padx=0, pady=0, ipadx=40, sticky=W)
                ent3 = ttk.Entry(self.window.frame2, width=self.window.entry_width)
                ent3.grid(row=(self.number_row_to_paste + i), column=0, sticky=E)
                ent3.bind("<Return>", self.calc_result)
                ent4 = ttk.Entry(self.window.frame2, width=self.window.entry_width)
                ent4.grid(row=(self.number_row_to_paste + i), column=1, sticky=W)
                ent4.bind("<Return>", self.calc_result)
                self.listrows.append((ent3, ent4, label11))
            if row_add <= 9:
                self.window.draw.configure(height=self.listrows[0][0].winfo_height() * row_add,
                                      scrollregion=(0, 0, 0, self.listrows[0][0].winfo_height() * row_add))
            else:
                self.window.draw.configure(height=210,
                                      scrollregion=(0, 0, 0, self.listrows[0][0].winfo_height() * row_add))

            self.totalrows = row_add

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
            if row_add <= 9:
                self.window.draw.configure(height=self.listrows[0][0].winfo_height() * row_add,
                                      scrollregion=(0, 0, 0, self.listrows[0][0].winfo_height() \
                                                    * row_add))
            else:
                self.window.draw.configure(height=210,
                                      scrollregion=(0, 0, 0, self.listrows[0][0].winfo_height() \
                                                    * row_add))

    def calc_result(self, event=None):
        """
        Производит рассчет погрешности и выводит полученное значение в
        соответствующей метке
        """
        formula = f"m\u209A = {self.accuracy} * √("
        try:
            levels = int(self.window.sbox2.get())
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
                formula += f'({width}\u00B2 + {height}\u00B2)+'
        except ValueError:
            return
        result = Decimal('{}'.format(self.accuracy * sqrt(sum(parameters) * levels)))
        result = result.quantize(Decimal("1.0"), ROUND_HALF_UP)
        if result == 0.0:
            result = 0.1
        self.window.label9["text"] = (str(result) + " кв.м.")
        if levels == 1:
            formula = formula[:-1] + f') = {result}'
        else:
            formula = formula[:-1].replace('√(', '√((') + f')*{levels}) = {result}'
        if len(parameters) == 1:
            formula = formula.replace('√(', '√').replace('))', ')')
        self.window.text1.delete(1.0, END)
        self.window.text1.insert(1.0, formula)

    def check_accurasy(self, event):
        """
        Регулирует значение кривизны стен
        """
        if event == "1 см":
            self.accuracy = 0.01
        elif event == "2 см":
            self.accuracy = 0.02
        elif event == "3 см":
            self.accuracy = 0.03

    def calc_built_up(self):
        """
        Рассчитывает погрешность определения площади застройки на
        основе загруженных координат
        """
        file_name = fd.askopenfilename()
        if not file_name:
            return
        coords = []
        if file_name[-3:] == 'txt':
            with open(file_name) as file:
                coords = file.readlines()
            for i in range(len(coords)):  # меняем запятые на точки,
                if "," in coords[i]:
                    coords[i] = coords[i].replace(",", ".")
                coords[i] = coords[i].rstrip('\n')
                coords[i] = coords[i].split()
        elif file_name[-3:] == 'csv':
            with open(file_name) as file:
                reader = csv.DictReader(file, delimiter=';')
                for line in reader:
                    if line['Номер']:
                        coords.append([line['Номер'], line['Новый X'], line['Новый Y']])
                for line in coords:  # меняем запятые на точки,
                    for item in range(len(line)):
                        if "," in line[item]:
                            line[item] = line[item].replace(",", ".")
        if coords[0] == coords[-1]:
            coords.insert(0, coords[-2])  # дополняем список первым и последним элементом
        else:
            coords.insert(0, coords[-1])
            coords.append(coords[1])
        tmp_list = []
        for i in range(1, len(coords) - 1):
            tmp_list.append((float(coords[i + 1][1]) - float(coords[i - 1][1])) ** 2 +
                            (float(coords[i + 1][2]) - float(coords[i - 1][2])) ** 2)
        result = Decimal('{}'.format(0.35 * 0.1 * sqrt(sum(tmp_list))))
        result = result.quantize(Decimal("1.0"), ROUND_HALF_UP)
        if result == 0.0:
            result = 0.1
        else:
            self.window.label9["text"] = (str(result) + " кв.м.")
        formula = f'm\u209A = 0.35 * 0.1 * √({round(sum(tmp_list), 2)}) = {result}'
        self.window.text1.delete(1.0, END)
        self.window.text1.insert(1.0, formula)


class Start:
    """
    Запускает программу
    """
    def __init__(self):
        self.root = ThemedTk(theme="itft1")
        self.root.title("Расчет СКП площади")
        self.main = Main(self)
        self.centering()
        self.root.bind("<Key>", self.hot_key_on_rus)
        self.root.bind("<Key>", self.hot_key_on_rus)
        self.root.mainloop()

    @staticmethod
    def hot_key_on_rus(event):
        ctrl = event.state != 0
        if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
            event.widget.event_generate("<<Cut>>")
        if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
            event.widget.event_generate("<<Paste>>")
        if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")

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

