import argparse
import codecs
import json

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials


CLOUD_PLATFORM_LINK = 'https://www.googleapis.com/auth/cloud-platform'


class NLPClient(object):
    @property
    def service(self):
        credentials = GoogleCredentials.get_application_default()
        scoped_credentitals = credentials.create_scoped([CLOUD_PLATFORM_LINK])
        http = httplib2.Http()
        scoped_credentitals.authorize(http)
        return discovery.build('language', 'v1beta1', http=http)

    def _get_request_body(self, text, encoding):
        return {
            'document': {
                'type': 'PLAIN_TEXT',
                'content': text,
            },
            'encodingType': encoding,
        }

    def analyze_entity(self, text, encoding='UTF8'):
        body = self._get_request_body(text, encoding)
        request = self.service.documents().analyzeEntities(body=body)
        response = request.execute()
        return response

    def process(self, text, encoding='UTF8', output_file=None):
        response = self.analyze_entity(text, encoding)
        if output_file is None:
            print json.dumps(response, indent=2)
        else:
            with open(output_file, 'w') as output_handle:
                output_handle.write(json.dumps(response, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str)
    parser.add_argument('--encoding', type=str, default='UTF8')
    parser.add_argument('--output_file', type=str, default=None)
    args = parser.parse_args()
    client = NLPClient()
    with codecs.open(args.input_file, 'r', args.encoding) as input_handle:
        text = input_handle.read()
    client.process(text, args.encoding, args.output_file)
