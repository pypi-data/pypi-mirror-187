
------------
Pretty-Forms
------------

A Django built-in forms and model forms libraries modification that decorates
the forms using the Bulma CSS framework allowing further customization
posibilities without the need of editing a CSS file.

It works like a replacement of the original Django forms libraries importing
the Form or ModelForm objects from `prettyforms` module and using them instead of
the ones provided by Django.

It requires that the template being rendererd  has loaded the https://bulma.io/
static file loaded to work. This can be included from CDN repository:
 
 * https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css
