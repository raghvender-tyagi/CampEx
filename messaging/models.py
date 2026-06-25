from django.db import models
from django.conf import settings

class Conversation(models.Model):
    listing = models.ForeignKey('listings.Listing', on_delete=models.SET_NULL, 
                                 null=True, related_name='conversations')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='buying_conversations')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='selling_conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('listing', 'buyer', 'seller')
        ordering = ['-created_at']

    def __str__(self):
        listing_title = self.listing.title if self.listing else "Deleted Listing"
        return f"Chat on {listing_title} between {self.buyer.username} and {self.seller.username}"

    @property
    def last_message(self):
        return self.messages.order_by('created_at').last()

    def unread_count_for_user(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()

    def get_other_user(self, user):
        return self.seller if user == self.buyer else self.buyer

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,
                                      related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at}"
