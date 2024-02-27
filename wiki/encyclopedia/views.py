# from django import forms
# import Re module to work with Regular Expressions 
import re
from django.shortcuts import render
from django.http import HttpResponse

#use to convert markdwon to HTML https://github.com/trentm/python-markdown2
from markdown2 import Markdown
from . import util

# used for the random page display
import random





def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def encyclopedia_entry(request,name):

    # We get the entry in .md 
    entry = util.get_entry(name)
    # print(entry)
   
    if entry == None:
        # return code 404 and renders error page
        return render(request, "encyclopedia/404.html",status=404)
    else: 
         # Convert .md file to HTML. Notice in HTML template "entries.html" it's necessary to use {% autoescape off %} to render html correctly
         # https://stackoverflow.com/questions/65052048/how-to-disable-autoescape-when-using-django-template-from-string-and-render
        markdowner = Markdown()
        markdown_entry = markdowner.convert(entry)

        return render(request, "encyclopedia/entries.html", {
            "entry": markdown_entry,
            "name": name.capitalize()
        })


def search(request):
    
    # ref:https://stackoverflow.com/questions/150505/how-to-get-get-request-values-in-django
    query = request.GET.get('q', '') #string
    print(query)

    # If the search matches a result exactly it will return the page. It compares capital and lower case automatically so css,Css,etc CSS will provide the same result
    entry = util.get_entry(query)

    # IF the query doesn't match any of the results it will return none the util.get_entry(query) 
    # Therefore we try to approximate what the user wants and create a list that for example.
    # The user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were ytho, then Python should appear in the search results.
    # Include csrf_token in the HTML to avoid attacks.
    if entry == None:
        # We get the complete list of entries in a dictionary
        entries= util.list_entries() 
        # print(entries)  
        # Create an empty list to include the ones that are approx the same that have the query as a substring
        listshow = []

        # Iterate to the complete list of entries and compare them using regex function search. If there's a match it will include the entry in the empty list "listshow" 
        for element in entries:
            x = re.search(query.lower(), element.lower())
            if x != None:             
                 listshow.append(element)

        # If there are not results return empty True and inform users there are no results matching that query
        lenlist = len(listshow)
        if lenlist == 0:
            return render(request, "encyclopedia/search.html", {
                "empty": True
                }) 

        # If there are results we show the list of entries
        else:
            # print(listshow)
            # We pass the list to the HTML so they can render it accordingly in the search.html page
            return render(request, "encyclopedia/search.html", {
            "entries": listshow
        })
    else:
        # Convert .md file to HTML. Notice in HTML template "entries.html" it's necessary to use {% autoescape off %} to render html correctly
        # https://stackoverflow.com/questions/65052048/how-to-disable-autoescape-when-using-django-template-from-string-and-render
        markdowner = Markdown()
        markdown_entry = markdowner.convert(entry)

        return render(request, "encyclopedia/entries.html", {
            "entry": markdown_entry, 
            "name": query.capitalize()
        })

     

def newpage(request, title=None, content=None):

    if request.method == "POST":
        # Get the title and the content from HTML page. (Easier to do importing forms from django but we are following alternative method)
        # To obtain the title, it is used the **name** in the HTML
        title = request.POST.get('title', None)       
        content = request.POST.get('content', None)

        print(title)
        print(content)

        #to remove leading and trailing whitespace from the title
        title = title.strip()

        

        if not title or not content:
            error_message = "Title and content are required."
            return render(request, "encyclopedia/error.html", {"error_message": error_message})
        
        # If an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
        elif util.get_entry(title):
            error_message = "Wiki Entry Already Exists! Please access it in the home page or search it to edit it."
            return render(request, "encyclopedia/error.html", {"error_message": error_message})
        
        # If it doesn't exist user can save new page
        else:
            # Format title so it can be saved correctly in the .md
            str1 = '# '
            newline = '\n'
            mdtitle = str1 + title + newline
            content = mdtitle + content

            # calling util module and use the save function to save the entry
            # The title should not have any space at the end otherwise it will nosave in md correctly. With the .strip() function it helps us to solve this
            util.save_entry(title, content)

            entry = util.get_entry(title)

            markdowner = Markdown()
            markdown_entry = markdowner.convert(entry)

            return render(request, "encyclopedia/entries.html", {
                "entry": markdown_entry, 
                "name": title.capitalize()
            })


    return render(request, "encyclopedia/new_page.html")        



def editpage(request, title=None):


    if request.method == "POST":
        # Get the title and the content from HTML page. (Easier to do importing forms from django but we are following alternative method)
        # To obtain the title, it is used the **name** in the HTML
        title = request.POST.get('title', None)       
        content = request.POST.get('content', None)

        print(title)
        print(content)

        #to remove leading and trailing whitespace from the title
        title = title.strip()

        if not title or not content:
            error_message = "Title and content are required."
            return render(request, "encyclopedia/error.html", {"error_message": error_message})
        
        else:
            # Format title so it can be saved correctly in the .md
            str1 = '# '
            newline = '\n'
            mdtitle = str1 + title + newline
            content = mdtitle + content

            # calling util module and use the save function to save the entry
            # The title should not have any space at the end otherwise it will nosave in md correctly. With the .strip() function it helps us to solve this
            util.save_entry(title, content)

            entry = util.get_entry(title)

            markdowner = Markdown()
            markdown_entry = markdowner.convert(entry)

            return render(request, "encyclopedia/entries.html", {
                "entry": markdown_entry,
                "name": title.capitalize()
            })

    entry = util.get_entry(title)

    # Remove title from "entry" so when a user makes the POST is store without including in the content another title.
    x = list(entry)
    # print(x)

    for i, char in enumerate(x):
        # slice title between "#"" and "\n" and break once "\n" is found
        if char == "\n":
            x = x[i+1:]
            break
    #conver the whole list to string after removing title    
    x = ''.join(x)
    # print(x)

    content = x

    return render(request, "encyclopedia/edit_page.html", {
                "title": title,
                "content": content
            })

def randompage(request):

    list = util.list_entries()
    # print(list)
    # print(len(list))

    #returns a random number between 0 (included) and len(list) (not included the number). It works because in the list indexes starts from "0" until "len(list)-1"
    r_number = random.randrange(0, len(list))
    # print(r_number)
    
    #selects the entry to display
    # print(list[r_number])
    random_title = list[r_number]


    entry = util.get_entry(random_title)
    markdowner = Markdown()
    markdown_entry = markdowner.convert(entry)

    return render(request, "encyclopedia/entries.html", {
        "entry": markdown_entry, 
        "name": random_title.capitalize()
    })