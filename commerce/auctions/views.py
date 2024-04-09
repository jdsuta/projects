from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

# to control race conditions
from django.db import transaction

from .models import *
from django.db.models import Max
from .forms import AuctionForm


# https://stackoverflow.com/questions/9834038/django-order-by-query-set-ascending-and-descending
# the show the most recent item:
# - before column "creation_date" means "descending order", while without - mean "ascending".
def index(request):
    userid = request.user.id
    Auctions = Auction.objects.all().order_by('-creation_date').annotate(highest_bid = Max('item_bid__price_offered'))
    # annotate() function in Django is used to add annotations to each object in a queryset. 
    # Here is instructing Django to calculate the maximum value of the price_offered field across all related Bid objects for each Auction
    # We loop through every item in auctions and check if there's an "auction_winner" for each item.
    # If there's an auction_winner, we will set the temp value (temporary_winner) to True for that item.
    # The temporary value is dynamically added to each Auction object.
    # Then, the queryset Auctions with the temporary values is transferred to the HTML template.
    
    for auction in Auctions:
        bidwinner = Bid.objects.filter(item=auction, auction_winner=True).first()
        if bidwinner is not None:
            bidwinner = bidwinner.bidder_id
            # print(userid)
            if bidwinner == userid:
                # print('They are the same wohoo!')
                bidwinner = 1
            else:
                bidwinner = 2
        else:
            bidwinner = 0   
        
        # Dynamically add a temporary_winner attribute to each auction object
        auction.temporary_winner = bidwinner
        with transaction.atomic():
            auction.save()
    
    # for auction in Auctions:
    #     print(f"{auction.item} - Bid Winner: {auction.temporary_winner}")
    # If I try to do this Auction.objects.all().order_by('-creation_date') or manipulate Auxctions after I have assigned the temporary value it get lost. 
    # So Manipulate before assigning the temp value first
        
    return render(request, "auctions/index.html", {
        "Items": Auctions
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# https://forum.djangoproject.com/t/using-request-user-in-forms-py/19184
# To pass the user logged in, in the form

@login_required
def create_listing(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            # Assign the current authenticated user to the user field of the Auction instance
            form.instance.user = request.user
            # print(request.user)
            form.save()
            return HttpResponseRedirect(reverse("index"))  # Redirect to a success page or another view
    else:
        form = AuctionForm()

    return render(request, 'auctions/create_listing.html', {'form': form})


def listings(request, item=None):
    
    if request.method == "POST":
        
        item = request.POST.get('itemid') 
        # userid = request.POST.get('userid')
        userid = request.user.id 
        watchlist_param = request.POST.get('watchlist')
        closebid_param = request.POST.get('closebid_param')
        comment = request.POST.get('comment')
        # pricedb = request.POST.get('pricedb')
        
        # Neccesary to pass closebid_param to render page correctly
        if closebid_param == 'True':
            winner = True
        else:
            winner = False
            
        # Neccesary to pass watchlist to render page correctly
        if watchlist_param == 'True':
            watchlist = True
        else:
            watchlist = False       
    
        
        #This is to check which form was submitteed in this case the form for watchlist
        form_type = request.POST.get('form_type')    
        
        # If item is watchlisted to delete froom the DB and return new valor "watchlist"
        # If item is not watchlisted it will add it to the DB and return new value for "watchlist"
        # In Django, when you define a ForeignKey or ManyToManyField 
        # relationship between models, you can reference fields of related 
        # models using double underscores (__). "following relationships backward" 
        # items__id is used tp tell that you want to filter the Watchlist objects based on the id field of related items.

        ######## Watchlist form
        if form_type == 'watchlist':  
            if watchlist_param == 'True':
                try:
                    #  to ensure that all database operations within the block are executed within a single transaction. Race conditions control
                    with transaction.atomic():
                        Watchlist.objects.get(user_id=userid, items__id=item)
                        
                        # command to delete the object from the DB
                        # https://stackoverflow.com/questions/3805958/how-to-delete-a-record-in-django-models
                        Watchlist.objects.filter(user_id=userid, items__id=item).delete()
                        
                    watchlist = False
                    
                except Watchlist.DoesNotExist:
                    return HttpResponseBadRequest("The watchlist entry does not exist.")
                    
            elif watchlist_param == 'False':
                try:
                    with transaction.atomic():
                        # Because is needed the username
                        user = request.user
                        watchlistdb = Watchlist(user=user)
                        watchlistdb.save()
                        # Add the item to the watchlist
                        watchlistdb.items.add(item)
                            
                    watchlist = True             
                except Exception as e:
                    return HttpResponseBadRequest("Error occurred while adding to watchlist: " + str(e))               
            
        ######## Bidding form
        elif form_type == 'bid':        
            try:
                # to capture the number entered 
                proposedbid = request.POST.get('bid')
                username = request.user
                
                try:
                    higher_priceBid = Bid.objects.filter(item=item).order_by('-price_offered').first()
                    winner = higher_priceBid.auction_winner 
                    if winner == True:
                        return HttpResponseBadRequest("This bid has been closed and not new bids are allowed, please refresh this page and go to active listing page and select a new item")  
                    else:
                        pass
                except (Bid.DoesNotExist, AttributeError):
                    pass                        
                    
                #  to ensure that all database operations within the block are executed within a single transaction. Race conditions control
                with transaction.atomic():                                       
                    higher_priceBid = Bid.objects.filter(item=item).order_by('-price_offered').first()
                    
                    if higher_priceBid is not None:
                        higher_priceBid = float(higher_priceBid.price_offered)
                        
                        proposedbid = float(proposedbid)
                        print(f'Proposed bid is { proposedbid } type: {type(proposedbid)}')
                        
                        if proposedbid > higher_priceBid:
                            auction = Auction.objects.get(pk=item)
                            b = Bid(item = auction, bidder = username, price_offered = proposedbid)
                            b.save()
                        else:
                            return HttpResponseBadRequest("The Proposed Bid should be greater than previously placed bids. Please refresh the page")  
                

                    # If there's not a bid it will create one                
                    else:
                        auction = Auction.objects.get(pk=item)
                        # print(auction)
                        b = Bid(item = auction, bidder = username, price_offered = proposedbid)
                        # print(b)
                        b.save()               
                                      
            except ValueError:
                return HttpResponseBadRequest("Invalid bid value. Please enter a valid number.")

        ######## Close bidding
        elif form_type == 'close_bid':          
            if closebid_param == 'False':
                try:
                    itembid = Auction.objects.get(id=item)
                    auctioner = itembid.user_id
                    user = request.user.id
                    
                    if user == auctioner:
                        with transaction.atomic():
                            # Get the highest bid for the item
                            try:
                                higher_priceBid = Bid.objects.filter(item=item).order_by('-price_offered').first()
                                higher_priceBid.auction_winner = True
                                higher_priceBid.save()
                                winner = True
                            except Bid.DoesNotExist:
                                return HttpResponseBadRequest("No bids exist for this auction.")
                    else:
                        return HttpResponseBadRequest("You are not authorized to close this auction.")
                    
                except Auction.DoesNotExist:
                    return HttpResponseBadRequest("The specified auction does not exist.")
                
            elif closebid_param == 'True':
                try:
                    itembid = Auction.objects.get(id=item)
                    auctioner = itembid.user_id
                    user = request.user.id
                    
                    if user == auctioner:
                        with transaction.atomic():
                            # Get the highest bid for the item
                            try:
                                higher_priceBid = Bid.objects.filter(item=item).order_by('-price_offered').first()
                                higher_priceBid.auction_winner = False
                                higher_priceBid.save()
                                winner = False
                            except Bid.DoesNotExist:
                                return HttpResponseBadRequest("No bids exist for this auction.")
                    else:
                        return HttpResponseBadRequest("You are not authorized to close this auction.")
                    
                except Auction.DoesNotExist:
                    return HttpResponseBadRequest("The specified auction does not exist.")
        
        ######## Comment Section
        elif form_type == 'comment':
            try:
                with transaction.atomic():
                    # print(userid)
                    # print(item)
                    # print(comment)
                    commentdb = Comment(item_id=item,commenter_id=userid, comment = comment)
                    commentdb.save()                
            except Exception as e:
                    return HttpResponseBadRequest("Error occurred while adding comment" + str(e))               

    else:
        # To check item id is passing
        # print(item)
        # To check the user authenticated
        # print(request.user)
        
        #### GET ####
        ## gets user id
        userid = request.user.id

        try:
            watchlist_item = Watchlist.objects.get(user_id=userid, items__id=item)
            # print(watchlist_item)
            # If item is watchlisted it will return a True 
            watchlist = True
            
        except Watchlist.DoesNotExist:
            watchlist = False
 
    ### Common for post and get
    try:
        watchlist_item = Watchlist.objects.get(user_id=userid, items__id=item)
        watchlist = True
    except Watchlist.DoesNotExist:
        watchlist = False

   
    try:
        itemdb = Auction.objects.get(id=item)
        pricedb = float(itemdb.price)
        # print(type(pricedb)) 
        
        # Close Bid
        auctioner = Auction.objects.get(id=item)
        auctioner = auctioner.user_id
        # print(auctioner)
        # print(user)
        
        # If auctioner is equal to user it means they can see the button to close bid. Otherwise they won't see anything if they are logged out or don't own the item

        if auctioner == userid:
            closebid = 1
            try: 
                higher_priceBid = Bid.objects.filter(item=item).order_by('-price_offered').first()
                winner = higher_priceBid.auction_winner
            except (Bid.DoesNotExist, AttributeError):
                winner = 0
                    
        else:
            try: 
                higher_priceBid = Bid.objects.filter(item=item).order_by('-price_offered').first()
                print(higher_priceBid)
                winner = higher_priceBid.auction_winner
            except (Bid.DoesNotExist, AttributeError):
                winner = 0
            closebid = 0    
                    
    except Auction.DoesNotExist:
        return HttpResponseBadRequest("The Auction entry does not exist.")

    # checks largest bid and passes this value to the FE.    
    higher_priceBid = Bid.objects.filter(item=item).order_by('-price_offered').first()
    if higher_priceBid is not None:
        higher_priceBid = float(higher_priceBid.price_offered)
        Bid.objects.filter(item=item).order_by('-price_offered')
        bidscount = Bid.objects.filter(item=item).count()
        uid_db = Bid.objects.filter(item=item).order_by('-price_offered').first().bidder_id
        userid = request.user.id
        if uid_db == userid:
            log_samebidder = 1            
        else:
            log_samebidder = 0

    else:
        # If there are not bids, there are no bids count and therefor no samebidder
        higher_priceBid = 0
        bidscount = 0
        log_samebidder = 0
  
    # Checking bid winner if the logged in user is the winner of the auction it will display in the page the message that has won
    # The logic is if they are the same bidwinner = 1 otherwise bidwinner = 0
    bidwinner = Bid.objects.filter(item=item, auction_winner=True).first()
    if bidwinner is not None:
        bidwinner = bidwinner.bidder_id
        # print(userid)
        if bidwinner == userid:
            # print('They are the same wohoo!')
            bidwinner = 1
        else:
            bidwinner = 0
    else:
        bidwinner = 0
    # print(bidwinner)   
    
    # Retrieving comments to display
    
    comments = Comment.objects.filter(item_id=item)
    # print(comments)
     
    
    
    return render(request, "auctions/listings.html", {
        "item": Auction.objects.get(id=item),
        "isWatchlisted": watchlist,
        "pricedb": pricedb,
        "higher_priceBid" : higher_priceBid,
        "bidscount" : bidscount,
        "log_samebidder" : log_samebidder,
        "closebid" : closebid ,
        "closebid_param" : winner,
        "user_bidwinner" : bidwinner,
        "comments" : comments
    })



@login_required
def watchlist(request):
    
    userid = request.user.id
    Auctions = Auction.objects.all().order_by('-creation_date')
    
    # Need to save it first before calling watclist items and to avoid bugs. 
    for auction in Auctions:
        bidwinner = Bid.objects.filter(item=auction, auction_winner=True).first()
        
        if bidwinner is not None:
            bidwinner = bidwinner.bidder_id
            # print(userid)
            if bidwinner == userid:
                # print('They are the same wohoo!')
                bidwinner = 1
            else:
                bidwinner = 2
        else:
            bidwinner = 0   
        
        # Dynamically add a temporary_winner attribute to each auction object
        auction.temporary_winner = bidwinner
        with transaction.atomic():
            auction.save()    
    
    watchlisted_items = Watchlist.objects.filter(user_id=userid)
    # print(watchlisted_items)
    
    return render(request, 'auctions/watchlist.html', {
        "watchlisted_items": watchlisted_items
    })


def categories(request):
    # Will store all the current categories in the page.
    categories = Auction.objects.values('category').distinct()
    
    return render(request, 'auctions/categories.html', {
        "categories": categories
    })

def categories_specific(request, category):
    
    userid = request.user.id
    Auctions = Auction.objects.all().order_by('-creation_date')
    
    # Need to save it first before calling watclist items and to avoid bugs. 
    for auction in Auctions:
        bidwinner = Bid.objects.filter(item=auction, auction_winner=True).first()
        
        if bidwinner is not None:
            bidwinner = bidwinner.bidder_id
            # print(userid)
            if bidwinner == userid:
                # print('They are the same wohoo!')
                bidwinner = 1
            else:
                bidwinner = 2
        else:
            bidwinner = 0   
        
        # Dynamically add a temporary_winner attribute to each auction object
        auction.temporary_winner = bidwinner
        with transaction.atomic():
            auction.save()
    
    cat = category
    # print(cat)
    
    Auction_categoriy_filtered = Auction.objects.filter(category=cat)
    #print(Auction_categoriy_filtered)
    
    # We need to grab each auction with that category and display it accordingly.
    return render(request, 'auctions/categories_specific.html', {
        "ItemsCAtegorized": Auction_categoriy_filtered,
        "category" : cat
    })  

    

'''
super user
david
panzas123


Django ModelForm – Create form from Models

https://www.geeksforgeeks.org/django-modelform-create-form-from-models/

'''