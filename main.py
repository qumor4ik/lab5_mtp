import logging
import sys
import tkinter as tk

from gui import Lab5Application
from logic import (
    CanvasShapeManager,
    CurrencyConverter,
    ItemListManager,
    format_echo_text,
)
from tests import run_all_tests

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def run_console_demo() -> None:
    """Демонстрирует работу логики всех заданий варианта 2 в консоли."""
    logger.info("=== Лабораторная работа №5 (Вариант 2) ===")
    run_all_tests()

    # Средняя 2: Поле ввода и вывод текста
    echo_result = format_echo_text("Лабораторная работа №5")
    logger.info("[Средняя 2] %s", echo_result)

    # Средняя 4: Список (Listbox) и выбор элемента
    list_mgr = ItemListManager(["Tkinter", "PyQt5", "Canvas"])
    logger.info(
        "[Средняя 4] Элементы списка: %s | Выбран индекс 0: %s",
        list_mgr.get_all(),
        list_mgr.get_item(0),
    )

    # Средняя 7: Окно с меню (File -> Exit)
    logger.info("[Средняя 7] Главное меню File -> Exit сконфигурировано")

    # Повышенная 2: Рисование фигур мышью
    canvas_mgr = CanvasShapeManager()
    shape = canvas_mgr.record_shape("rectangle", 15, 25, 180, 140, "#2563eb")
    logger.info("[Повышенная 2] Нарисована фигура: %s", shape)

    # Повышенная 6: Конвертер валют
    converter = CurrencyConverter()
    rub_amount = converter.convert(100, "USD", "RUB")
    logger.info("[Повышенная 6] 100.00 USD = %.2f RUB", rub_amount)


def main() -> None:
    """Точка входа в приложение."""
    run_console_demo()

    if "--test" in sys.argv:
        logger.info("Запуск завершён в тестовом режиме (--test).")
        return

    try:
        app = Lab5Application()
        logger.info("Запуск графического интерфейса Tkinter...")
        app.mainloop()
    except tk.TclError as exc:
        logger.warning(
            "Графический дисплей недоступен (%s). Работа завершена в консоли.",
            exc,
        )


if __name__ == "__main__":
    main()
