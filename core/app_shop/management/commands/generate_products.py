import os
import random
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify

from app_account.models import User
from app_shop.models import Product, ProductCategory, ProductStatusType


class Command(BaseCommand):
    help = "Seed the database with fake products (with images)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            type=int,
            default=10,
            help="Number of products to create"
        )

    def handle(self, *args, **kwargs):
        fake = Faker('fa_IR')
        total = kwargs["total"]

        user = User.objects.filter(is_active=True, is_superuser=True)
        categories = list(ProductCategory.objects.all())
        images = ['img{}.jpg'.format(n) for n in range(1, 11)]
        images_path = os.path.join("static", "defaults", "random_products")

        if not user:
            self.stdout.write(self.style.ERROR("User not found."))
            return
        if not categories:
            self.stdout.write(self.style.ERROR("No categories found. Please create at least 1 category."))
            return

        for _ in range(total):
            title = " ".join(fake.words(nb=3)).title()

            product = Product.objects.create(
                user=user[0],
                title=title,
                slug=slugify(title, allow_unicode=True),
                stock=random.randint(0, 100),
                price=fake.random_int(min=10, max=500)*1000,
                discount_percent=random.choice([0, 10]),
                status=random.choice([ProductStatusType.publish.value, ProductStatusType.draft.value]),
                description=fake.text(max_nb_chars=500),
                brief_description=fake.text(max_nb_chars=300),
            )

            # Assign 1–3 random categories
            chosen_cats = random.sample(categories, k=random.randint(1, min(3, len(categories))))
            product.category.add(*chosen_cats)

            # Pick a random image from the list
            img_name = random.choice(images)
            img_path = os.path.join(images_path, img_name)

            if os.path.exists(img_path):
                with open(img_path, "rb") as f:
                    product.image.save(img_name, File(f), save=True)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {total} products with images."))
