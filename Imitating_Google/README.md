In this project, the idea was to replicate the front-end design for Google Search, Google Image Search, and Google Advanced Search by using CSS and HTML. Additionally, we would need to use forms so we can provide the results. 

### Imitation of Google in Action

Discover the results for this task in this video

[![Watch the video](https://img.youtube.com/vi/yE5DRvgfORw/maxresdefault.jpg)](https://www.youtube.com/embed/yE5DRvgfORw)


The key part of this project was to udnerstand forms and how the queries are formed. 

# HTML

## Google Search:

For example, here is a little example on how the google index works: 

```
<form action="https://google.com/search">
    <input class="text-box" type="text" name="q" autofocus>
    <br>
    <br>
    <button class="button" type="submit" value="Google Search">Google Search</button>
    <!-- btnI used with button I'm feeling lucky it will modify the query-->
    <button class="button" type="submit" name="btnI" value="I’m Feeling Lucky">I’m Feeling Lucky</button>
</form>
```


In the code above, there are two buttons "Google Search" and "I’m Feeling Lucky". For example, when looking for the word "hello": 

- When clicking on "Google Search" the system will use this query: `https://www.google.com/search?q=hello`
- Interestingly, when clicking on "I’m Feeling Lucky" the system will use this query `https://google.com/search?q=hello&btnI=I%E2%80%99m+Feeling+Lucky`

Notice the **name** of button "I’m Feeling Lucky" is attached to the qeury `...&btnI=I%E2%80%99m+Feeling+Lucky` and changes the URL. Therefore working differently than button "Google Search"

## Google Image Search:

```
        <form action="https://google.com/search">
            <input class="text-box" type="text" name="q">
            <input type="hidden" name="tbm" value="isch" />
            <br>
            <br>
            <button class="button" type="submit" value="Google Image Search">Google Image Search</button>
        </form>
```

For the image it was necessary to add the following parameters `name="tbm" value="isch"` so when looking for an image for example cat. The URL gets formed as follows: `https://www.google.com/search?q=cat&tbm=isch` 

Notice in this case there's no other button. The query parameter was added "hidden" in the form. 
 
## Google Advance Search:

For google advance search the same principle was added. However, the idea is to figure out the parameter for every field. Here you can see the names for eevry field

- All these words ->  `name="as_q"`
- This exact word or phrase: ->  `name="as_epq"`
- Any of these words: ->  `name="as_oq"`
- None of these words: ->  `name="as_eq"`

Here the key piece of code: 

```
<form action="https://google.com/search">
            <table>
                <tr>
                    <th>
                        Find pages with…
                    </th>
                    <th>
                    </th>
                </tr>
                <tr>
                    <td>
                        all these words:
                    </td>
                    <td>
                        <input type="text" name="as_q">
                    </td>
                </tr>
                <tr>
                    <td>
                        this exact word or phrase:
                    </td>
                    <td>
                        <input type="text" name="as_epq">
                    </td>
                </tr>
                <tr>
                    <td>
                        any of these words:
                    </td>
                    <td>
                        <input type="text" name="as_oq">
                    </td>
                </tr>
                <tr>
                    <td>
                        none of these words:
                    </td>
                    <td>
                        <input type="text" name="as_eq">
                    </td>
                </tr>
                <tr>
                    <td>
                    </td>
                    <td>
                        <div class="button-container"> <!-- Container to align the button -->
                            <button class="button" id="button" type="submit" value="Advance Search">Advance Search</button>
                        </div>
                    </td>
                </tr>
            </table>
        </form>
```


# CSS 

Additionally, CSS was used to give a style to the page. What's mos interesting was getting to know the specificity order.  What happens when a header should be red based on its class but blue based on its id? 

So when determining the styles for an HTML element, CSS follows a specificity order that can result in conflicts. 

The order of specificity is as follows:

1. **In-line Styling**: Styles applied directly to an element using the `style` attribute have the highest specificity. They will override any other styles applied to the same element.

2. **ID Selector**: Styles applied through an ID selector (`#id`) have the second-highest specificity. If a class selector and an ID selector both target the same element, the ID selector takes precedence.

3. **Class Selector**: Styles applied through a class selector (`.class`) have a lower specificity compared to IDs. If both class and element type selectors target the same element, the class selector takes precedence.

4. **Element Type Selector**: Styles applied using an element type selector (e.g., `p`, `div`, `h1`) have the lowest specificity. They are the least specific and can be overridden by more specific selectors like IDs or classes.


As a reference for this I used [CS50 Web notes][cs50x-web]

<!-- Specifications accomplished in this project: 

# Website Requirements

Your website should have at least three pages:

1. **Google Search Page** (named `index.html`):
   - Include links in the upper-right corner to navigate to Image Search and Advanced Search pages.
   - Provide a search bar with rounded corners.
   - Center the search button beneath the search bar.
   - Allow users to enter a query, click "Google Search," and view Google search results.

2. **Google Image Search Page**:
   - Include a link in the upper-right corner to return to Google Search.
   - Allow users to enter a query, click a search button, and view Google Image search results.

3. **Google Advanced Search Page**:
   - Include a link in the upper-right corner to return to Google Search.
   - Allow users to input data for the following fields, similar to Google's advanced search options:
     - "Find pages with all these words:"
     - "Find pages with this exact word or phrase:"
     - "Find pages with any of these words:"
     - "Find pages with none of these words:"
   - Stack the four options vertically, and align all text fields to the left.
   - Use Google's CSS aesthetics, including a blue "Advanced Search" button with white text.

4. **"I'm Feeling Lucky" Button**:
   - Add an "I'm Feeling Lucky" button to the main Google Search page.
   - Clicking this button should take users directly to the first Google search result for the query, bypassing the normal results page.
   - Note: A redirect notice may appear due to a security feature implemented by Google.

Make sure your CSS design aligns with Google's aesthetics. -->

[cs50x-harvard]: https://cs50.harvard.edu/x/2023/
[github-imitating-google]: https://github.com/jdsuta/projects/tree/main/Imitating_Google
[cs50x-web]: https://cs50.harvard.edu/web/2020/notes/0/