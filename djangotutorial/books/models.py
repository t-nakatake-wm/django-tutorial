from django.db import models
from django.core.exceptions import ValidationError


class Book(models.Model):
    title = models.CharField(max_length=100)
    pages = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def clean(self):
        if self.pages < 1:
            raise ValidationError("ページ数は1以上でなければなりません。")
        if self.price < 0:
            raise ValidationError("価格は0以上でなければなりません。")
        if self.title.strip() == "":
            raise ValidationError("タイトルを入力してください。")

    def __str__(self):
        return f"{self.title} ({self.pages} pages)"
