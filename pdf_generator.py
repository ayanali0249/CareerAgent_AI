from fpdf import FPDF
import tempfile

class PDFReport:
    def __init__(self, name="Candidate", job_role="Not Specified"):
        self.name = name
        self.job_role = job_role
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, "AI Resume Analysis Report", ln=True, align="C")
        self.pdf.set_font("Arial", "", 12)
        self.pdf.ln(10)
        self.pdf.cell(0, 10, f"Candidate Name: {self.name}", ln=True)
        self.pdf.cell(0, 10, f"Target Job Role: {self.job_role}", ln=True)
        self.pdf.ln(5)

    def add_section(self, title, items, color=(230, 230, 230)):
        self.pdf.set_fill_color(*color)
        self.pdf.set_font("Arial", "B", 13)
        self.pdf.cell(0, 10, title, ln=True, fill=True)
        self.pdf.set_font("Arial", "", 12)
        if items:
            for item in items:
                self.pdf.cell(0, 8, f"- {item}", ln=True)
        else:
            self.pdf.cell(0, 8, "None", ln=True)
        self.pdf.ln(5)

    def generate(self, extracted_skills, matched_skills, missing_skills, score):
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, f"Match Score: {score:.2f}%", ln=True)
        self.pdf.ln(5)

        self.add_section("Extracted Skills", extracted_skills)
        self.add_section("Matched Skills", matched_skills, color=(200, 255, 200))
        self.add_section("Missing Skills", missing_skills, color=(255, 200, 200))

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        self.pdf.output(temp_file.name)
        return temp_file.name
