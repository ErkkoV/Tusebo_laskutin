import os
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
from datetime import datetime, timedelta
from maksu import viitenumero  # Import your reference number generation library


# Load .env file
load_dotenv()

IBAN = os.getenv("IBAN")
BIC = os.getenv("BIC")
BANK_NAME = os.getenv("BANK_NAME")


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
    # Add the generation date to the filename
    filename = os.path.join(
        output_dir, f"Tusebo_lasku_{safe_name}_{bill_type}_{generation_date}.pdf"
    )
    c = canvas.Canvas(filename, pagesize=A4)

    width, height = A4
    c.setFont("Helvetica", 12)

    c.drawString(100, height - 100, f"To: {name} <{email}>")
    c.drawString(100, height - 130, f"Amount Due: €{amount}")
    c.drawString(100, height - 160, f"Reference Number: {ref_number}")
    c.drawString(100, height - 200, f"Bill Type: {bill_type.capitalize()}")

    # Calculate and display the due date
    due_date = calculate_due_date(due_days)
    c.drawString(100, height - 230, f"Due Date: {due_date}")

    c.drawString(100, height - 260, "Please make your payment to:")
    c.drawString(100, height - 290, f"Bank: {BANK_NAME}")
    c.drawString(100, height - 310, f"IBAN: {IBAN}")
    c.drawString(100, height - 330, f"BIC: {BIC}")

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
