from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from listings.models import Listing, Category, Wishlist
from messaging.models import Conversation, Message
from notifications.models import Notification

User = get_user_model()

class CampusExchangeBuyingTests(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(
            username='user1', 
            college_email='user1@kiet.edu', 
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2', 
            college_email='user2@mycollege.in', 
            password='password123'
        )
        
        # Create category
        self.category = Category.objects.create(name='Books', slug='books')
        
        # Create listing
        self.listing = Listing.objects.create(
            title='Test book',
            description='A test book description',
            price=250,
            listing_type='sell',
            category=self.category,
            seller=self.user2,
            hostel_location='Hostel A',
            status='available'
        )
        
        # Setup clients
        self.client1 = Client()
        self.client1.login(username='user1', password='password123')
        
        self.client2 = Client()
        self.client2.login(username='user2', password='password123')

    def test_toggle_wishlist(self):
        # Initial check
        self.assertFalse(Wishlist.objects.filter(user=self.user1, listing=self.listing).exists())
        
        # Toggle Wishlist
        url = reverse('listings:toggle_wishlist', kwargs={'pk': self.listing.pk})
        response = self.client1.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['wishlisted'])
        self.assertEqual(data['count'], 1)
        self.assertTrue(Wishlist.objects.filter(user=self.user1, listing=self.listing).exists())
        
        # Toggle again (remove)
        response = self.client1.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['wishlisted'])
        self.assertEqual(data['count'], 0)
        self.assertFalse(Wishlist.objects.filter(user=self.user1, listing=self.listing).exists())

    def test_wishlist_page(self):
        # Add to wishlist
        Wishlist.objects.create(user=self.user1, listing=self.listing)
        
        url = reverse('listings:wishlist')
        response = self.client1.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test book')

    def test_message_notification(self):
        # Start user conversation
        url = reverse('messaging:start_user_conversation', kwargs={'user_id': self.user2.pk})
        response = self.client1.get(url)
        
        # Verify conversation created
        conversation = Conversation.objects.get(buyer=self.user1, seller=self.user2)
        self.assertIsNotNone(conversation)
        
        # Send message
        msg_url = reverse('messaging:conversation', kwargs={'pk': conversation.pk})
        msg_response = self.client1.post(msg_url, {'body': 'Hey is this still available?'})
        
        self.assertEqual(msg_response.status_code, 302) # Redirects to page to refresh
        
        # Check that message was created
        messages_count = Message.objects.filter(conversation=conversation).count()
        self.assertEqual(messages_count, 1)
        
        # Check notification created for recipient (user2)
        notifications = Notification.objects.filter(recipient=self.user2)
        self.assertEqual(notifications.count(), 1)
        self.assertEqual(notifications.first().notification_type, 'message')
        self.assertIn('user1', notifications.first().title)

    def test_wishlist_sold_notification(self):
        # user1 wishlists user2's listing
        Wishlist.objects.create(user=self.user1, listing=self.listing)
        
        # user2 marks listing as sold
        status_url = reverse('listings:mark_status', kwargs={'pk': self.listing.pk, 'status': 'sold'})
        response = self.client2.get(status_url)
        self.assertEqual(response.status_code, 302)
        
        # Verify status is sold
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.status, 'sold')
        
        # Check notification created for user1 (wishlist holder)
        notifications = Notification.objects.filter(recipient=self.user1)
        self.assertEqual(notifications.count(), 1)
        self.assertEqual(notifications.first().notification_type, 'wishlist_sold')
        self.assertIn('Test book has been sold', notifications.first().title)

    def test_public_profile(self):
        # Access user2's profile as user1
        url = reverse('public_profile', kwargs={'username': 'user2'})
        response = self.client1.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user2')
        self.assertContains(response, 'Verified Student')
