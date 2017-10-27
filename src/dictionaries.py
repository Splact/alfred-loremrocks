import os
import sys

from workflow import Workflow, web


def get_dictionaries():
    """Get available dictionaries from lorem.rocks"""
    url = 'https://api.lorem.rocks/dictionaries'
    params = dict(format='json')
    r = web.get(url, params)

    # throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    # Parse the JSON returned by pinboard and extract the dictionaries
    dictionaries = r.json()

    return dictionaries

def search_key_for_dictionary(dictionary):
    """Generate a string search key for a dictionary"""
    elements = []
    elements.append(dictionary['name'])
    return u' '.join(elements)

def get_thumbnail(dictionary):
    available_thumbs = ['ipsum', 'cadabra', 'macaroni']

    if dictionary in available_thumbs:
        return 'thumbs/{}.png'.format(dictionary)
    else:
        return 'thumbs/default.png'

def get_dummy_paragraph(dictionary):
    """Get dummy paragraph from lorem.rocks"""
    url = "https://api.lorem.rocks/dictionaries/{}/paragraph".format(dictionary)
    params = dict(format='json')
    r = web.get(url, params)

    # throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    result = r.json()

    return result['text']

def main(wf):
    # Get query from Alfred
    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    # Retrieve dictionaries from cache if available and no more than 1 hour old
    dictionaries = wf.cached_data('dictionaries', get_dictionaries, max_age=7200)

    # If script was passed a query, use it to filter dictionaries
    if query:
        dictionaries = wf.filter(query, dictionaries, key=search_key_for_dictionary)

    # Loop through the returned dictionaries and add an item for each to
    # the list of results for Alfred
    for dictionary in dictionaries:
        icon = get_thumbnail(dictionary['slug'])
        text = get_dummy_paragraph(dictionary['slug'])

        wf.add_item(title=dictionary['name'],
                    subtitle=dictionary['description'],
                    arg=text,
                    copytext=text,
                    largetext=text,
                    valid=True,
                    icon=icon)

    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))