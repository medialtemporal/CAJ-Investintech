from PyPDF2 import PdfReader
from PyPDF2 import errors
import csv
import os

# Keywords
words = ['ai', 'chatgpt', 'llm', 'artificial intelligence', 'language model', 'gpt', 'generative ai', 'midjourney',
         'bard', 'dall-e']

# Get faculties
folder_name = 'syllabi'
faculties = os.listdir(os.path.join(os.getcwd(), folder_name))
faculties.remove(".DS_Store")

# Get departments inside the faculty folder (list)
departments = []
for faculty in faculties:
    faculty_departments = os.listdir(os.path.join(os.getcwd(), folder_name, faculty))
    for department in faculty_departments:
        if department != ".DS_Store":
            departments.append(f'{faculty}/{department}')

# Get file names for all syllabi within department folder (list)
syllabi = []
for department in departments:
    department_syllabi = os.listdir(os.path.join(os.getcwd(), folder_name, department))
    for syllabus in department_syllabi:
        if syllabus != ".DS_Store":
            syllabi.append(f'{department}/{syllabus}')


def main():
    for syllabus_path in syllabi:
        try:
            text = scan_syllabus(os.path.join(os.getcwd(), folder_name, syllabus_path))
            keywords = find_keywords(text)
            write_to_csv(syllabus_path, keywords, len(text))
        except errors.DependencyError:
            print('Dependency Error!! (1)\n', syllabus_path)
        except errors.PdfReadError:
            print('This PDF is not able to be read: ', syllabus_path)


def scan_syllabus(syllabus_text):
    text = ""
    reader = PdfReader(syllabus_text)
    for page in reader.pages:
        try:
            text = text + page.extract_text().strip()
        except errors.DependencyError:
            print('Dependency Error 2\n', syllabus_text)
    return text


def find_keywords(text):
    keywords = []
    text = text.lower()
    for word in words:
        if " " + word + " " in text:  # to avoid, for e.g., "said"
            keywords.append(word)
        elif " " + word + "." in text:
            keywords.append(word)
        elif " " + word + "," in text:
            keywords.append(word)
    return keywords


def write_to_csv(syllabus_path, keywords, num_chars):
    with open('ai_data.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([syllabus_path, keywords, num_chars])
    print(f'Wrote {syllabus_path} to CSV')


main()
