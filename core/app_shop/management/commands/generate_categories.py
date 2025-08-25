from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
from app_shop.models import ProductCategory


class Command(BaseCommand):
    help = "Seed the database with fake product categories"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            type=int,
            default=10,
            help="Number of categories to create"
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs["total"]

        for _ in range(total):
            title = fake.word()
            ProductCategory.objects.create(
                title=title,
                slug=slugify(title, allow_unicode=True)
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {total} categories."))
