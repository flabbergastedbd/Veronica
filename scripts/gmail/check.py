from __future__ import print_function
import httplib2
import os
import tornado.template

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a table of unread mails
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    response = service.users().messages().list(userId='me', labelIds=['UNREAD', 'INBOX']).execute()

    # result1 = service.users().labels().list(userId='me').execute()
    # for label in result1['labels']:
    #     print("%s - %s" % (label['id'], label['name']))

    m_ids = []
    messages = []
    if 'messages' in response: m_ids.extend(response['messages'])
    for m in m_ids:
        result = service.users().messages().get(userId='me', id=m['id'], format="metadata", metadataHeaders='From').execute()
        messages.append(result)
    print(tornado.template.Template(LOG_TEMPLATE).generate(messages=messages))
    return(0)


LOG_TEMPLATE = """<table class="table table-bordered">
  {% for m in messages %}
    <tr {% if 'CATEGORY_SOCIAL' in m['labelIds'] %}
       class="table-info"
    {% elif 'CATEGORY_UPDATES' in m['labelIds'] %}
       class="table-warning"
    {% elif 'CATEGORY_PROMOTIONS' in m['labelIds'] %}
       class="table-success"
    {% end %}>
      <td>
        <blockquote class="blockquote">
            <p class="m-b-0">{% raw m['snippet'][0:min(len(m['snippet']), 50)] %}</p>
            {% if len(m['payload']['headers']) > 0 %}
                <footer class="blockquote-footer">{% raw m['payload']['headers'][0]['value'] %}</footer>
            {% end %}
        </blockquote>
      </td>
    </tr>
  {% end %}
</table>"""

if __name__ == '__main__':
    main()
