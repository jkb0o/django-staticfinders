About
-----
Filtered static finders for django staticfiles.
When collectstatic is called, finder check each filename.
If filename matches STATICFILES_INCLUDE and 
do not matches STATICFILES_EXLUDE then file will be 
copied, else skipped.

Install
-------

Add to settings.py::

   STATICFILES_FINDERS = (
       'staticfinders.FilteredFileSystemFinder',
       'staticfinders.FilteredAppDirectoriesFinder',
   )
   STATICFILES_INCLUDE = (
       '*.js', 
       '*.css', 
       '*.png',
       '*.jpg',
       '*.jpeg',
       '*.woff',
   )
   STATICFILES_EXCLUDE = (
       'templates*',
       'blocks*',
       'img/sprites/*/*.png'
   )

