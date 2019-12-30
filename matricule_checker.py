import re
import os
import sys
from glob import glob

from pdfminer.high_level import extract_text

if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

REPORT_PATH = os.path.join(application_path, "report.csv")

report = ["Nom du fichier;Matricule nom;Matricule fichier;Valide"]

all_pdf_file_paths = glob(os.path.join(application_path, "*.pdf"))

if not all_pdf_file_paths:
    print("No pdf files to check.")

for pdf_file_path in all_pdf_file_paths:
    pdf_filename = os.path.basename(pdf_file_path)
    print(f"Checking {pdf_filename}...")
    matricule_match = re.match(r"0(?P<filename_matricule>\d{6})", pdf_filename)

    if not matricule_match:
        report.append(f"{pdf_filename};;;non")
        break

    filename_matricule = matricule_match["filename_matricule"]

    text = extract_text(pdf_file_path)

    m = re.search(r"Matricule : (?P<pdf_matricule>\d{6}\w{1})", text)

    if m is not None:
        pdf_matricule = m["pdf_matricule"]

        if pdf_filename.startswith("0"):
            condition = pdf_matricule[:-1] == filename_matricule
        else:
            condition = pdf_matricule == filename_matricule

        if condition:
            report.append(f"{pdf_filename};{filename_matricule};{pdf_matricule};oui")
        else:
            report.append(f"{pdf_filename};{filename_matricule};{pdf_matricule};non")
    else:
        break

if os.path.exists(REPORT_PATH):
    lecture_mode = "w"
else:
    lecture_mode = "x"

with open(REPORT_PATH, lecture_mode) as file_:
    file_.write("\n".join(report))
