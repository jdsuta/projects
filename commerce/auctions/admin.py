from django.contrib import admin
from .models import User, Auction, Bid, Comment, Watchlist

# Define your custom admin class for Auction
# Defining custom admin classes like AuctionAdmin allows you to customize how your models are presented and interacted with in the Django admin interface. In your example:

# list_display: Specifies the fields to be displayed in the list view of the admin interface for the Auction model.
# search_fields: Allows searching for records based on the specified fields.
# list_filter: Provides filters on the right side of the admin interface to filter records based on the specified fields.

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item', 'price', 'description', 'category', 'creation_date', 'temporary_winner')
    search_fields = ('user__username','item', 'description', 'category')
    list_filter = ('category', 'creation_date')

class BidAdmin(admin.ModelAdmin):
    list_display = ('bidder', 'auction_winner', 'get_item_description', 'price_offered', 'get_item_owner')
    search_fields = ('bidder__username', 'item__description')

    def get_item_description(self, obj):
        return obj.item.description

    get_item_description.short_description = 'Item Description'
    
    def get_item_owner(self, obj):
        return obj.item.user

    get_item_owner.short_description = 'Auction Creator'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenter', 'comment', 'get_item_description')
    search_fields = ('commenter__username', 'item__description')
    
    def get_item_description(self, obj):
        return obj.item.description

    get_item_description.short_description = 'Item Description'


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_item_description')
    search_fields = ('user__username', 'items__description')
    
    def get_item_description(self, obj):
        # used in many to many relationship
        return ", ".join([str(item.description) for item in obj.items.all()])

    get_item_description.short_description = 'Item Description'
    


# Register your models here.

admin.site.register(User)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)



# list display:
# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#:~:text=Set%20list_display%20to%20control%20which,list%20page%20of%20the%20admin.&text=If%20you%20don't%20set,()%20representation%20of%20each%20object.
# Search field:
# https://adiramadhan17.medium.com/django-admin-add-search-field-4067b31a26dc
# This assumes that the Comment model has a foreign key to an Item model, and each comment is associated with a specific item.
# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/ supported by llm
# In summary I wanted to access a field of the item (foreign key)
