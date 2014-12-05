To generate and build the API documentation, you'll need sphinx, jinja2
and sphinx\_rtd\_theme and then just run

    $ python3 autogen.py nfoview
    $ sphinx-build -b html . _build/html
