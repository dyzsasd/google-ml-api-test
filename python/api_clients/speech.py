import argparse
import base64
from multiprocessing import Pool
import time

from google.cloud.credentials import get_credentials
from google.cloud.speech.v1beta1 import cloud_speech_pb2 as cloud_speech
from google.longrunning import operations_grpc_pb2
from grpc.beta import implementations
from tinytag import TinyTag


DEADLINE_SECS = 60
SPEECH_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'
AUDIO_ENCODING = 'FLAC'
SPEECH_API_HOST = 'speech.googleapis.com'
SPEECH_API_PORT = 443


class GoogleSpeechClientBase(object):
    @property
    def channel(self):
        ssl_channel = implementations.ssl_channel_credentials(None, None, None)
        creds = get_credentials().create_scoped([SPEECH_SCOPE])
        auth_header = (
            'Authorization',
            'Bearer ' + creds.get_access_token().access_token
        )
        auth_plugin = implementations.metadata_call_credentials(
            lambda _, cb: cb([auth_header], None),
            name='google_creds'
        )
        composite_channel = implementations.composite_channel_credentials(
            ssl_channel, auth_plugin)
        return implementations.secure_channel(
            SPEECH_API_HOST, SPEECH_API_PORT, composite_channel)

    @property
    def service(self):
        service = cloud_speech.beta_create_Speech_stub(self.channel)
        return service

    def _sample_rate(self, input_file):
        tags = TinyTag.get(input_file)
        return tags.samplerate

    def _process(self, input_file, language_code):
        raise NotImplemented("process method should be implemented.")


class GoogleSpeechSyncClient(GoogleSpeechClientBase):
    def _process(self, input_file, language_code):
        if not input_file.endswith('.flac'):
            raise RuntimeError('Only flac encoding file is supported.')
        audio_content = cloud_speech.RecognitionAudio(
            content=open(input_file, 'rb').read(),
        )
        sample_rate = self._sample_rate(input_file)
        response = self.service.SyncRecognize(
            cloud_speech.SyncRecognizeRequest(
                config=cloud_speech.RecognitionConfig(
                    encoding=AUDIO_ENCODING,
                    sample_rate=sample_rate,
                    language_code=language_code,
                ),
                audio=audio_content
                ),
            DEADLINE_SECS
        )
        return response

    def process(self, input_file, language_code='en-US', output_file=None):
        response = self._process(input_file, language_code)
        if output_file is None:
            for result in response.results:
                print('Result:')
                for alternative in result.alternatives:
                    print(u'  ({}): {}'.format(
                        alternative.confidence, alternative.transcript))
        else:
            with open(output_file, 'w') as output_handle:
                for result in response.results:
                    for alternative in result.alternatives:
                        output_handle.write(u'  ({}): {}'.format(
                            alternative.confidence, alternative.transcript))
                        output_handle.write('\n')

class GoogleSpeechAsyncClient(GoogleSpeechClientBase):
    pool = Pool()

    def _process(self, input_file, language_code):
        if not input_file.endswith('.flac'):
            raise RuntimeError('Only flac encoding file is supported.')
        audio_content = cloud_speech.RecognitionAudio(
            content=open(input_file, 'rb').read(),
        )
        sample_rate = self._sample_rate(input_file)
        operation = self.service.AsyncRecognize(
            cloud_speech.AsyncRecognizeRequest(
                config=cloud_speech.RecognitionConfig(
                    encoding=AUDIO_ENCODING,
                    sample_rate=sample_rate,
                    language_code=language_code,
                ),
                audio=audio_content
                ),
            DEADLINE_SECS
        )
        return operation


    def process(self, input_file, language_code='en-US', output_file=None):
        operation = self._process(input_file, language_code)
        long_service = operations_grpc_pb2.beta_create_Operation_stub(
            self.channel)
        name = operation_handle.name
        while True:
            print 'Waiting for result ...'
            time.sleep(1)
            operation = service.GetOperation(
                operations_grpc_pb2.GetOperationRequest(name=name),
                DEADLINE_SECS
            )
            if operation.done:
                break
        response = cloud_speech.AsyncRecognizeResponse()
        operation.response.Unpack(response)
        if output_file is None:
            for result in response.results:
                print('Result:')
                for alternative in result.alternatives:
                    print(u'  ({}): {}'.format(
                        alternative.confidence, alternative.transcript))
        else:
            with open(output_file, 'w') as output_handle:
                for result in response.results:
                    for alternative in result.alternatives:
                        output_handle.write(u'  ({}): {}'.format(
                            alternative.confidence, alternative.transcript))
                        output_handle.write('\n')


def process(input_file, language_code, output_file):
    tags = TinyTag.get(input_file)
    if tags.duration > 60:
        client = GoogleSpeechAsyncClient()
    else:
        client = GoogleSpeechSyncClient()
    client.process(input_file, language_code, output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str)
    parser.add_argument('--language_code', type=str, default='en-US')
    parser.add_argument('--output_file', type=str, default=None)
    args = parser.parse_args()

    process(args.input_file, args.language_code, args.output_file)
