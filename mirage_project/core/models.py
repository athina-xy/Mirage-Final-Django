from django.db import models

# Create your models here.

class Category(models.Model):
    label = models.CharField(max_length=50)
    url_name = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.label


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    label = models.CharField(max_length=50)
    url_name = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.category.label} - {self.label}"


RARITY_CHOICES = [
    ('common', 'Common'),
    ('rare', 'Rare'),
    ('legendary', 'Legendary'),
]


class Item(models.Model):
    label = models.CharField(max_length=100)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='items'
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        related_name='items'
    )

    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=7, decimal_places=2)

    # Mirage flavour fields
    element = models.CharField(max_length=30, blank=True)
    reality_fragment = models.CharField(max_length=50, blank=True)
    rarity = models.CharField(
        max_length=20,
        choices=RARITY_CHOICES,
        default='common'
    )

    # storing a path under static
    image_url = models.CharField(
        max_length=200,
        blank=True,
        help_text="Path under static/, e.g. 'images/items/emberwreath-longbow.png'"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label