from project import wiki, time, openWeb
import wikipedia
import datetime
import warnings
# Filter out DeprecationWarnings related to 'aifc' and 'audioop'
warnings.filterwarnings("ignore", category=DeprecationWarning, module='speech_recognition')
import speech_recognition
def test_time():
    assert time("Jarvis what's the time") == f'Its {datetime.datetime.now().strftime("%H %M-%p")}'
def test_wiki():
    assert wiki("what do you know about Pakistan") == wikipedia.summary('Pakistan',sentences = 2)
def test_openWeb():
    assert openWeb('Jarvis open Youtube') == ''
