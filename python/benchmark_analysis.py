import codecs
from os import listdir
from os.path import isfile, join
import re

root='/Users/s.zhang/workspace/dailymotion/google-ml-api'

recognition_results_path = "%s/data/benchmark/de-DE/text/" % root
reference_path = "%s/data/benchmark/de-DE/transcript/" % root

results={}

print "loading results ..."
for file_name in listdir(recognition_results_path):
    if isfile(join(recognition_results_path, file_name)):
        abs_file_path = join(recognition_results_path, file_name)
        with codecs.open(abs_file_path, 'r', 'utf8') as input_handle:
            sentences = []
            for result_text in input_handle:
                result_text = result_text[:-1]
                result = {}
                accuracy = re.findall(r'\(([\d\.]+)\).*', result_text)
                items = result_text.split(': ')
                if not accuracy or len(items) < 2:
                    results[file_name] = None
                    break
                result['accuracy'] = float(accuracy[0])
                result['text'] = items[1].strip()
                result['tokens'] = items[1].strip().split(' ')
                sentences.append(result)
            base_name=file_name.split('.')[0]
            results[base_name] = sentences

references = {}
print "loading reference ..."
for file_name in listdir(reference_path):
    if isfile(join(reference_path, file_name)):
        abs_file_path = join(reference_path, file_name)
        with codecs.open(abs_file_path, 'r', 'utf8') as input_handle:
            sentences = []
            for reference_text in re.split(r'[,\.\n]', input_handle.read()):
                reference = {}
                if not reference_text:
                    break
                reference['text'] = reference_text.strip()
                reference['tokens'] = reference_text.strip().split(' ')
                sentences.append(reference)
            references[file_name] = sentences


def get_word_count(tokens):
    word_count = {}
    for token in tokens:
        if token not in word_count:
            word_count[token] = 0
        word_count[token] += 1
    return word_count

def compare_tokens(left_tokens, right_tokens):
    if not left_tokens or not right_tokens:
        return 0
    left_header = left_tokens[0]
    right_header = right_tokens[0]
    if left_header == right_header:
        return 1 + compare_tokens(left_tokens[1:], right_tokens[1:])
    else:
        return max(
            compare_tokens(left_tokens[1:], right_tokens),
            compare_tokens(left_tokens, right_tokens[1:])
        )


comparaison = {}

for key, sentences in results.items():
    if key not in references:
        continue
    reference_sentences = references[key]
    result_tokens = [
        token in sentence
        for sentence in sentences
        for token in sentence['tokens']
    ]
    reference_tokens = [
        token in sentence
        for sentence in reference_sentences
        for token in sentence['tokens']
    ]
    matched_tokens_count = compare_tokens(result_tokens, reference_tokens)
    comparaison[key] = {
        'matched_token_count': matched_tokens_count,
        'reference_tokens_count' : len(reference_tokens),
        'success_rate': matched_tokens_count * 1.0 / len(reference_tokens),
    }

stats = {}
for key, comp in comparaison.items():
    token_count = comp['reference_tokens_count']
    if token_count not in stats:
        stats[token_count] = {
            'count': 0,
            'sum': 0.0,
        }
    stats[token_count]['count'] += 1
    stats[token_count]['sum'] += comp['success_rate']

for key, stat in stats.items():
    stat['avg'] = stat['sum'] / stat['count']
