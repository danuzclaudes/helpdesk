import io
import json
import pdb
import random
import string

from datetime import datetime
from flask import Flask, render_template, make_response, redirect
from flask.ext.restful import Api, Resource, reqparse, abort

from twitter import Twitter

# Define our priority levels.
# These are the values that the "priority" property can take on a help request.
#PRIORITIES = ('closed', 'low', 'normal', 'high')

# Load data from disk.
# This simply loads the data from our "database," which is just a JSON file.
with open('data.jsonld') as data:
    data = json.load(data)

# Generate a unique ID for a new help request.
# By default this will consist of six lowercase numbers and letters.
def generate_id(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Respond with 404 Not Found if no help request with the specified ID exists.
def error_if_note_not_found(note_id):
    if note_id not in data['notes']:
        message = "No help request with ID: {}".format(note_id)
        abort(404, message=message)


# Filter and sort a list of notes.
def filter_and_sort_notes(query='', sort_by='date'):

    # Returns True if the query string appears in the help request's
    # title or description.
    def matches_query(item):
        (note_id, note) = item
        text = note['title'] + note['note_content']
        return query.lower() in text

    # Returns the help request's value for the sort property (which by
    # default is the "time" property).
    def get_sort_value(item):
        (note_id, note) = item
        return note[sort_by]

    filtered_notes = filter(matches_query, data['notes'].items())

    return sorted(filtered_notes, key=get_sort_value, reverse=True)


# Given the data for a help request, generate an HTML representation
# of that help request.
def render_note_as_html(note):
    return render_template(
        'note.html',
        note=note)


# Given the data for a list of help requests, generate an HTML representation
# of that list.
def render_note_list_as_html(notes):
    twitter = Twitter()
    twitter.search('from:rybesh')
    return render_template(
        'notes.html',
        notes=notes,
        tdata=twitter.search('from:rybesh'))


# Raises an error if the string x is empty (has zero length).
def nonempty_string(x):
    s = str(x)
    if len(x) == 0:
        raise ValueError('string is empty')
    return s


# Specify the data necessary to create a new help request.
# "from", "title", and "description" are all required values.
new_note_parser = reqparse.RequestParser()
for arg in ['author', 'title', 'note_content']:
    new_note_parser.add_argument(
        arg, type=nonempty_string, # required=True,
        help="'{}' is a required value".format(arg))
new_note_parser.add_argument(
    'profile_url', type=str, default='')


# Specify the data necessary to update an existing help request.
# Only the priority and comments can be updated.
update_note_parser = reqparse.RequestParser()
# update_note_parser.add_argument(
#     'priority', type=int, default=PRIORITIES.index('normal'))
update_note_parser.add_argument(
    'note_content', type=str, default='')


# Specify the parameters for filtering and sorting help requests.
# See `filter_and_sort_notes` above.
query_parser = reqparse.RequestParser()
query_parser.add_argument(
    'query', type=str, default='')
query_parser.add_argument(
    'sort_by', type=str, choices=('title', 'date', 'author'), default='date')


# Define our help request resource.
class Note(Resource):

    # If a help request with the specified ID does not exist,
    # respond with a 404, otherwise respond with an HTML representation.
    def get(self, note_id):
        error_if_note_not_found(note_id)
        return make_response(
            render_note_as_html(
                data['notes'][note_id]), 200)

    # If a help request with the specified ID does not exist,
    # respond with a 404, otherwise update the help request and respond
    # with the updated HTML representation.
    def patch(self, note_id):
        error_if_note_not_found(note_id)
        note = data['notes'][note_id]
        update = update_note_parser.parse_args()
        # note['priority'] = update['priority']
        # note['note_content'] = note['note_content'].replace('\r\n', '<br>')
        if len(update['note_content'].strip()) > 0:
            note['note_content'] = update['note_content']
        with open('data.jsonld', 'w') as d:
            json.dump(data, d, ensure_ascii=False)
        return make_response(
            render_note_as_html(note), 200)


# Define a resource for getting a JSON representation of a help request.
class NoteAsJSON(Resource):

    # If a help request with the specified ID does not exist,
    # respond with a 404, otherwise respond with a JSON representation.
    def get(self, note_id):
        error_if_note_not_found(note_id)
        note = data['notes'][note_id]
        note['@context'] = data['@context']
        return note


# Define our help request list resource.
class NoteList(Resource):

    # Respond with an HTML representation of the help request list, after
    # applying any filtering and sorting parameters.
    def get(self):
        query = query_parser.parse_args()
        return make_response(
            render_note_list_as_html(
                filter_and_sort_notes(**query)), 200)

    # Add a new help request to the list, and respond with an HTML
    # representation of the updated list.
    def post(self):
        id = generate_id()
        note = new_note_parser.parse_args()
        note['author'] = {'name' : '{}'.format(note['author']),
                                 'profile_url' : '{}'.format(note['profile_url']),
                                 '@type': 'foaf:person'}
        note['date'] = "{:%Y-%m-%d}".format(datetime.now())
        # note['priority'] = PRIORITIES.index('normal')
        note["@type"] = "notebook:note"
        note["@id"] = "note/" + id
        del note['profile_url']
        data['notes'][id] = note
        with open('data.jsonld', 'w') as d:
            json.dump(data, d, ensure_ascii=False)
        return make_response(
            render_note_list_as_html(
                filter_and_sort_notes()), 201)


# Define a resource for getting a JSON representation of the help request list.
class NoteListAsJSON(Resource):
    def get(self):
        return data


# Assign URL paths to our resources.
app = Flask(__name__)
api = Api(app)
api.add_resource(NoteList, '/notebook')
api.add_resource(NoteListAsJSON, '/notebook.json')
api.add_resource(Note, '/note/<string:note_id>')
api.add_resource(NoteAsJSON, '/note/<string:note_id>.json')


# Redirect from the index to the list of help requests.
@app.route('/')
def index():
    return redirect(api.url_for(NoteList), code=303)


# Start the server.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5555, debug=True)
