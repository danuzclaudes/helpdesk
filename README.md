This is an example of a simple web API implemented using
[Flask](http://flask.pocoo.org/) and
[Flask-RESTful](http://flask-restful.readthedocs.org/en/latest/).

To run it:

1. Install required dependencies:
   ```
   $ pip install -r requirements.txt
   ``` 
   [Flask](http://flask.pocoo.org/docs/0.10/installation/#installation)
   and
   [Flask-RESTful](http://flask-restful.readthedocs.org/en/latest/installation.html) to run `server.py` 
   and [RDFLib](http://rdflib.readthedocs.org/en/latest/) and [JSONLD for RDFLib](https://github.com/RDFLib/rdflib-jsonld) to run the `extractdata.py` script or the `another-server.py` service.

2. Run the helpdesk server:
   ```
   $ python server.py
   ```
   Alternatively, you can access the service running here: http://127.0.0.1:5555/notebook
   
3. Use the `extractdata.py` script to examine the triples found in various representations of the helpdesk resources.
   
   RDFa/microdata for the list of help requests:
   ```
   $ python extractdata.py http://127.0.0.1:5555/notebook
   ```
   JSON-LD for the list of help requests:
   ```
   $ python extractdata.py http://127.0.0.1:5555/notebook.json
   ```
   RDFa/microdata for an individual help request:
   ```
   $ python extractdata.py http://127.0.0.1:5555/note/note1
   ```
   JSON-LD for an individual help request:
   ```
   $ python extractdata.py http://127.0.0.1:5555/note/note1.json
   ```

4. Run the contact server for an example of a service calling another service:
   ```
   $ python another-server.py
   ```

   Alternatively, you can access the service running here: http://127.0.0.1:5556/contacts.json

--------------------------------------------------------------------------------------------------------

####INLS 620 Web Information Organization Project
####Scholarly Notebook Service Documentation

Our website compiles notes on a senator which, for the purpose of this project, are merely commentary on the life of a make-believe senator, ‘Senator Shaw’. This design can be used to write political articles about a senator such as [this one](http://bobgrahamnow.com/).


The website was designed to allow for flexibility of purpose. Each individual note is defined with:
- `title`
- `note_content`
- `author`


Underneath `author`, the code defines `profile_URL` and `name`, which give a LinkedIn profile and the name of the author, and `@type` as `foaf:person`. In this format, the note title, content, and author can be added by the user in `json` language.


Here are some features of our notebook application:
- From the website, each note can be sorted based on title, author, and date.  
    - This allows for the user to find specific notes without going through the entire list.  

- A new note can be created via the button on the notebook’s front page.  
    - This will take the user to the note page where they can add author and note content.

- The content of each note always appears as a text box through which the user can read or edit the content.  
    - This is to allow for easier editing, but can be risky since anyone who opens a note after it is created  can edit its entire contents.
    - Thus, it is best for a website such as this to be protected with a login and password to protect the edit function and to protect the authorship rights of those writing the notes.

- The website also represents tweets from Twitter API service.
    - This takes advantage of the machine-readable data provided by 3rd party service


The `JSON-LD @context` is defined with the following:
```
{“note”: "https://schema.org/CreativeWork",
"notes": {
  "@id": "http://www.w3.org/2000/01/rdf-schema#member",
  "@container": "@index" },
"author": {
   "@id": "http://purl.org/dcterms/creator",
   "@type": "foaf:person" },
"profile_url": "@id",
"name": "http://schema.org",
"title": "http://schema.org/title",
"note_content": "http://schema.org/text",
"date": {
   "@id": "http://schema.org/dateCreated",
   "@type": "http://w3.org/2001/xml/schema#date" },
"foaf": "http://purl.org/foaf" }
```


The classes defined in `/notebook` are:
* notes-table: the parent tag of the table which lists all notes
* note: a specific note
* title: the title of the note
* author: the author of the note
* date: the created date of the note
* createNote: indicates the usage of the form is to create a new note


The `rel` defined in `/notebook`:
* collection: describes the list of notes
* item: describes a specific note

                        
The classes defined in `/note` are:
* title: specifies the title of note
* author: the author of the note
* content: the text paragraph of note
* updateNote: indicates the usage of the form is to update the note content

