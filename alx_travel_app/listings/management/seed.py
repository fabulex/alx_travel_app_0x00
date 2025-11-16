from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from datetime import timedelta
from decimal import Decimal
from listings.models import User, Listing, Booking, Review
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with sample listings, bookings, and reviews'

    def handle(self, *args, **kwargs):
        # Clear existing data for clean seed
        Booking.objects.all().delete()
        Review.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.filter(is_host=False).delete()  # Keep superuser if needed; delete guests

        # Create sample hosts with unique usernames
        hosts = []
        host1 = User.objects.create_user(
            username="host1_unique",  # Made unique
            password="pass12345",
            email="host1@example.com",
            is_host=True
        )
        hosts.append(host1)
        for i in range(2):  # Additional dynamic hosts with unique usernames
            username = f"{fake.user_name()}_{i+1}"  # Append index for uniqueness
            host = User.objects.create_user(
                username=username,
                email=fake.email(),
                password='pass123',
                is_host=True,
                phone_number=fake.phone_number()
            )
            hosts.append(host)

        # Sample data (use 'title' as per model)
        hardcoded_data = [
            {
                "host": host1,
                "title": "Beach House",
                "description": "Nice house near the beach.",
                "country": "Morocco",
                "city": "Agadir",
                "address": "Beach Road 1",
                "price_per_night": Decimal('90.00'),
                "bedrooms": random.randint(1, 3),
                "bathrooms": Decimal('2.0'),
                "guests": 4,
            },
            {
                "host": host1,
                "title": "Mountain Cabin",
                "description": "Cozy cabin with forest view.",
                "country": "Morocco",
                "city": "Ifrane",
                "address": "Pine Street 12",
                "price_per_night": Decimal('120.00'),
                "bedrooms": random.randint(2, 4),
                "bathrooms": Decimal('1.5'),
                "guests": 6,
            },
        ]
        dynamic_data = []
        for host in hosts[1:]:
            dynamic_data.append({
                "host": host,
                "title": fake.catch_phrase(),
                "description": fake.paragraph(nb_sentences=3),
                "country": fake.country(),
                "city": fake.city(),
                "address": fake.street_address(),
                "price_per_night": Decimal(str(random.uniform(50, 300))),
                "bedrooms": random.randint(1, 5),
                "bathrooms": Decimal(str(random.uniform(1, 3))),
                "guests": random.randint(1, 8),
            })

        sample_data = hardcoded_data + dynamic_data
        listings = []
        for item in sample_data:
            listing = Listing.objects.create(**item)
            listings.append(listing)

        # Create sample guests with unique usernames
        guests = []
        for i in range(5):
            username = f"guest_{fake.user_name()}_{i+1}"  # Unique with index
            guest = User.objects.create_user(
                username=username,
                email=fake.email(),
                password='pass123'
            )
            guests.append(guest)

        # Create sample bookings (as before)
        for listing in listings:
            for _ in range(random.randint(1, 3)):
                guest = random.choice(guests)
                check_in = fake.date_between(start_date='-1y', end_date='today')
                check_out = check_in + timedelta(days=random.randint(3, 14))
                total_price = listing.price_per_night * (check_out - check_in).days

                booking = Booking.objects.create(
                    user=guest,
                    listing=listing,
                    check_in=check_in,
                    check_out=check_out,
                    total_price=total_price,
                    status=random.choice(['pending', 'confirmed', 'canceled'])
                )

                # Add review if confirmed
                if booking.status == 'confirmed' and random.random() > 0.5:
                    Review.objects.create(
                        booking=booking,
                        rating=random.randint(1, 5),
                        comment=fake.sentence()
                    )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully seeded {len(listings)} listings with bookings and reviews!')
        )
