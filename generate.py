import os
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from dotenv import load_dotenv
from datetime import datetime, timedelta
from maksu import viitenumero  # Import your reference number generation library


# Load .env file
load_dotenv()

IBAN = os.getenv("IBAN")
BIC = os.getenv("BIC")
BANK_NAME = os.getenv("BANK_NAME")
EMAIL = os.getenv("EMAIL")
ADDRESS = os.getenv("ADDRESS")
YNUMBER = os.getenv("YNUMBER")
PHONE = os.getenv("PHONE")


def load_customers_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        return [row for row in reader if len(row) == 2]  # Only email and name


def load_bills_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        return [row for row in reader if len(row) == 3]


def calculate_due_date(days_to_pay):
    """Returns a due date by adding 'days_to_pay' to today's date."""
    today = datetime.today()
    due_date = today + timedelta(days=int(days_to_pay))
    return due_date.strftime("%d.%m.%Y")  # Format: day.month.year


def load_generated_references(file_path="generated_references.txt"):
    """Load the last generated reference number to ensure uniqueness."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return int(f.read().strip())  # Return as an integer
    return 100  # Start from 101 if no file exists


def save_generated_reference(reference_number, file_path="generated_references.txt"):
    """Save the new generated reference number to the file."""
    with open(file_path, "w") as f:
        f.write(str(reference_number))


def generate_pdf(
    name, email, ref_number, bill_type, amount, due_days, output_dir, generation_date
):
    safe_name = name.replace(" ", "_").lower()
    filename = os.path.join(
        output_dir, f"Tusebo_lasku_{safe_name}_{bill_type}_{generation_date}.pdf"
    )
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Load env details
    org_email = os.getenv("EMAIL")
    phone = os.getenv("PHONE")
    address = os.getenv("ADDRESS")
    y_number = os.getenv("YNUMBER")

    # Draw header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 50, "Turun Seudun Bofferoijat ry")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 65, f"Y-tunnus: {y_number}")
    c.drawString(40, height - 80, f"{address}")
    c.drawString(40, height - 95, f"Puhelin: {phone}")
    c.drawString(40, height - 110, f"Sähköposti: {org_email}")

    # Invoice meta
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, height - 50, "LASKU")
    c.setFont("Helvetica", 10)
    c.drawString(400, height - 65, f"Laskunumero: {ref_number}")
    c.drawString(400, height - 80, f"Päiväys: {generation_date}")

    # Customer info
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, height - 150, "Vastaanottaja:")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 165, f"{name}")
    c.drawString(40, height - 180, f"{email}")

    # Table headers
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, height - 220, "Määrä")
    c.drawString(100, height - 220, "Kuvaus")
    c.drawString(400, height - 220, "Summa")

    # Table row
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 240, "1 kpl")
    c.drawString(100, height - 240, f"{bill_type.capitalize()}")
    c.drawString(400, height - 240, f"{amount} €")

    # Subtotal & total
    c.setFont("Helvetica-Bold", 10)
    c.drawString(320, height - 300, "Välisumma:")
    c.drawString(420, height - 300, f"{amount} €")
    c.drawString(320, height - 320, "ALV:")
    c.drawString(420, height - 320, "-")
    c.drawString(320, height - 340, "Toimituskulut:")
    c.drawString(420, height - 340, "-")

    # Total due
    c.setFont("Helvetica-Bold", 10)
    c.drawString(320, height - 370, "Maksettavaa Yhteensä:")
    c.drawString(450, height - 370, f"{amount} €")

    # Due date
    due_date = calculate_due_date(due_days)
    c.setFont("Helvetica", 10)
    c.drawString(320, height - 390, f"Eräpäivä: {due_date}")

    # Bank info box
    c.setStrokeColor(colors.black)
    c.rect(40, height - 600, 520, 160, fill=0)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 470, "Tilinumero (IBAN):")
    c.setFont("Helvetica", 10)
    c.drawString(200, height - 470, IBAN)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 490, "BIC:")
    c.setFont("Helvetica", 10)
    c.drawString(200, height - 490, BIC)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 510, "Eräpäivä:")
    c.setFont("Helvetica", 10)
    c.drawString(200, height - 510, due_date)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 530, "Viitenumero:")
    c.setFont("Helvetica", 10)
    c.drawString(200, height - 530, ref_number)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 550, "Saaja:")
    c.setFont("Helvetica", 10)
    c.drawString(200, height - 550, BANK_NAME)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 570, "Summa:")
    c.setFont("Helvetica", 10)
    c.drawString(200, height - 570, f"{amount} €")

    # Finalize PDF
    c.showPage()
    c.save()
    print(f"Generated {bill_type} bill for {name} with reference {ref_number}")


def main():
    customer_file = "emails.csv"
    bill_file = "laskut.csv"
    output_dir = "laskut"
    os.makedirs(output_dir, exist_ok=True)

    customers = load_customers_csv(customer_file)
    bills = load_bills_csv(bill_file)

    # Get the current generation date to add to filenames
    generation_date = datetime.today().strftime("%d.%m.%Y")

    # Load the last generated reference number
    last_generated_ref = load_generated_references()

    # For each customer, generate a bill for each type in laskut.csv
    for name, email in customers:
        for bill_type, amount, due_days in bills:
            # Generate the reference number using the rolling number
            ref_number = viitenumero.generate_reference(
                str(last_generated_ref + 1)
            )  # Generate the reference
            last_generated_ref += 1  # Increment the last generated reference number

            # Save the new reference number
            save_generated_reference(last_generated_ref)

            # Generate the PDF
            generate_pdf(
                name.strip(),
                email.strip(),
                ref_number,
                bill_type.strip(),
                amount.strip(),
                due_days.strip(),
                output_dir,
                generation_date,
            )


if __name__ == "__main__":
    main()
