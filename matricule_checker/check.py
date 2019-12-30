import re
from os import path
from glob import glob

from pdfminer.high_level import extract_text

report = ["Nom du fichier,Matricule nom, Matricule fichier,Valide"]

for pdf_filename in glob("*.pdf"):
    matricule_match = re.match(r"0(?P<filename_matricule>\d{6})", pdf_filename)

    if not matricule_match:
        report.append(f"{pdf_filename},,,non")
        break

    filename_matricule = matricule_match["filename_matricule"]

    text = extract_text(pdf_filename)

    m = re.search(r"Matricule : (?P<pdf_matricule>\d{6}\w{1})", text)

    if m is not None:
        pdf_matricule = m["pdf_matricule"]

        if pdf_filename.startswith("0"):
            condition = pdf_matricule[:-1] == filename_matricule
        else:
            condition = pdf_matricule == filename_matricule

        if condition:
            report.append(f"{pdf_filename},{filename_matricule},{pdf_matricule},oui")
        else:
            report.append(f"{pdf_filename},{filename_matricule},{pdf_matricule},non")
    else:
        break

if path.exists("report.csv"):
    lecture_mode = "w"
else:
    lecture_mode = "x"

with open("report.csv", lecture_mode) as file_:
    file_.write("\n".join(report))
