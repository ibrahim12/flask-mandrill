import requests
import json

class Mandrill(object):
    app = None
    mandrill_api = None
    api_key = None

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.api_key = app.config['MANDRILL_API_KEY']
        self.app = app

    def _check_config(self):
        if not self.api_key:
            raise ValueError('No Mandrill API key has been configured')


    def send_email(self, **kwargs):
        """
        Sends an email using Mandrill's API. Returns a
        Requests :class:`Response` object.

        At a minimum kwargs must contain the keys to, from_email, and text.

        Everything passed as kwargs except for the keywords 'key', 'async',
        and 'ip_pool' will be sent as key-value pairs in the message object.

        Reference https://mandrillapp.com/api/docs/messages.JSON.html#method=send
        for all the available options.
        """
        self._check_config()

        data = {
            'async': kwargs.pop('async', False),
            'ip_pool': kwargs.pop('ip_pool', ''),
            'key': kwargs.pop('key', self.api_key),
            'message': kwargs,
        }
        data['message'].setdefault('from_email',
                                  self.app.config['MANDRILL_DEFAULT_FROM'])
        response = requests.post(self.messages_endpoint,
                                 data=json.dumps(data),
                                 headers={'Content-Type':'application/json'})
        response.raise_for_status()
        return response

    def send_template_email(self, **kwargs):
        """
        Sends a template email using Mandrill's API. Returns a
        Requests :class:`Response` object.

        At a minimum kwargs must contain the keys to, from_email, and text.

        Everything passed as kwargs except for the keywords 'key', 'async',
        and 'ip_pool' will be sent as key-value pairs in the message object.

        Reference https://mandrillapp.com/api/docs/messages.JSON.html#method=send-template
        for all the available options.
        """

        self._check_config()

        if 'template_name' not in kwargs:
            raise ValueError('Template Name is needed.')

        if 'template_content' not in kwargs:
            raise ValueError('Template Content is needed')

        data = {
            'async': kwargs.pop('async', False),
            'ip_pool': kwargs.pop('ip_pool', ''),
            'key': kwargs.pop('key', self.api_key),
            'template_nmae' : kwargs.pop('template_nmae', ''),
            'template_content' : kwargs.pop('template_content', ''),
            'message': kwargs,
        }
        data['message'].setdefault('from_email',
                                  self.app.config['MANDRILL_DEFAULT_FROM'])
        response = requests.post(self.messages_endpoint,
                                 data=json.dumps(data),
                                 headers={'Content-Type':'application/json'})
        response.raise_for_status()
        return response

    @property 
    def template_messages_endpoint(self):
        return 'https://mandrillapp.com/api/1.0/messages/send-template.json'

    @property
    def messages_endpoint(self):
        return 'https://mandrillapp.com/api/1.0/messages/send.json'
