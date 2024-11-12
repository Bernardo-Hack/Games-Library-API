from django.test import TestCase
from Games.models import Publisher, Game
from django.db.utils import IntegrityError
from datetime import date

# Tests for the Publisher and Game models

class PublisherModelTest(TestCase):

    def setUp(self):
        # Set up a sample Publisher
        self.publisher = Publisher.objects.create(
            name="Sample Publisher", 
            location="Sample Location", 
            website="http://samplepublisher.com"
        )

    def test_publisher_creation(self):
        # Ensure the publisher instance is created and saved properly
        self.assertEqual(self.publisher.name, "Sample Publisher")
        self.assertEqual(self.publisher.location, "Sample Location")
        self.assertEqual(self.publisher.website, "http://samplepublisher.com")
    
    def test_publisher_name_unique_constraint(self):
        # Attempt to create a publisher with a duplicate name should raise IntegrityError
        with self.assertRaises(IntegrityError):
            Publisher.objects.create(name="Sample Publisher", location="Another Location", website="http://anotherwebsite.com")

    def test_publisher_website_unique_constraint(self):
        # Attempt to create a publisher with a duplicate website should raise IntegrityError
        with self.assertRaises(IntegrityError):
            Publisher.objects.create(name="Another Publisher", location="Another Location", website="http://samplepublisher.com")


class GameModelTest(TestCase):

    def setUp(self):
        # Set up a sample publisher and a game
        self.publisher = Publisher.objects.create(
            name="Sample Publisher", 
            location="Sample Location", 
            website="http://samplepublisher.com"
        )
        self.game = Game.objects.create(
            title="Sample Game",
            description="This is a sample game description.",
            release_date=date(2022, 1, 1),
            genre="Action",
            onWindows=True,
            onMac=False,
            onLinux=True
        )
        self.game.publisher.add(self.publisher)

    def test_game_creation(self):
        # Checks if the game instance is created and saved properly
        self.assertEqual(self.game.title, "Sample Game")
        self.assertEqual(self.game.description, "This is a sample game description.")
        self.assertEqual(self.game.release_date, date(2022, 1, 1))
        self.assertEqual(self.game.genre, "Action")
        self.assertIn(self.publisher, self.game.publisher.all())

    def test_game_title_unique_constraint(self):
        # This function tries to create a game with a duplicate title, should raise IntegrityError
        with self.assertRaises(IntegrityError):
            Game.objects.create(
                title="Sample Game",
                description="Another description.",
                release_date=date(2023, 5, 15),
                genre="Adventure",
                onWindows=False,
                onMac=True,
                onLinux=False
            )

    def test_game_get_platforms(self):
        # Test the if .get_platforms returns the correct platforms
        platforms = self.game.get_platforms()
        self.assertIn("Windows", platforms)
        self.assertIn("Linux", platforms)
        self.assertNotIn("Mac", platforms)
