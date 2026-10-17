import logging
import math
from dataclasses import dataclass

logger = logging.getLogger(__name__)


def format_echo_text(raw_text: str) -> str:
    """Валидирует и форматирует введённый пользователем текст (Средняя 2)."""
    if not isinstance(raw_text, str):
        raise TypeError("Ожидается строковое значение")
    cleaned = raw_text.strip()
    if not cleaned:
        raise ValueError("Поле ввода не может быть пустым")
    logger.info("Обработан текст пользователя: '%s'", cleaned)
    return f"Вы ввели: {cleaned}"


class ItemListManager:
    """Менеджер элементов списка для виджета Listbox (Средняя 4)."""

    def __init__(self, initial_items: list[str] | None = None) -> None:
        self._items: list[str] = []
        if initial_items is not None:
            if not isinstance(initial_items, list):
                raise TypeError("Начальные элементы должны быть списком")
            for item in initial_items:
                self.add_item(item)

    def add_item(self, item: str) -> str:
        """Добавляет проверенный непустой элемент в список."""
        if not isinstance(item, str):
            raise TypeError("Элемент списка должен быть строкой")
        cleaned = item.strip()
        if not cleaned:
            raise ValueError("Нельзя добавить пустой элемент в список")
        self._items.append(cleaned)
        logger.info("Добавлен элемент в список: '%s'", cleaned)
        return cleaned

    def remove_item(self, index: int) -> str:
        """Удаляет и возвращает элемент по индексу."""
        self._validate_index(index)
        removed = self._items.pop(index)
        logger.info("Удалён элемент из списка: '%s'", removed)
        return removed

    def get_item(self, index: int) -> str:
        """Возвращает элемент списка по индексу."""
        self._validate_index(index)
        return self._items[index]

    def get_all(self) -> list[str]:
        """Возвращает копию текущего списка элементов."""
        return list(self._items)

    def _validate_index(self, index: int) -> None:
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс выходит за границы списка")


@dataclass(frozen=True)
class DrawnShape:
    """Модель фигуры, нарисованной мышью на холсте (Повышенная 2)."""

    shape_type: str
    x1: float
    y1: float
    x2: float
    y2: float
    color: str


class CanvasShapeManager:
    """Хранилище и валидатор фигур на холсте (Повышенная 2)."""

    ALLOWED_SHAPES: tuple[str, ...] = ("rectangle", "oval", "line")

    def __init__(self) -> None:
        self._shapes: list[DrawnShape] = []

    def record_shape(
        self,
        shape_type: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str = "#2563eb",
    ) -> DrawnShape:
        """Проверяет параметры и сохраняет фигуру в историю холста."""
        if not isinstance(shape_type, str):
            raise TypeError("Тип фигуры должен быть строкой")
        normalized_type = shape_type.strip().lower()
        if normalized_type not in self.ALLOWED_SHAPES:
            raise ValueError(f"Неизвестный тип фигуры: {shape_type}")

        coords = (x1, y1, x2, y2)
        for coord in coords:
            if isinstance(coord, bool) or not isinstance(coord, (int, float)):
                raise TypeError("Координаты должны быть числами")
            if math.isnan(coord) or math.isinf(coord):
                raise ValueError("Координаты должны быть конечными числами")

        if not isinstance(color, str) or not color.strip():
            raise ValueError("Цвет фигуры должен быть непустой строкой")

        shape = DrawnShape(
            shape_type=normalized_type,
            x1=float(x1),
            y1=float(y1),
            x2=float(x2),
            y2=float(y2),
            color=color.strip(),
        )
        self._shapes.append(shape)
        logger.info(
            "Записана фигура %s: (%s, %s) -> (%s, %s)",
            shape.shape_type,
            shape.x1,
            shape.y1,
            shape.x2,
            shape.y2,
        )
        return shape

    def undo_last(self) -> DrawnShape | None:
        """Удаляет последнюю добавленную фигуру."""
        if not self._shapes:
            return None
        removed = self._shapes.pop()
        logger.info("Отменена фигура: %s", removed.shape_type)
        return removed

    def clear(self) -> None:
        """Очищает список сохранённых фигур."""
        self._shapes.clear()
        logger.info("Холст полностью очищен")

    @property
    def shapes(self) -> list[DrawnShape]:
        """Возвращает список всех сохранённых фигур."""
        return list(self._shapes)


class CurrencyConverter:
    """Конвертер валют с поддержкой кросс-курсов и истории (Повышенная 6)."""

    DEFAULT_RATES_TO_RUB: dict[str, float] = {
        "RUB": 1.0,
        "USD": 92.50,
        "EUR": 100.40,
        "CNY": 12.80,
        "KZT": 0.19,
    }

    def __init__(self, rates_to_rub: dict[str, float] | None = None) -> None:
        raw_rates = (
            rates_to_rub
            if rates_to_rub is not None
            else self.DEFAULT_RATES_TO_RUB
        )
        if not isinstance(raw_rates, dict) or not raw_rates:
            raise ValueError("Словарь курсов валют не может быть пустым")

        self._rates: dict[str, float] = {}
        for code, rate in raw_rates.items():
            if not isinstance(code, str) or not code.strip():
                raise ValueError("Код валюты должен быть непустой строкой")
            if isinstance(rate, bool) or not isinstance(rate, (int, float)):
                raise TypeError("Курс валюты должен быть числом")
            if rate <= 0 or math.isnan(rate) or math.isinf(rate):
                raise ValueError("Курс валюты должен быть больше нуля")
            self._rates[code.strip().upper()] = float(rate)

        self._history: list[str] = []

    @property
    def supported_currencies(self) -> list[str]:
        """Возвращает список доступных кодов валют."""
        return list(self._rates.keys())

    @property
    def history(self) -> list[str]:
        """Возвращает историю успешных конвертаций."""
        return list(self._history)

    def get_exchange_rate(
        self, from_currency: str, to_currency: str
    ) -> float:
        """Вычисляет кросс-курс между двумя валютами."""
        src = self._validate_currency(from_currency)
        dst = self._validate_currency(to_currency)
        return self._rates[src] / self._rates[dst]

    def convert(
        self, amount: float | int, from_currency: str, to_currency: str
    ) -> float:
        """Переводит сумму из одной валюты в другую."""
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числовым значением")
        if math.isnan(amount) or math.isinf(amount):
            raise ValueError("Сумма должна быть конечным числом")
        if amount < 0:
            raise ValueError(
                "Сумма для конвертации не может быть отрицательной"
            )

        src = self._validate_currency(from_currency)
        dst = self._validate_currency(to_currency)

        rate = self._rates[src] / self._rates[dst]
        result = round(float(amount) * rate, 2)
        record = f"{float(amount):.2f} {src} = {result:.2f} {dst}"
        self._history.append(record)
        logger.info("Выполнена конвертация: %s", record)
        return result

    def parse_and_convert(
        self, raw_amount: str, from_currency: str, to_currency: str
    ) -> float:
        """Парсит строку суммы и выполняет конвертацию."""
        if not isinstance(raw_amount, str):
            raise TypeError("Ожидается строковое представление суммы")
        cleaned = raw_amount.strip().replace(",", ".")
        if not cleaned:
            raise ValueError("Введите сумму для конвертации")
        try:
            numeric_amount = float(cleaned)
        except ValueError as exc:
            raise ValueError(
                f"Некорректный формат числа: '{raw_amount}'"
            ) from exc

        return self.convert(numeric_amount, from_currency, to_currency)

    def clear_history(self) -> None:
        """Очищает историю конвертаций."""
        self._history.clear()

    def _validate_currency(self, code: str) -> str:
        if not isinstance(code, str):
            raise TypeError("Код валюты должен быть строкой")
        normalized = code.strip().upper()
        if normalized not in self._rates:
            raise ValueError(f"Неподдерживаемая валюта: {code}")
        return normalized
