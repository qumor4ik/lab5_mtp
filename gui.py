import logging
import tkinter as tk
from tkinter import messagebox, ttk

from logic import (
    CanvasShapeManager,
    CurrencyConverter,
    ItemListManager,
    format_echo_text,
)

logger = logging.getLogger(__name__)


class TextInputFrame(ttk.LabelFrame):
    """Средняя 2: Текстовое поле и кнопка, выводящая введённый текст."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(
            parent,
            text="Средняя 2: Ввод и вывод текста",
            padding=10,
        )
        self._build_ui()

    def _build_ui(self) -> None:
        self.columnconfigure(1, weight=1)

        prompt_label = ttk.Label(self, text="Введите текст:")
        prompt_label.grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)

        self.text_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.text_var)
        self.entry.grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=4)
        self.entry.bind("<Return>", lambda _event: self.handle_show_text())

        self.show_btn = ttk.Button(
            self,
            text="Вывести текст",
            command=self.handle_show_text,
        )
        self.show_btn.grid(row=0, column=2, padx=(0, 4), pady=4)

        self.clear_btn = ttk.Button(
            self,
            text="Сброс",
            command=self.reset,
        )
        self.clear_btn.grid(row=0, column=3, pady=4)

        self.output_var = tk.StringVar(value="Здесь появится введённый текст")
        self.output_label = ttk.Label(
            self,
            textvariable=self.output_var,
            foreground="#1d4ed8",
        )
        self.output_label.grid(
            row=1, column=0, columnspan=4, sticky="w", pady=(4, 0)
        )

    def handle_show_text(self) -> None:
        """Считывает текст из поля ввода и выводит его в метку."""
        try:
            formatted = format_echo_text(self.text_var.get())
            self.output_var.set(formatted)
        except ValueError as exc:
            self.output_var.set(f"Ошибка: {exc}")

    def reset(self) -> None:
        """Очищает поле ввода и возвращает исходный текст метки."""
        self.text_var.set("")
        self.output_var.set("Здесь появится введённый текст")


class ListboxFrame(ttk.LabelFrame):
    """Средняя 4: Список (Listbox) и выбор элемента."""

    DEFAULT_ITEMS: list[str] = [
        "Python 3.12",
        "Tkinter GUI",
        "PyQt5 Framework",
        "SQLite3 Database",
        "Git & GitHub Actions",
    ]

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(
            parent,
            text="Средняя 4: Список (Listbox) и выбор элемента",
            padding=10,
        )
        self.manager = ItemListManager(self.DEFAULT_ITEMS)
        self._build_ui()
        self._refresh_listbox()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        list_container = ttk.Frame(self)
        list_container.grid(
            row=0, column=0, columnspan=3, sticky="nsew", pady=(0, 8)
        )
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)

        self.listbox = tk.Listbox(
            list_container,
            height=6,
            selectmode=tk.SINGLE,
            exportselection=False,
        )
        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.listbox.bind("<<ListboxSelect>>", self.on_select_event)

        scrollbar = ttk.Scrollbar(
            list_container,
            orient=tk.VERTICAL,
            command=self.listbox.yview,
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.new_item_var = tk.StringVar()
        self.new_item_entry = ttk.Entry(self, textvariable=self.new_item_var)
        self.new_item_entry.grid(
            row=1, column=0, sticky="ew", padx=(0, 6), pady=4
        )

        add_btn = ttk.Button(
            self,
            text="Добавить",
            command=self.handle_add_item,
        )
        add_btn.grid(row=1, column=1, padx=(0, 4), pady=4)

        remove_btn = ttk.Button(
            self,
            text="Удалить",
            command=self.handle_remove_selected,
        )
        remove_btn.grid(row=1, column=2, pady=4)

        self.selected_var = tk.StringVar(value="Выбранный элемент: нет")
        selected_label = ttk.Label(
            self,
            textvariable=self.selected_var,
            foreground="#15803d",
        )
        selected_label.grid(
            row=2, column=0, columnspan=3, sticky="w", pady=(4, 0)
        )

    def _refresh_listbox(self) -> None:
        self.listbox.delete(0, tk.END)
        for item in self.manager.get_all():
            self.listbox.insert(tk.END, item)

    def on_select_event(self, _event: tk.Event | None = None) -> None:
        """Обновляет метку при выборе элемента в Listbox."""
        selection = self.listbox.curselection()
        if not selection:
            self.selected_var.set("Выбранный элемент: нет")
            return
        index = int(selection[0])
        value = self.manager.get_item(index)
        self.selected_var.set(f"Выбранный элемент [{index + 1}]: {value}")

    def handle_add_item(self) -> None:
        """Добавляет новый элемент из текстового поля в Listbox."""
        try:
            added = self.manager.add_item(self.new_item_var.get())
            self.new_item_var.set("")
            self._refresh_listbox()
            self.selected_var.set(f"Добавлен элемент: {added}")
        except ValueError as exc:
            self.selected_var.set(f"Ошибка: {exc}")

    def handle_remove_selected(self) -> None:
        """Удаляет текущий выделенный элемент из Listbox."""
        selection = self.listbox.curselection()
        if not selection:
            self.selected_var.set("Сначала выберите элемент для удаления")
            return
        index = int(selection[0])
        removed = self.manager.remove_item(index)
        self._refresh_listbox()
        self.selected_var.set(f"Удалён элемент: {removed}")

    def reset(self) -> None:
        """Восстанавливает начальный список элементов."""
        self.manager = ItemListManager(self.DEFAULT_ITEMS)
        self.new_item_var.set("")
        self._refresh_listbox()
        self.selected_var.set("Выбранный элемент: нет")


class DrawingCanvasFrame(ttk.LabelFrame):
    """Повышенная 2: Рисование фигур мышью на холсте Canvas."""

    SHAPE_LABELS: dict[str, str] = {
        "Прямоугольник": "rectangle",
        "Овал": "oval",
        "Линия": "line",
    }
    COLOR_OPTIONS: dict[str, str] = {
        "Синий": "#2563eb",
        "Красный": "#dc2626",
        "Зелёный": "#16a34a",
        "Фиолетовый": "#9333ea",
    }

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(
            parent,
            text="Повышенная 2: Рисование фигур мышью (зажмите ЛКМ)",
            padding=10,
        )
        self.shape_manager = CanvasShapeManager()
        self._start_x: float = 0.0
        self._start_y: float = 0.0
        self._preview_id: int | None = None
        self._drawn_canvas_ids: list[int] = []
        self._build_ui()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        toolbar = ttk.Frame(self)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(toolbar, text="Фигура:").pack(side=tk.LEFT, padx=(0, 4))
        self.shape_label_var = tk.StringVar(value="Прямоугольник")
        shape_combo = ttk.Combobox(
            toolbar,
            textvariable=self.shape_label_var,
            values=list(self.SHAPE_LABELS.keys()),
            state="readonly",
            width=15,
        )
        shape_combo.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(toolbar, text="Цвет:").pack(side=tk.LEFT, padx=(0, 4))
        self.color_label_var = tk.StringVar(value="Синий")
        color_combo = ttk.Combobox(
            toolbar,
            textvariable=self.color_label_var,
            values=list(self.COLOR_OPTIONS.keys()),
            state="readonly",
            width=12,
        )
        color_combo.pack(side=tk.LEFT, padx=(0, 10))

        undo_btn = ttk.Button(
            toolbar,
            text="Отменить",
            command=self.undo_last_shape,
        )
        undo_btn.pack(side=tk.LEFT, padx=(0, 4))

        clear_btn = ttk.Button(
            toolbar,
            text="Очистить холст",
            command=self.clear_canvas,
        )
        clear_btn.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(
            self,
            bg="#ffffff",
            height=220,
            relief=tk.SUNKEN,
            borderwidth=1,
        )
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)

        self.status_var = tk.StringVar(value="Фигур нарисовано: 0")
        status_label = ttk.Label(self, textvariable=self.status_var)
        status_label.grid(row=2, column=0, sticky="w", pady=(6, 0))

    def _current_shape_type(self) -> str:
        return self.SHAPE_LABELS.get(self.shape_label_var.get(), "rectangle")

    def _current_color(self) -> str:
        return self.COLOR_OPTIONS.get(self.color_label_var.get(), "#2563eb")

    def _draw_canvas_item(
        self,
        shape_type: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str,
    ) -> int:
        if shape_type == "rectangle":
            return self.canvas.create_rectangle(
                x1, y1, x2, y2, outline=color, width=2
            )
        if shape_type == "oval":
            return self.canvas.create_oval(
                x1, y1, x2, y2, outline=color, width=2
            )
        return self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

    def _on_mouse_down(self, event: tk.Event) -> None:
        self._start_x = float(event.x)
        self._start_y = float(event.y)
        self._preview_id = self._draw_canvas_item(
            self._current_shape_type(),
            self._start_x,
            self._start_y,
            self._start_x,
            self._start_y,
            self._current_color(),
        )

    def _on_mouse_drag(self, event: tk.Event) -> None:
        if self._preview_id is not None:
            self.canvas.coords(
                self._preview_id,
                self._start_x,
                self._start_y,
                float(event.x),
                float(event.y),
            )

    def _on_mouse_up(self, event: tk.Event) -> None:
        if self._preview_id is None:
            return
        end_x = float(event.x)
        end_y = float(event.y)
        self.canvas.coords(
            self._preview_id, self._start_x, self._start_y, end_x, end_y
        )
        self._drawn_canvas_ids.append(self._preview_id)
        self._preview_id = None

        self.shape_manager.record_shape(
            self._current_shape_type(),
            self._start_x,
            self._start_y,
            end_x,
            end_y,
            self._current_color(),
        )
        self._update_status()

    def undo_last_shape(self) -> None:
        """Удаляет последнюю нарисованную фигуру с холста и из модели."""
        if self._drawn_canvas_ids:
            last_id = self._drawn_canvas_ids.pop()
            self.canvas.delete(last_id)
            self.shape_manager.undo_last()
            self._update_status()

    def clear_canvas(self) -> None:
        """Полностью очищает холст."""
        self.canvas.delete("all")
        self._drawn_canvas_ids.clear()
        self.shape_manager.clear()
        self._update_status()

    def _update_status(self) -> None:
        count = len(self.shape_manager.shapes)
        self.status_var.set(f"Фигур нарисовано: {count}")


class CurrencyConverterFrame(ttk.LabelFrame):
    """Повышенная 6: Программа «Конвертер валют»."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(
            parent,
            text="Повышенная 6: Конвертер валют",
            padding=10,
        )
        self.converter = CurrencyConverter()
        self._build_ui()

    def _build_ui(self) -> None:
        self.columnconfigure(1, weight=1)
        currencies = self.converter.supported_currencies

        ttk.Label(self, text="Сумма:").grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=4
        )
        self.amount_var = tk.StringVar(value="100")
        self.amount_entry = ttk.Entry(self, textvariable=self.amount_var)
        self.amount_entry.grid(
            row=0, column=1, columnspan=3, sticky="ew", pady=4
        )
        self.amount_entry.bind(
            "<Return>", lambda _event: self.handle_convert()
        )

        ttk.Label(self, text="Маршрут:").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=4
        )

        self.from_var = tk.StringVar(value="USD")
        from_combo = ttk.Combobox(
            self,
            textvariable=self.from_var,
            values=currencies,
            state="readonly",
            width=8,
        )
        from_combo.grid(row=1, column=1, sticky="w", pady=4)

        swap_btn = ttk.Button(
            self,
            text="⇄",
            width=4,
            command=self.handle_swap_currencies,
        )
        swap_btn.grid(row=1, column=2, padx=6, pady=4)

        self.to_var = tk.StringVar(value="RUB")
        to_combo = ttk.Combobox(
            self,
            textvariable=self.to_var,
            values=currencies,
            state="readonly",
            width=8,
        )
        to_combo.grid(row=1, column=3, sticky="e", pady=4)

        convert_btn = ttk.Button(
            self,
            text="Конвертировать",
            command=self.handle_convert,
        )
        convert_btn.grid(
            row=2, column=0, columnspan=4, sticky="ew", pady=(6, 4)
        )

        self.result_var = tk.StringVar(value="Введите сумму и нажмите кнопку")
        result_label = ttk.Label(
            self,
            textvariable=self.result_var,
            foreground="#1d4ed8",
        )
        result_label.grid(
            row=3, column=0, columnspan=4, sticky="w", pady=(2, 4)
        )

        ttk.Label(self, text="История конвертаций:").grid(
            row=4, column=0, columnspan=4, sticky="w", pady=(4, 2)
        )

        self.history_listbox = tk.Listbox(self, height=4)
        self.history_listbox.grid(
            row=5, column=0, columnspan=4, sticky="nsew", pady=(0, 4)
        )
        self.rowconfigure(5, weight=1)

    def handle_swap_currencies(self) -> None:
        """Меняет местами исходную и целевую валюты."""
        current_from = self.from_var.get()
        current_to = self.to_var.get()
        self.from_var.set(current_to)
        self.to_var.set(current_from)
        self.handle_convert()

    def handle_convert(self) -> None:
        """Выполняет расчёт конвертации и обновляет историю."""
        src = self.from_var.get()
        dst = self.to_var.get()
        try:
            converted = self.converter.parse_and_convert(
                self.amount_var.get(), src, dst
            )
            rate = self.converter.get_exchange_rate(src, dst)
            self.result_var.set(
                f"Итог: {converted:.2f} {dst} "
                f"(курс 1 {src} = {rate:.4f} {dst})"
            )
            self._refresh_history()
        except (ValueError, TypeError) as exc:
            self.result_var.set(f"Ошибка: {exc}")

    def _refresh_history(self) -> None:
        self.history_listbox.delete(0, tk.END)
        for entry in reversed(self.converter.history):
            self.history_listbox.insert(tk.END, entry)

    def reset(self) -> None:
        """Сбрасывает поля конвертера и историю."""
        self.amount_var.set("100")
        self.from_var.set("USD")
        self.to_var.set("RUB")
        self.converter.clear_history()
        self._refresh_history()
        self.result_var.set("Введите сумму и нажмите кнопку")


class Lab5Application(tk.Tk):
    """Главное окно приложения с меню File -> Exit (Средняя 7)."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Лабораторная работа №5 — Вариант 2 (Нестеров В.С.)")
        self.geometry("920x680")
        self.minsize(820, 600)

        self._build_menu()
        self._build_layout()
        self.bind("<Control-q>", lambda _event: self.exit_application())

    def _build_menu(self) -> None:
        """Создаёт главное меню окна с пунктом File -> Exit (Средняя 7)."""
        self.menubar = tk.Menu(self)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(
            label="Reset All",
            command=self.reset_all_panels,
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Exit",
            accelerator="Ctrl+Q",
            command=self.exit_application,
        )
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(
            label="About",
            command=self.show_about_dialog,
        )
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        self.config(menu=self.menubar)

    def _build_layout(self) -> None:
        container = ttk.Frame(self, padding=12)
        container.pack(fill=tk.BOTH, expand=True)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(1, weight=1)

        self.text_frame = TextInputFrame(container)
        self.text_frame.grid(
            row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10)
        )

        left_column = ttk.Frame(container)
        left_column.grid(
            row=1, column=0, sticky="nsew", padx=(0, 6)
        )
        left_column.columnconfigure(0, weight=1)
        left_column.rowconfigure(0, weight=1)
        left_column.rowconfigure(1, weight=1)

        self.listbox_frame = ListboxFrame(left_column)
        self.listbox_frame.grid(
            row=0, column=0, sticky="nsew", pady=(0, 10)
        )

        self.converter_frame = CurrencyConverterFrame(left_column)
        self.converter_frame.grid(row=1, column=0, sticky="nsew")

        self.drawing_frame = DrawingCanvasFrame(container)
        self.drawing_frame.grid(
            row=1, column=1, sticky="nsew", padx=(6, 0)
        )

    def reset_all_panels(self) -> None:
        """Сбрасывает состояние всех виджетов к начальному."""
        self.text_frame.reset()
        self.listbox_frame.reset()
        self.converter_frame.reset()
        self.drawing_frame.clear_canvas()
        logger.info("Все панели приложения сброшены к начальному состоянию")

    def show_about_dialog(self) -> None:
        """Отображает информационное окно о лабораторной работе."""
        messagebox.showinfo(
            title="О программе",
            message=(
                "Лабораторная работа №5: Визуальное программирование\n"
                "Выполнил: Нестеров Вадим Сергеевич (группа 221141)\n"
                "Вариант 2: Задания Ср. 2, 4, 7 и Пов. 2, 6"
            ),
        )

    def exit_application(self) -> None:
        """Корректно завершает работу главного окна (File -> Exit)."""
        logger.info("Завершение работы приложения через команду Exit")
        self.destroy()
