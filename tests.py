import logging

from logic import (
    CanvasShapeManager,
    CurrencyConverter,
    ItemListManager,
    format_echo_text,
)

logger = logging.getLogger(__name__)


def test_text_echo() -> None:
    """Тесты для задания Средняя 2 (обработка текстового поля)."""
    assert format_echo_text("Привет, Tkinter!") == "Вы ввели: Привет, Tkinter!"
    assert format_echo_text("   Тест пробелов   ") == "Вы ввели: Тест пробелов"

    for invalid_text in ("", "   "):
        try:
            format_echo_text(invalid_text)
            assert False, "Ожидалось исключение ValueError для пустой строки"
        except ValueError:
            pass

    try:
        format_echo_text(123)  # type: ignore[arg-type]
        assert False, "Ожидалось исключение TypeError для нестрокового типа"
    except TypeError:
        pass


def test_item_list_manager() -> None:
    """Тесты для задания Средняя 4 (работа со списком элементов)."""
    manager = ItemListManager(["Первый", "Второй"])
    assert manager.get_all() == ["Первый", "Второй"]
    assert manager.get_item(1) == "Второй"

    manager.add_item("  Третий  ")
    assert manager.get_item(2) == "Третий"

    removed = manager.remove_item(0)
    assert removed == "Первый"
    assert manager.get_all() == ["Второй", "Третий"]

    try:
        manager.get_item(True)
        assert False, "Ожидалось исключение TypeError для индекса типа bool"
    except TypeError:
        pass

    try:
        manager.get_item(10)
        assert False, "Ожидалось исключение IndexError при выходе за границы"
    except IndexError:
        pass


def test_canvas_shape_manager() -> None:
    """Тесты для задания Повышенная 2 (рисование фигур мышью)."""
    canvas_mgr = CanvasShapeManager()
    shape1 = canvas_mgr.record_shape("Rectangle", 10, 20, 110, 120, "#2563eb")
    assert shape1.shape_type == "rectangle"
    assert len(canvas_mgr.shapes) == 1

    shape2 = canvas_mgr.record_shape("oval", 0, 0, 50.5, 75.5, "#dc2626")
    assert shape2.shape_type == "oval"
    assert len(canvas_mgr.shapes) == 2

    undone = canvas_mgr.undo_last()
    assert undone == shape2
    assert len(canvas_mgr.shapes) == 1

    try:
        canvas_mgr.record_shape("triangle", 0, 0, 10, 10)
        assert False, "Ожидалось исключение ValueError для неизвестной фигуры"
    except ValueError:
        pass

    try:
        canvas_mgr.record_shape("line", True, 0, 10, 10)
        assert False, "Ожидалось исключение TypeError для координаты bool"
    except TypeError:
        pass

    canvas_mgr.clear()
    assert canvas_mgr.shapes == []


def test_currency_converter() -> None:
    """Тесты для задания Повышенная 6 (конвертер валют)."""
    converter = CurrencyConverter({"RUB": 1.0, "USD": 90.0, "EUR": 100.0})

    assert converter.convert(0, "USD", "RUB") == 0.0
    assert converter.convert(10, "USD", "RUB") == 900.0
    assert converter.parse_and_convert("100,50", "RUB", "RUB") == 100.5
    assert converter.convert(100, "EUR", "USD") == 111.11
    assert len(converter.history) == 4

    try:
        converter.convert(True, "USD", "RUB")
        assert False, "Ожидалось исключение TypeError для суммы типа bool"
    except TypeError:
        pass

    try:
        converter.convert(-50, "USD", "RUB")
        assert False, "Ожидалось исключение ValueError для отрицательной суммы"
    except ValueError:
        pass

    try:
        converter.parse_and_convert("abc", "USD", "RUB")
        assert False, "Ожидалось исключение ValueError для некорректной строки"
    except ValueError:
        pass

    try:
        converter.convert(10, "GBP", "RUB")
        assert False, "Ожидалось исключение ValueError для неизвестной валюты"
    except ValueError:
        pass


def run_all_tests() -> None:
    """Запускает полный набор модульных проверок лабораторной работы №5."""
    test_text_echo()
    test_item_list_manager()
    test_canvas_shape_manager()
    test_currency_converter()
    logger.info("[TESTS] Все автотесты лабораторной №5 успешно пройдены!")
