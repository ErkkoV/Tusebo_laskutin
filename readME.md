
# Tusebo Laskutin Setup Guide

This guide will help you set up the project environment, install dependencies, and configure the necessary files to generate bills with custom references.

---

## 1. Setting Up the Virtual Environment

To set up a virtual environment for the project:

### Step 1: Create a Virtual Environment

Run the following command to create a virtual environment in the project directory:

```bash
python -m venv venv
```

This will create a new directory called `venv` that contains the isolated environment for this project.

### Step 2: Activate the Virtual Environment

- Activate the virtual environment using:

```bash
.env\Scripts\Activate
```

If you get error message, try:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

You should now see `(venv)` before the prompt, indicating that the virtual environment is active.

### Step 3: Install Dependencies

Once the virtual environment is activated, install the project dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## 2. Setting Up the `.env` File

### Step 1: Copy `.env.example` to `.env`

To configure your environment, copy the `.env.example` file and rename it to `.env`:

```bash
cp .env.example .env
```

### Step 2: Update `.env` File

Edit the `.env` file with the correct values for your project:

```ini
IBAN=FI00 1234 5600 0007 89
BIC=NDEAFIHH
BANK_NAME=Fictional Bank Oy
EMAIL=esimerkki@esimerkki.com
PHONE=07099999999
ADDRESS=Esimerkkikuja 13, 70015 KUJALA
YNUMBER=01-9977111
```

These values are needed to generate the bills and will be read by the program to populate the bank information on each bill.

---

## 3. Setting Up `emails.csv`

Create the `emails.csv` file in the root of the project directory. The file should contain customer names, email addresses, and customer numbers (in the format: `name;email;customer_number`). Here's an example:

```csv
petteri esimerkki;petteri.esimerkki@esimerkki.fi
juuso jokunen;juuso@esimerkki.fi
```

- **Name**: Full name of the customer.
- **Email**: Email address of the customer.

---

## 4. Setting Up `laskut.csv`

Create the `laskut.csv` file to define the types of bills, their amounts, and the number of days the customer has to pay. Here’s an example:

```csv
jasenmaksu;20.00;180
kannatusmaksu;40.00;180
kausimaksu;60;30
```

- **Bill Type**: A description of the bill type (e.g., membership fee, support fee, etc.).
- **Amount**: The amount due for the bill.
- **Days to Pay**: Number of days after which the bill is due.

---

## 5. Reference Number Generation and Storing

### Step 1: Reference Number Generation

The reference numbers are generated based on finnish bank reference standard.

### Step 2: Tracking Latest Reference Number

The program will store the **last generated reference number** in the `references.txt` file. Each time a bill is generated, it will update the `references.txt` file with the latest reference number.

Example of `references.txt`:

```text
101
```

In order to ensure unique reference numbers each time a new bill is generated, the program will read this file, increment the reference number, and store the new number back in the file.

---

## 6. Running the Program

Once everything is set up, you can run the program to generate the bills:

```bash
python generate.py
```

Or use whole path, example:

```bash
python C:/Projects/Tusebo_laskutin/generate.py
```

This will read the `emails.csv` and `laskut.csv` files, generate reference numbers, create PDFs for each customer, and save them in the `laskut` folder. The bill filenames will include the customer name, date, and the reference number.

---
