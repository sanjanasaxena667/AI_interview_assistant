Step 1: Install the Tools

Ollama: Download from ollama.com and install.

Run this command in terminal: ollama pull deepseek-v3.1:671b-cloud

Tesseract OCR: Download this Windows Installer and install it.

Install to default location: C:\Program Files\Tesseract-OCR

Poppler: Download this Zip file.

Extract the folder to C:\Program Files\poppler.

Check that this folder exists: C:\Program Files\poppler\poppler-24.02.0\Library\bin (This is where pdftoppm.exe lives).

Step 2: Check the Code Path

Open interview_assistant.py and make sure line 13 matches your actual Poppler folder from Step 1.

# Update this path if your folder name is different!

POPPLER_PATH = r"C:\Program Files\poppler\poppler-24.02.0\Library\bin"

Step 3: Install Python Libraries

Open your terminal/command prompt in the project folder and run:

pip install streamlit langchain-ollama langchain-core pytesseract pdf2image pillow

Step 4: Run the App

Run this command:

streamlit run abcd.py
