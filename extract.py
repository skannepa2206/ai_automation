import spacy
import re
import yaml
import pdfplumber
from collections import defaultdict

# Load NLP model
nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
    return text.strip() if text else "No text extracted from PDF."


def clean_text(text):
    """Removes unnecessary newlines and extra spaces."""
    return re.sub(r'\s+', ' ', text).strip()


def extract_insights(text):
    """Extracts key insights from an email or document text."""
    text = clean_text(text)  # Clean input text
    insights = defaultdict(list)

    # Extract feature from subject line
    subject_match = re.search(r'Subject: Feature Request - ([\w\s&-]+?)(?:\s+Hello|\s*$)', text, re.I)
    if subject_match:
        insights["Feature"] = subject_match.group(1).strip()

    # Extract requested feature from PDF format
    feature_match = re.search(r'Requested Feature:[\s]+([\w\s&-]+?)(?:\s+Priority|\s*$)', text, re.I)
    if feature_match and "Feature" not in insights:
        insights["Feature"] = feature_match.group(1).strip()

    # Extract priority
    priority_match = re.search(r'Priority:[\s]+(High|Medium|Low)(?:\s+Deadline|\s*$)', text, re.I)
    if priority_match:
        insights["Priority"] = priority_match.group(1).capitalize()

    # Also check for priority level format
    priority_level_match = re.search(r'Priority Level:[\s]+(High|Medium|Low)(?:\s+Deadline|\s*$)', text, re.I)
    if priority_level_match and "Priority" not in insights:
        insights["Priority"] = priority_level_match.group(1).capitalize()

    # Extract deadline
    deadline_match = re.search(r'Deadline:[\s]+([\w\s]+?)(?:\s+Teams involved|\s+Assigned Teams|\s*$)', text, re.I)
    if deadline_match:
        insights["Deadline"] = deadline_match.group(1).strip()

    # Extract assigned teams
    assigned_match = re.search(r'Teams involved:[\s]+([\w\s,&]+?)(?:\s+Best,|\s+Details:|\s*$)', text, re.I)
    if assigned_match:
        teams_text = assigned_match.group(1).strip()
        teams = [team.strip() for team in teams_text.split(",")]
        teams = [team for team in teams if team]  # Remove empty values
        insights["Assigned to"] = teams

    # Check for alternate format of assigned teams
    assigned_alt_match = re.search(r'Assigned Teams:[\s]+([\w\s,&]+?)(?:\s+Details:|\s*$)', text, re.I)
    if assigned_alt_match and "Assigned to" not in insights:
        teams_text = assigned_alt_match.group(1).strip()
        teams = [team.strip() for team in teams_text.split(",")]
        teams = [team for team in teams if team]  # Remove empty values
        insights["Assigned to"] = teams

    return dict(insights)  # Convert defaultdict to dict before returning


def save_to_yaml(data, output_file="output.yaml"):
    """Saves extracted insights to a YAML file."""
    with open(output_file, "w") as file:
        yaml.dump(data, file, default_flow_style=False)  # Save list as YAML
    print(f"✅ Extracted insights saved to {output_file}")


if __name__ == "__main__":
    all_extracted_data = []  # Store extracted data for all files

    # Load and process email
    with open("sample_inputs/email_1.txt", "r") as file:
        email_text = file.read()
        email_summary = extract_insights(email_text)
        print("Extracted Insights from Email:\n", yaml.dump(email_summary, default_flow_style=False))
        all_extracted_data.append(email_summary)

    # Load and process PDF
    pdf_text = extract_text_from_pdf("sample_inputs/feature_request.pdf")
    if pdf_text and pdf_text != "No text extracted from PDF.":
        pdf_summary = extract_insights(pdf_text)
        print("\nExtracted Insights from PDF:\n", yaml.dump(pdf_summary, default_flow_style=False))
        all_extracted_data.append(pdf_summary)
    else:
        print("\nNo text extracted from PDF. Please check the document format.")

    # Save all extracted data to output.yaml
    save_to_yaml(all_extracted_data, "output.yaml")
