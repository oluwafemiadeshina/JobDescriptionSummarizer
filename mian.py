#%% md
# # Job Description (JD) Summarizer
#%% md
# ## Install Required Libraries
#%%
!pip install nltk spacy sumy
!python -m spacy download en_core_web_sm
!pip uninstall -y spacy pydantic
#%%
!pip install spacy pydantic==1.10.13
!python -m spacy download en_core_web_sm

#%%
# Test spaCy import first
import spacy
print(f"spaCy version: {spacy.__version__}")

# Then test pydantic import
import pydantic
print(f"pydantic version: {pydantic.__version__}")

#%% md
# ## Import Libraries
#%%
import nltk
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from collections import Counter

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
#%%
import spacy
import pydantic
print("spaCy version:", spacy.__version__)
print("pydantic version:", pydantic.__version__)
#%% md
# ## Text Preprocessing
#%%
def preprocess_text(text):
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")

    # Tokenize and remove stopwords
    doc = nlp(text)
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]

    return tokens
#%% md
# ## Keyword Extraction
#%%
def extract_keywords(tokens, top_n=10):
    # Count word frequencies
    word_freq = Counter(tokens)

    # Get the most common words
    keywords = word_freq.most_common(top_n)

    return keywords
#%% md
# ## Summarization
#%%
def summarize_text(text, sentences_count=3):
    # Create a parser and tokenizer
    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    # Use LSA Summarizer
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)

    return ' '.join([str(sentence) for sentence in summary])
#%% md
# ## Putting It All Together
#%%
def summarize_job_description(jd_text):
    # Preprocess the text
    tokens = preprocess_text(jd_text)

    # Extract keywords
    keywords = extract_keywords(tokens)

    # Summarize the text
    summary = summarize_text(jd_text)

    return {
        "keywords": keywords,
        "summary": summary
    }
#%% md
# ## Example Usage
#%%
job_description = """
We are looking for a Python Developer to join our team. The ideal candidate should have experience with Python, Django, and Flask.
Responsibilities include developing and maintaining web applications, writing clean and scalable code, and collaborating with cross-functional teams.
The candidate should have a strong understanding of software development principles and be able to work in an agile environment.
Experience with REST APIs, databases, and version control systems like Git is a plus.
"""

result = summarize_job_description(job_description)
print("Keywords:", result["keywords"])
print("Summary:", result["summary"])