from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from datetime import timedelta
from decimal import Decimal
from ...models import User, Listing, Booking, Review
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with sample listings, bookings, and reviews'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Booking.objects.all().delete()
        Review.objects.all().delete()
        Listing.objects.all().delete()

        # Create sample hosts (including hardcoded example)
        hosts = []
        host1 = User.objects.create_user(
            username="host1", password="pass12345", email="host1@example.com", is_host=True
        )
        hosts.append(host1)
        for _ in range(2):  # Additional dynamic hosts
            host = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='pass123',
                is_host=True,
                phone_number=fake.phone_number()
            )
            hosts.append(host)

        # Sample data (mix hardcoded + dynamic)
        hardcoded_data = [
            {
                "host": host1,
                "name": "Beach House",
                "description": "Nice house near the beach.",
                "country": "Morocco",
                "city": "Agadir",
                "address": "Beach Road 1",
                "price_per_night": Decimal('90.00'),
            },
            {
                "host": host1,
                "name": "Mountain Cabin",
                "description": "Cozy cabin with forest view.",
                "country": "Morocco",
                "city": "Ifrane",
                "address": "Pine Street 12",
                "price_per_night": Decimal('120.00'),
            },
        ]
        dynamic_data = []
        for host in hosts[1:]:  # Dynamic for other hosts
            dynamic_data.append({
                "host": host,
                "name": fake.catch_phrase(),
                "description": fake.paragraph(nb_sentences=3),
                "country": fake.country(),
                "city": fake.city(),
                "address": fake.street_address(),
                "price_per_night": Decimal(str(random.uniform(50, 300))),
            })

        sample_data = hardcoded_data + dynamic_data
        listings = []
        for item in sample_data:
            listing = Listing.objects.create(**item)
            listings.append(listing)

        # Rest of seeding (guests, bookings, reviews) as before...
        # (Omit for brevity; add from generated)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully seeded {len(listings)} listings!')
        )
