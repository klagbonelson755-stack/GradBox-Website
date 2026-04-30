from django.core.management.base import BaseCommand
from store.models import Package


class Command(BaseCommand):
    help = 'Seed the database with initial product packages'

    def handle(self, *args, **options):
        # Clear existing packages
        Package.objects.all().delete()

        packages_data = [
            {
                'name': 'Complete Facial Kit',
                'category': 'facials',
                'description': 'Everything you need for a complete facial care routine. Includes premium skincare products, moisturizing pomade, and face polish for that glowing look.',
                'items': ['Skin care set', 'Moisturizing pomade', 'Face polish', 'Cleanser', 'Toner'],
                'image_url': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400',
                'price': '150.00',
            },
            {
                'name': 'Starter Kitchen Pack',
                'category': 'foodstuffs',
                'description': 'Essential foodstuffs to get you through the semester. Perfect for students who want to cook their own meals.',
                'items': ['5kg Bag of Rice', 'Cooking Oil (2L)', 'Tomatoes (3 cans)', 'Onions (1kg)', 'Indomie (2 packs)'],
                'image_url': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400',
                'price': '200.00',
            },
            {
                'name': 'Phone Essentials Bundle',
                'category': 'phone',
                'description': 'Complete your phone setup with this essential bundle. Everything you need to protect and power your device.',
                'items': ['Phone Charger', 'AirPods/Earbuds', 'Screen Protector', 'Phone Cover/Case'],
                'image_url': 'https://images.unsplash.com/photo-1511707171634-8f898009faa0?w=400',
                'price': '350.00',
            },
            {
                'name': 'Morning Energy Pack',
                'category': 'breakfast',
                'description': 'Start your day right with this breakfast pack. Quick and easy items for busy mornings on campus.',
                'items': ['Milo (750g)', 'Milk (1L)', 'Sugar (1kg)', 'Biscuits (2 packs)', 'Tea bags'],
                'image_url': 'https://images.unsplash.com/photo-1525351484163-7529414344d8?w=400',
                'price': '80.00',
            },
        ]

        for pkg_data in packages_data:
            package = Package.objects.create(**pkg_data)
            self.stdout.write(self.style.SUCCESS(f'Created: {package.name}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nSuccessfully created {len(packages_data)} packages!'))
