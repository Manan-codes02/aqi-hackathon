# Official CPCB AQI categories and standard health advisories

from deep_translator import GoogleTranslator

def translate_advisory(text, target_language='hi'):
    """
    Translate advisory text into a regional language.
    Common codes: hi=Hindi, ta=Tamil, kn=Kannada, bn=Bengali, te=Telugu, mr=Marathi
    """
    try:
        translated = GoogleTranslator(source='en', target=target_language).translate(text)
        return translated
    except Exception as e:
        return f"[Translation failed: {e}]"
    
def get_multilingual_advisory(aqi_value, languages=['hi', 'ta', 'kn']):
    """
    Given an AQI value, return the advisory in English plus multiple regional languages.
    languages: list of language codes, e.g. hi=Hindi, ta=Tamil, kn=Kannada, bn=Bengali, te=Telugu, mr=Marathi
    """
    base = get_advisory(aqi_value)
    translations = {"en": base["advisory"]}

    for lang in languages:
        translations[lang] = translate_advisory(base["advisory"], target_language=lang)

    return {
        "aqi": base["aqi"],
        "category": base["category"],
        "color": base["color"],
        "messages": translations
    }

AQI_CATEGORIES = [
    {
        "max": 50,
        "category": "Good",
        "color": "green",
        "advisory": "Air quality is satisfactory. Enjoy outdoor activities as usual."
    },
    {
        "max": 100,
        "category": "Satisfactory",
        "color": "light green",
        "advisory": "Air quality is acceptable. Sensitive individuals may experience minor discomfort."
    },
    {
        "max": 200,
        "category": "Moderate",
        "color": "yellow",
        "advisory": "People with asthma, lung or heart disease, children and older adults should reduce prolonged outdoor exertion."
    },
    {
        "max": 300,
        "category": "Poor",
        "color": "orange",
        "advisory": "Everyone may experience breathing discomfort on prolonged exposure. Avoid outdoor activity if possible."
    },
    {
        "max": 400,
        "category": "Very Poor",
        "color": "red",
        "advisory": "Breathing discomfort on prolonged exposure for most people. Avoid outdoor exercise; keep windows closed."
    },
    {
        "max": float('inf'),
        "category": "Severe",
        "color": "maroon",
        "advisory": "Serious health risk for everyone. Avoid all outdoor activity. Use N95 masks if you must go outside."
    }
]

def get_advisory(aqi_value):
    """
    Given an AQI value, return its category, color, and health advisory message.
    """
    for level in AQI_CATEGORIES:
        if aqi_value <= level["max"]:
            return {
                "aqi": aqi_value,
                "category": level["category"],
                "color": level["color"],
                "advisory": level["advisory"]
            }

# Test it
if __name__ == "__main__":
    test_values = [35, 88, 150, 250, 350, 450]
    for val in test_values:
        result = get_advisory(val)
        print(f"AQI {val}: {result['category']} — {result['advisory']}")

    # Test multilingual advisory
    print("\n--- Multilingual advisory test (AQI 250) ---")
    result = get_multilingual_advisory(250, languages=['hi', 'ta', 'kn'])

    with open('multilingual_test_output.txt', 'w', encoding='utf-8') as f:
        f.write(f"AQI: {result['aqi']} ({result['category']})\n\n")
        for lang, msg in result['messages'].items():
            f.write(f"[{lang}]: {msg}\n\n")

    print("Saved to multilingual_test_output.txt — open in VS Code to view properly")