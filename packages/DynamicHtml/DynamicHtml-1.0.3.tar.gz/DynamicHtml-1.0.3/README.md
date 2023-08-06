# Dynamic Html

This is a simple library to get the html of a dynamic webpage. It deals with all of the Pyppeteer code behind the scenes so you don't have to. It is also synchronous, so you don't have to mess with async functions.

## Examples
```python
from DynamicHtml import DynamicHtml

url = 'https://www.google.com'
content = DynamicHtml(url)
```
This returns the rendered html for this webpage

You can also execute Javascript code before retrieving the content like so:
```python
from DynamicHtml import DynamicHtml

url = 'https://www.google.com'
script = '() => {window.scrollBy(0, document.body.scrollHeight);}'

content = DynamicHtml(url, script)
```
This will simply scroll to the bottom of the page using Javascript before retrieving the content. This could be useful to load specific lazily loaded elements and such.
