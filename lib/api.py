import os
import xmlrpc.client
import configparser
import logging
from logging.config import dictConfig

from lib.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException


class API(object):
    dictConfig({
        'version': 1,
        'formatters': {
            'f': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
        'handlers': {
            'h': {'class': 'logging.StreamHandler', 'formatter': 'f', 'level': logging.DEBUG}
        },
        'root': {
            'handlers': ['h'],
            'level': logging.INFO,
        }
    })
    logger = logging.getLogger()
    _config_parser = configparser.ConfigParser()
    _config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'settings.ini'))

    _config_parser.read(_config_file)
    common = xmlrpc.client.ServerProxy('http://{}:{}/xmlrpc/2/common'.format(
        _config_parser.get('server', 'host'), _config_parser.get('server', 'port')
    ))
    orm = xmlrpc.client.ServerProxy('http://{}:{}/xmlrpc/2/object'.format(
        _config_parser.get('server', 'host'), _config_parser.get('server', 'port')
    ))
    uid = common.authenticate(
        _config_parser.get('server', 'database'),
        _config_parser.get('user', 'username'),
        _config_parser.get('user', 'password'),
        {}
    )

    def authenticate(self, username, password):
        return self.common.authenticate(
            self._config_parser.get('server', 'database'),
            username,
            password,
            {})

    def do(self, model=None, action=None, params=None, context={}):
        res = self.orm.execute_kw(
            self._config_parser.get('server', 'database'),
            self.uid,
            self._config_parser.get('user', 'password'),
            model, action, params, context
        )

        return res


    def send_sms(self, phone_number, message):
        # Specify your login credentials
        username = self._config_parser.get('africas_talking', 'username')
        apikey = self._config_parser.get('africas_talking', 'apikey')
        # Specify the numbers that you want to send to in a comma-separated list
        # Please ensure you include the country code (+254 for Kenya)
        to = phone_number
        # And of course we want our recipients to know what we really do
        # message = "I'm a lumberjack and it's ok, I sleep all night and I work all day"
        # Create a new instance of our awesome gateway class
        gateway = AfricasTalkingGateway(username, apikey)
        # *************************************************************************************
        #  NOTE: If connecting to the sandbox:
        #
        #  1. Use "sandbox" as the username
        #  2. Use the apiKey generated from your sandbox application
        #     https://account.africastalking.com/apps/sandbox/settings/key
        #  3. Add the "sandbox" flag to the constructor
        #
        #  gateway = AfricasTalkingGateway(username, apiKey, "sandbox");
        # **************************************************************************************
        # Any gateway errors will be captured by our custom Exception class below,
        # so wrap the call in a try-catch block
        try:
            # Thats it, hit send and we'll take care of the rest.

            results = gateway.sendMessage(to_=to, message_=message, from_=None)

            for recipient in results:
                # status is either "Success" or "error message"
                print('number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
                                                                    recipient['status'],
                                                                    recipient['messageId'],
                                                                    recipient['cost']))
        except AfricasTalkingGatewayException as e:
            return ('Encountered an error while sending: %s' % str(e))
            pass
