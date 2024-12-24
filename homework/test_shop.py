"""
Протестируйте классы из модуля homework/models.py
"""
import random
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart(product):
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        available_quantity = product.quantity

        expected_result_1 = True
        actual_result_1 = product.check_quantity(available_quantity)
        assert expected_result_1 == actual_result_1, 'Фактический результат не соответствует ожидаемому!'

        expected_result_2 = True
        actual_result_2 = product.check_quantity(available_quantity - 1)
        assert expected_result_2 == actual_result_2, 'Фактический результат не соответствует ожидаемому!'

        expected_result_3 = False
        actual_result_3 = product.check_quantity(available_quantity + 1)
        assert expected_result_3 == actual_result_3, 'Фактический результат не соответствует ожидаемому!'

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        quantity_before_buy = product.quantity
        count = random.randint(1, quantity_before_buy)
        product.buy(count)
        quantity_after_buy = product.quantity

        expected_result = quantity_before_buy - count
        actual_result = quantity_after_buy

        assert expected_result == actual_result, 'Фактический результат не соответствует ожидаемому!'

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            available_quantity = product.quantity
            count = available_quantity + 1
            product.buy(count)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):
        count = random.randint(1, 10)
        cart.add_product(product, count)

        expected_result = count
        actual_result = cart.products[product]

        assert expected_result == actual_result, "Некорректное количество товаров!"

    def test_remove_product_positive(self, cart, product):
        count_add = random.randint(5, 10)
        count_remove = random.randint(1, 5)
        expected_result = count_add - count_remove

        cart.add_product(product, count_add)
        cart.remove_product(product, count_remove)

        actual_result = cart.products[product]
        assert actual_result == expected_result, 'Фактический результат не соответствует ожидаемому!'

    def test_remove_product_negative_1(self, cart, product):
        count_add = random.randint(1, 10)
        count_remove = None

        cart.add_product(product, count_add)
        cart.remove_product(product, count_remove)

        actual_result = cart.products[product]
        expected_result = 0
        assert actual_result == expected_result, 'Фактический результат не соответствует ожидаемому!'

    def test_remove_product_negative_2(self, cart, product):
        count_add = random.randint(1, 10)
        count_remove = count_add

        cart.add_product(product, count_add)
        cart.remove_product(product, count_remove)

        actual_result = cart.products[product]
        expected_result = 0
        assert actual_result == expected_result, 'Фактический результат не соответствует ожидаемому!'

    def test_remove_product_negative_3(self, cart, product):
        count_add = random.randint(1, 10)
        count_remove = count_add + 1

        cart.add_product(product, count_add)
        cart.remove_product(product, count_remove)

        actual_result = cart.products[product]
        expected_result = 0
        assert actual_result == expected_result, 'Фактический результат не соответствует ожидаемому!'

    def test_clear_cart(self, cart, product):
        count = random.randint(1, 10)
        cart.add_product(product, count)
        cart.clear()

        actual_result = cart.products

        assert not actual_result, 'Фактический результат не соответствует ожидаемому!'

    def test_get_total_price(self, cart, product):
        count = random.randint(1, 10)
        cart.add_product(product, count)
        expected_result = product.price * count

        actual_result = cart.get_total_price()
        assert expected_result == actual_result, 'Фактический результат не соответствует ожидаемому!'

    def test_get_total_price_after_clear_card(self, cart):
        cart.clear()
        expected_result = 0

        actual_result = cart.get_total_price()
        assert expected_result == actual_result, 'Фактический результат не соответствует ожидаемому!'

    def test_buy_positive(self, cart, product):
        count = 5
        quantity_before_buy = product.quantity

        cart.add_product(product, count)
        cart.buy()

        expected_result_product_quantity = quantity_before_buy - count
        actual_result_product_quantity = product.quantity

        assert expected_result_product_quantity == actual_result_product_quantity, 'Фактический результат не соответствует ожидаемому!'

        expected_result_card_count = 0
        actual_result_card_count = len(cart.products)
        assert expected_result_card_count == actual_result_card_count, 'Фактический результат не соответствует ожидаемому!'

    def test_buy_negative(self, cart, product):
        quantity_before_buy = product.quantity
        count_add = quantity_before_buy + random.randint(1, 10)

        cart.add_product(product, count_add)

        with pytest.raises(ValueError):
            cart.buy()
