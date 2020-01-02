import time
import re
import os
import sys
from glob import glob
import concurrent.futures

from pdfminer.high_level import extract_text

if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

start = time.time()

REPORT_PATH = os.path.join(application_path, "report.csv")

report = ["Nom du fichier;Matricule nom;Matricule fichier;Valide"]

all_pdf_file_paths = glob(os.path.join(application_path, "*.pdf"))

if not all_pdf_file_paths:
    print("No pdf files to check.")
    sys.exit()

print(f"Will check {len(all_pdf_file_paths)} pdf files: \n")


def check_matricule(pdf_file_path):
    pdf_filename = os.path.basename(pdf_file_path)
    print(f"Checking {pdf_filename}...")
    matricule_match = re.match(r"(?P<filename_matricule>\d{7})", pdf_filename)

    if not matricule_match:
        return f"{pdf_filename};;;non"

    filename_matricule = matricule_match["filename_matricule"]

    text = extract_text(pdf_file_path)

    if filename_matricule.startswith("0"):
        pattern = r"Matricule : (?P<pdf_matricule>\d{6}\w{1})"
    else:
        pattern = r"Matricule : (?P<pdf_matricule>\d{7})"

    m = re.search(pattern, text)

    if m is not None:
        pdf_matricule = m["pdf_matricule"]

        if pdf_filename.startswith("0"):
            condition = pdf_matricule[:-1] == filename_matricule[1:]
        else:
            condition = pdf_matricule == filename_matricule

        if condition:
            return f"{pdf_filename};{filename_matricule};{pdf_matricule};oui"
        else:
            return f"{pdf_filename};{filename_matricule};{pdf_matricule};non"
    else:
        return f"{pdf_filename};{filename_matricule};;non"


executor = concurrent.futures.ProcessPoolExecutor()
results = executor.map(check_matricule, all_pdf_file_paths)
report += results
end = time.time()

print()
print(f"Executed in {round(end - start, 3)} seconds.\n")

print("Writing report...")

with open(REPORT_PATH, "w+") as file_:
    file_.write("\n".join(report))
