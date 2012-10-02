=============
Cutting Board
=============

Cutting Board is a simple template workspace which allows you to build static  
HTML pages while taking advantage of the jinja2 templating language. 

Requirements
------------
python >= 2.6
flask

Basic Usage
-----------
To run the local development server on localhost:8000:

  ./cb.py

Your templates will be served at a path relative to the "templates" directory, 
without the .html extension. For example, to view "templates/foo/bar.html", 
you'd use "http://localhost:8000/foo/bar".

To run the local development server on 192.168.1.2:80:

  ./cb.py 192.168.1.2:80

To build your templates into static html:

  ./cb.py -b index foo/index foo/bar -o /path/to/output/dir

To build an archive of the html dir, just add -z:

  ./cb.py -b index foo/index foo/bar -o /path/to/output/dir -z

In this case, a file called "dir.zip" will be created in /path/to/output.
