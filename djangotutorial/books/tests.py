from django.test import TestCase
from django.core.exceptions import ValidationError
from parameterized import parameterized
from .models import Book
from itertools import product


titles = [
    "Python入門",
    "",
    "   ",
    "DjangoでWeb開発",
    "データサイエンスの基礎",
]
pages = [100, 0, -5, 250, 50]
prices = [10.00, 100.00, -10.00, 0.00, 25.50]


def generate_test_cases():
    for i, (title, page, price) in enumerate(product(titles, pages, prices)):
        if page < 1 or price < 0 or title.strip() == "":
            expected = False
        else:
            expected = True
        yield (f"case_{i+1}", title, page, price, expected)


class BookValidationTests(TestCase):
    # @parameterized.expand([
    #     ("valid_case", "Python入門", 100, 10.00, True),
    #     ("zero_pages", "ページなし", 0, 100.00, False),
    #     ("negative_pages", "マイナスページ", -5, 100.00, False),
    #     ("negative_price", "無料じゃない本", 50, -10.00, False),
    #     ("zero_price", "無料の本", 50, 0.00, True),
    #     ("empty_title", "", 50, 10.00, False),
    #     ("whitespace_title", "   ", 50, 10.00, False),
    # ])
    @parameterized.expand(generate_test_cases())
    def test_page_validation(self, name, title, pages, price, expected):
        book = Book(title=title, pages=pages, price=price)
        if expected:
            # 正常系: ValidationError が出ないこと
            book.full_clean()  # 問題なければ例外なし
        else:
            # 異常系: ValidationError が出ること
            with self.assertRaises(ValidationError):
                book.full_clean()
