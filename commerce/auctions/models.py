from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    item = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=700, blank=True, null=True)
    category = models.CharField(max_length=60, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    temporary_winner = models.IntegerField(default=0)
    
    # The MinValueValidator ensures that the price is a decimal field with a minimum value of 0
    # The blank=True parameter allows the form to be submitted without entering a value for this field, and null=True allows the database to store null values.    
    # the def __str__(self) .. we can digest better the info in the admin in django
    
    def __str__(self):
        return f"{self.id}  {self.user} - {self.item}, Price - {self.price}, Description - {self.description}, Image URL - {self.image_url}, Category - {self.category}, Creation Date - {self.creation_date} - Bid Winner: {self.temporary_winner}"
    
class Bid(models.Model):
    item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="item_bid")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    price_offered = models.DecimalField(max_digits=10, decimal_places=2)
    auction_winner = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Bidder: {self.bidder} - Price Offered: {self.price_offered} for Item: {self.item.item}. Winner: {self.auction_winner}"

class Comment(models.Model):
    item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    comment = models.CharField(max_length=250)
    
    def __str__(self):
        return f"{self.commenter} commented: {self.comment}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists_users")
    items = models.ManyToManyField(Auction, blank=True, related_name="watchlists")

    def __str__(self):
        item_ids = list(self.items.values_list('id', flat=True))
        return f"{self.user} - {item_ids}"