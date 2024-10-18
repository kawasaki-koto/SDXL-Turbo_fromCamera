from deep_translator import GoogleTranslator

def jap_to_eng(text):
    text = GoogleTranslator(source='ja', target='en').translate(text)
    print(text)
    return text