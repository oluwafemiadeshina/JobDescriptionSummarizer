#%% md
# # Job Description (JD) Summarizer
#%% md
# ## Install Required Libraries
#%%
# Install required libraries

!pip install nltk spacy sumy rake-nltk
!python -m spacy download en_core_web_sm
!pip uninstall -y spacy pydantic
#%%
!pip install spacy pydantic==1.10.13
!python -m spacy download en_core_web_sm

#%%
# Import libraries
import nltk
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from collections import Counter
from rake_nltk import Rake
import re
print(f"spaCy version: {spacy.__version__}")

#%%
# Then test pydantic import
import pydantic
print(f"pydantic version: {pydantic.__version__}")
#%%
# Load the spaCy model
nlp = spacy.load('en_core_web_sm')
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
# Text preprocessing
def preprocess_text(text):
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")

    # Tokenize, remove stopwords, and lemmatize
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]

    return tokens
#%% md
# ## Keyword Extraction
#%%
# Keyword extraction using RAKE
def extract_keywords(text, top_n=10):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    ranked_phrases = rake.get_ranked_phrases()[:top_n]
    return ranked_phrases

#%%



def extract_entities(text):
    doc = nlp(text)
    entities = {
        "ORG": [],  # Organizations (e.g., Spencer Academies Trust)
        "GPE": [],  # Geographical locations (e.g., Nottingham, United Kingdom)
        "DATE": [],  # Dates (e.g., 9th June 2025)
        "MONEY": [],  # Monetary values (e.g., £425 per week)
    }
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    return entities
#%% md
# ## Summarization
#%%
def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    # Adjust sentence count based on text length
    sentences_count = max(2, min(5, len(text.split(".")) // 10))
    summary = summarizer(parser.document, sentences_count)
    return ' '.join([str(sentence) for sentence in summary])
#%% md
# ## Putting It All Together
#%%
# Putting it all together
def summarize_job_description(jd_text):
    # Preprocess the text
    tokens = preprocess_text(jd_text)

    # Extract keywords
    keywords = extract_keywords(jd_text)

    # Extract keywords
    entities = extract_entities(jd_text)

    # Summarize the text
    summary = summarize_text(jd_text)

    return {
        "keywords": keywords,
        "entities": entities,
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
print("Entities:", result["entities"])
print("Summary:", result["summary"])
#%%
job_description = """
UniHub UniHub Dashboard James Notifications0 Spencer Academies Trust Nottingham, East Midlands, United Kingdom 1 job Teaching Intern United Kingdom £425 per week for full attendance & participation Full-time, Temporary Teaching Internship Programme takes place in Spencer Academies Trust schools across Nottinghamshire and Derbyshire. You will gain an insight into the life of a teacher and participate in training sessions. Applications close on 9 Feb 2025 Job details Teaching Internship Programme takes place in Spencer Academies Trust schools across Nottinghamshire and Derbyshire. You will gain an insight into the life of a teacher and participate in training sessions. Subjects: Maths Physics Chemistry Computing MFL. On the programme you will gain in-school experience, learn about the life of a teacher, support pupils in the classroom, shadow experienced teachers, discover the routes into teaching and participate in teaching. Eligibility You must be an undergraduate or master’s student, studying in a UK university, who is considering a career in teaching. The programme lasts for 3 weeks, 9th to 27th June 2025. You'll receive personalised post-programme support to assist you with getting into a career in teaching. More info Job types Graduate job Internship Expected commencement 9th June 2024 Posted 7 Nov 2024 Applications close on 9 Feb 2025 More jobs Independent Advisory Group – Volunteer – Derbyshire Derbyshire Constabulary Derbyshire, England, United Kingdom Youth Work Volunteer Safe and Sound Group First Floor East Mill, Darley Abbey Mills, Darley Abbey., Derby, Derbyshire, England, DE22 1DZ, United Kingdom Awareness Volunteer Safe and Sound Group First Floor East Mill, Darley Abbey Mills, Darley Abbey, Derby, Derbyshire, England, DE22 1DZ, United Kingdom
"""

result = summarize_job_description(job_description)
print("Keywords:", result["keywords"])
print("Entities:", result["entities"])
print("Summary:", result["summary"])
#%%
job_description = """
Researcher The Lullaby Trust Remote £10,000 per year Part-time (2 days per week (can be worked flexibly).) Contract (Fixed term for 6 months) Actively Interviewing This is a preview of your upcoming ad, it's not yet visible to candidates. The ad will be posted on 04 February 2025. Quick Apply Save Job description The main function of this role will be: Review The Lullaby Trust’s current Evidence Base. Create a revised Evidence Base including the production of plain language versions for each topic. Work with our designer to create final accessible PDF copies for each topic. Develop a standard operating procedure for updating the Evidence Base in future. Job Description Review The Lullaby Trust’s current Evidence Base. The Lullaby Trust’s guidance is constantly evolving as new evidence emerges on preventing unexpected infant deaths. However, much of our guidance, such as our Back to Sleep messaging, is based on an established and agreed body of evidence. The post holder will be required to undertake a narrative systematic review of the literature to create an updated Evidence Base for each aspect of The Lullaby Trust’s guidance, referencing established research and any relevant updated evidence. Ideally, papers would need to be readily available via open access to assist The Lullaby Trust staff with supporting research enquiries. It is important to note that whilst some of our guidance is based on direct evidence, some is indirect i.e. advising against using certain products due to association with other evidence-based guidance; therefore, the post holder should have a sound understanding of SIDS and unexpected infant death research to be able to demonstrate this link concisely. Current topics covered by our guidance and evidence include: Sleeping position Clear cot Room temperature Bedding Twins and multiples Smoking Alcohol and drug use Breastfeeding Airways Co-sleeping/bedsharing Products; slings, dummies, baby monitors Car seats Infection and immunisations Premature babies Poor antenatal care Swaddling Young parents Normal baby sleep Impact of deprivation Create a revised Evidence Base including the production of plain language versions for each topic. The Lullaby Trust’s current Evidence Base is an extensive document. This project aims to make the Evidence Base more accessible and easier to update. We envisage that each topic currently covered in the Evidence Base will have a fully referenced version and a plain language version to enable them to be understood and used by a variety of service users, including health professionals and parents or carers. On completion, the Evidence Base and its derivatives will remain the sole property of The Lullaby Trust, however the post holder will be credited and there is scope for the post holder to publish an academic paper based on the project. Work with our designer to create final accessible PDF copies for each topic. The post holder will need to support in the design of easily accessible PDF versions of the Evidence Base, including any relevant infographics and links to referenced research. Each document will need to align with the guidance available to service users via our website and in other published resources. It may be possible that the review provides insights into potential changes to the current guidance available and, where this is indicated, the post holder will work with our Scientific Advisory Group to provide the evidence for those discussions. Develop a standard operating procedure for updating the Evidence Base in future. As a dynamic organisation that adapts our guidance to the most up-to-date research. Our current process involves our Scientific Advisory Group assessing new research and, if appropriate, amending our guidance or adding research to an established research library. However, the format of the current Evidence Base document creates a challenge in adding new references and evidence. The revised Evidence Base documents created by this project will need to be easily edited and updated. The post holder will be required to develop a standard operating procedure for updating the documents as part of our current Scientific Advisory Group processes. Person Specification Essential: A good understanding of the research around SIDS and unexpected infant death. Experience of literature reviews, systematic reviews, critical appraisal, and evidence synthesis. Good written skills, including the ability to write in an accessible way. Attachment to a Further Education Institution. Access to own laptop/computer and necessary software. Ability to organise own time to meet agreed project milestones. To Apply: Please send a CV and a proposed project plan, including proposed methodology and a Gantt chart with intended timescales and milestones. References may be requested from successful applicants. Post holder must be available for regular online meetings to discuss progress and at least one in-person meeting with our Scientific Advisory Group in the London office. Application Instructions To Apply: Please send a CV and a proposed project plan, including proposed methodology and a Gantt chart with intended timescales and milestones. References may be requested from successful applicants.
"""

result = summarize_job_description(job_description)
print("Keywords:", result["keywords"])
print("Entities:", result["entities"])
print("Summary:", result["summary"])
#%%
def format_summary(job_title, location, salary, responsibilities, eligibility, benefits):
    summary = f"""
**Job Title:** {job_title}
**Location:** {location}
**Salary:** {salary}

**Responsibilities:**
- {responsibilities[0]}
- {responsibilities[1]}
- {responsibilities[2]}

**Eligibility:**
- {eligibility}

**Benefits:**
- {benefits}
"""
    return summary
#%%
import re

def clean_text(text):
    # Remove irrelevant text (e.g., "UniHub UniHub Dashboard James Notifications0")
    text = re.sub(r"UniHub.*?Notifications\d+", "", text)
    # Remove extra spaces and newlines
    text = re.sub(r"\s+", " ", text).strip()
    return text
#%%
def main():
    print("Job Description Summarizer")
    jd_text = input("Paste the job description here:\n")
    result = summarize_job_description(jd_text)
    print("\nKeywords:", result["keywords"])
    print("\nSummary:", result["summary"])

if __name__ == "__main__":
    main()
#%%
def save_to_file(result, filename="summary.txt"):
    with open(filename, "w") as f:
        f.write("Keywords:\n")
        f.write("\n".join(result["keywords"]) + "\n\n")
        f.write("Summary:\n")
        f.write(result["summary"])
    print(f"Summary saved to {filename}")
#%% md
# ## Support for Multiple Job Descriptions
#%%
def process_multiple_jds(jd_list):
    summaries = []
    for jd in jd_list:
        result = summarize_job_description(jd)
        summaries.append(result)
    return summaries
#%%
job_description = """
UniHub UniHub Dashboard James Notifications0 Spencer Academies Trust Nottingham, East Midlands, United Kingdom 1 job Teaching Intern United Kingdom £425 per week for full attendance & participation Full-time, Temporary Teaching Internship Programme takes place in Spencer Academies Trust schools across Nottinghamshire and Derbyshire. You will gain an insight into the life of a teacher and participate in training sessions. Applications close on 9 Feb 2025 Job details Teaching Internship Programme takes place in Spencer Academies Trust schools across Nottinghamshire and Derbyshire. You will gain an insight into the life of a teacher and participate in training sessions. Subjects: Maths Physics Chemistry Computing MFL. On the programme you will gain in-school experience, learn about the life of a teacher, support pupils in the classroom, shadow experienced teachers, discover the routes into teaching and participate in teaching. Eligibility You must be an undergraduate or master’s student, studying in a UK university, who is considering a career in teaching. The programme lasts for 3 weeks, 9th to 27th June 2025. You'll receive personalised post-programme support to assist you with getting into a career in teaching. More info Job types Graduate job Internship Expected commencement 9th June 2024 Posted 7 Nov 2024 Applications close on 9 Feb 2025 More jobs Independent Advisory Group – Volunteer – Derbyshire Derbyshire Constabulary Derbyshire, England, United Kingdom Youth Work Volunteer Safe and Sound Group First Floor East Mill, Darley Abbey Mills, Darley Abbey., Derby, Derbyshire, England, DE22 1DZ, United Kingdom Awareness Volunteer Safe and Sound Group First Floor East Mill, Darley Abbey Mills, Darley Abbey, Derby, Derbyshire, England, DE22 1DZ, United Kingdom
"""

result = summarize_job_description(job_description)
print("Keywords:", result["keywords"])
print("Summary:", result["summary"])