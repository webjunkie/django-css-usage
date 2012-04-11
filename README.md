Django-css-usage
================

What is it good for?
--------------------

Django-css-usage parses a given CSS file and greps all templates available in a
project with information from the CSS. It will output selectors that appear to
have no use in any of the templates. Over client-side-checking, this has the 
benefit of really checking all the HTML that an application could possibly output.


How do I use it?
----------------

Make sure it's on your path.

Add to installed_apps:

    INSTALLED_APPS = (...
                      'css_usage',
                      ...
                      )
                       
Use command line with path to CSS file (whithin static files folder):

    manage.py css_usage css/style.css
    
See results.

History
-------

### version 0.1 - 2012-04-10

- only support for CSS classes for now