import sys
from workflow import Workflow, ICON_WEB, web


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
        dictionary_slug = wf.args[0]
    else:
        dictionary_slug = 'macaroni'

    text = get_dummy_paragraph(dictionary_slug)

    print text

    # wf.add_item(text,
    #             arg=text,
    #             copytext=text,
    #             largetext=text,
    #             valid=True,
    #             icon=ICON_WEB)

    # # Send the results to Alfred as XML
    # wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
