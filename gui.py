import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from list_operations import ListOperations


class ListGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Связный список - Лабораторная работа 4.2")
        self.root.geometry("650x700")

        self.version_frame = tk.Frame(self.root)
        self.version_frame.pack(pady=10)

        tk.Label(self.version_frame, text="Версия модуля:").pack(side=tk.LEFT, padx=5)
        self.version_var = tk.StringVar(value="dynamic")
        self.version_combo = ttk.Combobox(self.version_frame,
                                          textvariable=self.version_var,
                                          values=["dynamic", "stl", "python"],
                                          state="readonly",
                                          width=15)
        self.version_combo.pack(side=tk.LEFT, padx=5)
        tk.Button(self.version_frame, text="Загрузить",
                  command=self.load_module).pack(side=tk.LEFT, padx=5)

        self.list_ops = None
        self._create_widgets()
        self.load_module()

    def load_module(self):
        try:
            mode = self.version_var.get()
            self.list_ops = ListOperations(mode=mode)

            mode_info = {
                "dynamic": ("Dynamic (C++ ручное управление)", "green"),
                "stl": ("STL (C++ стандартная библиотека)", "blue"),
                "python": ("Python (чистая реализация)", "orange")
            }

            mode_text, color = mode_info.get(mode, (mode.upper(), "black"))
            self.info_label.config(text=f"Загружен модуль: {mode_text}", fg=color)
            self.update_listbox()

            self._update_buttons_state()

        except Exception as e:
            messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить модуль: {str(e)}")
            self.info_label.config(text="Ошибка загрузки модуля", fg="red")

    def _update_buttons_state(self):
        """Обновление состояния кнопок на основе флагов доступности функций"""
        if not self.list_ops:
            return

        # Базовые кнопки - всегда активны
        basic_buttons = ['btn_add_first', 'btn_remove_first', 'btn_clear']
        for btn_name in basic_buttons:
            if hasattr(self, btn_name):
                getattr(self, btn_name).config(state=tk.NORMAL)

        # Расширенные кнопки - активны только если функция реализована
        advanced_buttons = {
            'btn_add_by_index': self.list_ops.has_add_by_index,
            'btn_remove_by_index': self.list_ops.has_remove_by_index,
            'btn_remove_by_condition': self.list_ops.has_remove_by_condition,
            'btn_add_last': self.list_ops.has_add_last,
            'btn_remove_last': self.list_ops.has_remove_last,
            'btn_reverse': self.list_ops.has_reverse,
            'btn_sort': self.list_ops.has_sort,
            'btn_min': self.list_ops.has_get_min,
            'btn_max': self.list_ops.has_get_max,
            'btn_remove_duplicates': self.list_ops.has_remove_duplicates,
        }

        for btn_name, is_available in advanced_buttons.items():
            if hasattr(self, btn_name):
                btn = getattr(self, btn_name)
                if is_available:
                    btn.config(state=tk.NORMAL)
                else:
                    btn.config(state=tk.DISABLED)

    def _create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        input_frame = tk.Frame(main_frame)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Значение:").pack(side=tk.LEFT, padx=5)
        self.entry = tk.Entry(input_frame, width=15)
        self.entry.pack(side=tk.LEFT, padx=5)

        self.listbox = tk.Listbox(main_frame, width=65, height=15)
        self.listbox.pack(pady=10)

        canvas = tk.Canvas(main_frame, height=400)
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        basic_frame = tk.LabelFrame(scrollable_frame, text="Базовые операции", padx=5, pady=5)
        basic_frame.pack(fill=tk.X, padx=5, pady=5)

        self.btn_add_first = tk.Button(basic_frame, text="Добавить в начало",
                                       command=self.add_first, width=25)
        self.btn_add_first.pack(side=tk.LEFT, padx=5, pady=2)

        self.btn_remove_first = tk.Button(basic_frame, text="➖ Удалить первый",
                                          command=self.remove_first, width=25)
        self.btn_remove_first.pack(side=tk.LEFT, padx=5, pady=2)

        self.btn_clear = tk.Button(basic_frame, text="Очистить список",
                                   command=self.clear_list, width=25)
        self.btn_clear.pack(side=tk.LEFT, padx=5, pady=2)

        index_frame = tk.LabelFrame(scrollable_frame, text="Операции по индексу", padx=5, pady=5)
        index_frame.pack(fill=tk.X, padx=5, pady=5)

        self.btn_add_by_index = tk.Button(index_frame, text="Добавить по индексу",
                                          command=self.add_by_index, width=25)
        self.btn_add_by_index.pack(side=tk.LEFT, padx=5, pady=2)

        self.btn_remove_by_index = tk.Button(index_frame, text="Удалить по индексу",
                                             command=self.remove_by_index, width=25)
        self.btn_remove_by_index.pack(side=tk.LEFT, padx=5, pady=2)

        self.btn_remove_by_condition = tk.Button(index_frame, text="Удалить по условию",
                                                 command=self.remove_by_condition, width=25)
        self.btn_remove_by_condition.pack(side=tk.LEFT, padx=5, pady=2)

        ends_frame = tk.LabelFrame(scrollable_frame, text="Операции с концами списка", padx=5, pady=5)
        ends_frame.pack(fill=tk.X, padx=5, pady=5)

        self.btn_add_last = tk.Button(ends_frame, text="➕ Добавить в конец",
                                      command=self.add_last, width=25)
        self.btn_add_last.pack(side=tk.LEFT, padx=5, pady=2)

        self.btn_remove_last = tk.Button(ends_frame, text="➖ Удалить последний",
                                         command=self.remove_last, width=25)
        self.btn_remove_last.pack(side=tk.LEFT, padx=5, pady=2)

        transform_frame = tk.LabelFrame(scrollable_frame, text="Преобразования", padx=5, pady=5)
        transform_frame.pack(fill=tk.X, padx=5, pady=5)

        self.btn_reverse = tk.Button(transform_frame, text="Развернуть список",
                                     command=self.reverse_list, width=25)
        self.btn_reverse.pack(side=tk.LEFT, padx=5, pady=2)

        self.btn_sort = tk.Button(transform_frame, text="Сортировать",
                                  command=self.sort_list, width=25)
        self.btn_sort.pack(side=tk.LEFT, padx=5, pady=2)

        self.btn_remove_duplicates = tk.Button(transform_frame, text="Удалить дубликаты",
                                               command=self.remove_duplicates, width=25)
        self.btn_remove_duplicates.pack(side=tk.LEFT, padx=5, pady=2)

        search_frame = tk.LabelFrame(scrollable_frame, text="Поиск и анализ", padx=5, pady=5)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        self.btn_min = tk.Button(search_frame, text="Найти минимум",
                                 command=self.show_min, width=25)
        self.btn_min.pack(side=tk.LEFT, padx=5, pady=2)

        self.btn_max = tk.Button(search_frame, text="Найти максимум",
                                 command=self.show_max, width=25)
        self.btn_max.pack(side=tk.LEFT, padx=5, pady=2)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.info_label = tk.Label(main_frame, text="Выберите версию модуля", fg="blue")
        self.info_label.pack(pady=5)

    def update_listbox(self):
        if not self.list_ops:
            return

        self.listbox.delete(0, tk.END)
        values = self.list_ops.get_all_values()

        if not values:
            self.listbox.insert(tk.END, "Список пуст")
        else:
            self.listbox.insert(tk.END, f"Всего элементов: {len(values)}")
            self.listbox.insert(tk.END, "-" * 40)
            for i, val in enumerate(values):
                self.listbox.insert(tk.END, f"  [{i:2d}] = {val:5d}")

        count = self.list_ops.get_count()
        mode_names = {
            "dynamic": "Dynamic (C++)",
            "stl": "STL (C++)",
            "python": "Python"
        }
        mode_name = mode_names.get(self.list_ops.mode, self.list_ops.mode)
        self.info_label.config(text=f"Всего элементов: {count} | Модуль: {mode_name}")

    def show_message(self, title, message, is_error=False):
        if is_error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)

    def add_first(self):
        if not self.list_ops:
            return

        try:
            value = int(self.entry.get())
            success, msg = self.list_ops.add_first(value)

            if success:
                self.entry.delete(0, tk.END)
                self.update_listbox()
            else:
                self.show_message("Ошибка", msg, True)
        except ValueError:
            self.show_message("Ошибка", "Пожалуйста, введите целое число", True)

    def remove_first(self):
        if not self.list_ops:
            return

        success, msg = self.list_ops.remove_first()

        if success:
            self.update_listbox()
        else:
            self.show_message("Предупреждение", msg, True)

    def clear_list(self):
        if not self.list_ops:
            return

        if messagebox.askyesno("Подтверждение", "Очистить весь список?"):
            success, msg = self.list_ops.clear_list()
            self.update_listbox()
            self.show_message("Успех", msg if success else msg, not success)

    def add_by_index(self):
        if not self.list_ops:
            return

        index = simpledialog.askinteger("Индекс", "Введите индекс:")
        if index is None:
            return

        value = simpledialog.askinteger("Значение", "Введите значение:")
        if value is None:
            return

        success, msg = self.list_ops.add_by_index(index, value)

        if success:
            self.update_listbox()
        else:
            self.show_message("Информация", msg)

    def remove_by_index(self):
        if not self.list_ops:
            return

        index = simpledialog.askinteger("Индекс", "Введите индекс для удаления:")
        if index is None:
            return

        success, msg = self.list_ops.remove_by_index(index)

        if success:
            self.update_listbox()
        else:
            self.show_message("Информация", msg)

    def remove_by_condition(self):
        if not self.list_ops:
            return

        value = simpledialog.askinteger("Значение", "Введите значение:")
        if value is None:
            return

        mode = simpledialog.askinteger("Режим",
                                       "Выберите режим:\n1 - меньше\n2 - равно\n3 - больше\n4 - меньше либо равно")
        if mode not in (1, 2, 3, 4):
            self.show_message("Ошибка", "Неверный режим", True)
            return

        success, msg = self.list_ops.remove_by_condition(value, mode)

        if success:
            self.update_listbox()
        else:
            self.show_message("Информация", msg)

    def add_last(self):
        if not self.list_ops:
            return

        try:
            value = int(self.entry.get())
            success, msg = self.list_ops.add_last(value)

            if success:
                self.entry.delete(0, tk.END)
                self.update_listbox()
            else:
                self.show_message("Информация", msg)
        except ValueError:
            self.show_message("Ошибка", "Введите целое число", True)

    def remove_last(self):
        if not self.list_ops:
            return

        success, msg = self.list_ops.remove_last()

        if success:
            self.update_listbox()
        else:
            self.show_message("Информация", msg, not success)

    def reverse_list(self):
        if not self.list_ops:
            return

        success, msg = self.list_ops.reverse_list()

        if success:
            self.update_listbox()
        else:
            self.show_message("Информация", msg)

    def sort_list(self):
        if not self.list_ops:
            return

        success, msg = self.list_ops.sort_list()

        if success:
            self.update_listbox()
        else:
            self.show_message("Информация", msg)

    def show_min(self):
        if not self.list_ops:
            return

        value, msg = self.list_ops.get_min()

        if value is not None:
            self.show_message("Минимум", msg)
        else:
            self.show_message("Информация", msg)

    def show_max(self):
        if not self.list_ops:
            return

        value, msg = self.list_ops.get_max()

        if value is not None:
            self.show_message("Максимум", msg)
        else:
            self.show_message("Информация", msg)

    def remove_duplicates(self):
        if not self.list_ops:
            return

        success, msg = self.list_ops.remove_duplicates()

        if success:
            self.update_listbox()
        else:
            self.show_message("Информация", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = ListGUI(root)
    root.mainloop()