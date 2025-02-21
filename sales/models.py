from django.db import models
from rest_framework.exceptions import ValidationError


class Organization(models.Model):
    """
    Название.
    Контакты:
        email,
        страна,
        город,
        улица,
        номер дома.
    Продукты:
        название,
        модель,
        дата выхода продукта на рынок.
    Поставщик (предыдущий по иерархии объект сети).
    Задолженность перед поставщиком в денежном выражении с точностью до копеек.
    Время создания (заполняется автоматически при создании).
    """

    name = models.CharField(
        null=True, blank=True, max_length=100, verbose_name="Название организации"
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    country = models.CharField(
        max_length=35,
        verbose_name="Страна",
        blank=True,
        null=True,
        help_text="Введите страну",
    )
    city = models.CharField(
        max_length=35,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Введите город",
    )
    street = models.CharField(
        max_length=35,
        verbose_name="Улица",
        blank=True,
        null=True,
        help_text="Введите улицу",
    )
    house_number = models.CharField(
        max_length=35,
        verbose_name="Номер дома",
        blank=True,
        null=True,
        help_text="Введите номер дома",
    )
    products = models.ManyToManyField("sales.Product", verbose_name="Продукты")
    provider = models.ForeignKey(
        "sales.Organization",
        null=True,
        blank=True,
        verbose_name="Поставщик",
        on_delete=models.SET_NULL,
    )
    debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        max_length=35,
        verbose_name="Задолженность",
        help_text="Введите задолженность с точностью до копеек",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    FACTORY = "Завод"
    RETAIL = "Розничная сеть"
    SOLE_TRADER = "Индивидуальный предприниматель"

    LEVEL_CHOICES = [
        (FACTORY, "Завод"),
        (RETAIL, "Розничная сеть"),
        (SOLE_TRADER, "Индивидуальный предприниматель"),
    ]

    status = models.CharField(
        max_length=150, choices=LEVEL_CHOICES, verbose_name="Уровень"
    )

    def __str__(self):
        return f"Organization {self.name}, status {self.status}"

    def clean(self, *args, **kwargs):
        self._validate_status()
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def _validate_status(self):
        # print(f"объект: {self}")

        if self.status == "Завод" and self.provider is not None:
            raise ValidationError(
                "Завод всегда находится на уровне 0, нет поставщиков."
            )
            # детей можно не проверять

        elif not self.status == "Завод":
            if not self.provider:
                raise ValidationError("Заполните поставщика.")
            else:
                if self.provider.status == "Завод":
                    # родителей можно не проверять

                    # если объект не новый (возможно у него есть дети)
                    if Organization.objects.filter(pk=self.pk).exists():

                        # дети могут быть, а внуки нет
                        next_level = Organization.objects.filter(provider=self)
                        if next_level:
                            if Organization.objects.filter(provider__in=next_level):
                                raise ValidationError(
                                    "В иерархической структуре не может быть больше трех уровней."
                                )

                else:
                    # проверка родителей (self.provider.provider должен быть Завод):
                    if (
                        self.provider.provider
                        and not self.provider.provider.status == "Завод"
                    ):
                        raise ValidationError(
                            "В иерархической структуре не может быть больше трех уровней 1."
                        )

                    # если объект не новый (возможно у него есть дети)
                    if Organization.objects.filter(pk=self.pk).exists():

                        # print(f"дети: {Organization.objects.filter(provider=self)}")

                        # проверка детей (детей не может быть):
                        if Organization.objects.filter(provider=self):
                            raise ValidationError(
                                "В иерархической структуре не может быть больше трех уровней 2."
                            )

        if self.provider == self:
            raise ValidationError("Нельзя быть поставщиком себе.")

        if self.status == "Завод" and not self.debt == 0:
            raise ValidationError(
                "У Завода не может быть задолженности, т.к. нет поставщика."
            )

    class Meta:
        verbose_name = "организация"
        verbose_name_plural = "организации"


class Product(models.Model):
    """
    Название,
    модель,
    дата выхода продукта на рынок.
    """

    name = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name="Название продукта",
    )
    product_model = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name="Модель продукта",
    )
    release_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="дата выхода продукта на рынок",
    )

    def __str__(self):
        return f"Product {self.name} ({self.product_model}, {self.release_date})"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
