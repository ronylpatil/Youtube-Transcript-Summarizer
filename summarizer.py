from transformers import pipeline
import pywhisper, pytube
from nltk import tokenize
import re


def youtubeSummarizer(link) -> 'Transcript Summary' :
    model = pywhisper.load_model("base", download_root = 'model/')

    pytube.YouTube(link).streams.filter(only_audio = True).get_by_itag(139).download(output_path = 'audioFile/', filename = 'xyz.mp3')

    transcript = model.transcribe("audioFile/xyz.mp3", fp16=False)

    tokanized_sentences = tokenize.sent_tokenize(transcript['text'])

    total_sentences = len(tokenize.sent_tokenize(transcript['text']))

    group_sentences = []
    temp = ''
    for i in range(total_sentences):
        if len((temp + tokanized_sentences[i]).split(' ')) < 400:
            temp += tokanized_sentences[i] + ' '
        else :
            group_sentences.append(temp)
            temp = ''

        if i == total_sentences - 1 :
            group_sentences.append(temp)
            temp = ''

    summarizer_pipeline = pipeline(task = 'summarization', model = 'sshleifer/distilbart-cnn-12-6')

    final_summary = []
    for sentence in group_sentences:
        final_summary.append(summarizer_pipeline(sentence.strip(), do_sample = False)[0]['summary_text'])

    summary = re.sub(r'\s([?.!"](?:\s|$))', r'\1', ' '.join(' '.join(final_summary).split()))

    with open('summary.txt', 'w+') as f :
        f.write(summary)

    return summary


