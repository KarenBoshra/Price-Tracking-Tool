import google.generativeai as genai
import textwrap

def generate_content(full_text):
    GOOGLE_API_KEY = "AIzaSyDoMvWwtm6H2K61RWoRHJCuVKRBNKxDxxg"
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    def to_markdown(text):
        text = text.replace('•', '  *')
        return textwrap.indent(text, '> ', predicate=lambda _: True)

    response = model.generate_content(full_text + "\n What is the product name, what is the product price as a number, and what is the currency? please separate each answer with a *** and put the result between qoutation")
    return to_markdown(response.text)