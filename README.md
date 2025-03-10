# AI-Powered Feature Request Automation

This project automates the processing of feature requests received via emails and PDF documents, and creates Trello cards for tracking them.

## Overview

The system monitors a designated folder for new feature request emails or PDFs, extracts key information using NLP and regex patterns, and automatically creates organized Trello cards for team tracking.

## Components

- **extract.py**: Extracts insights from emails and PDFs using regex patterns
- **watcher.py**: Monitors the input folder for new files and triggers processing
- **trello_automation.py**: Creates Trello cards based on the extracted information

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://your-repo-url.git
   cd ai_automation
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. Set up your Trello credentials in `trello_automation.py`:
   - API_KEY
   - TOKEN
   - BOARD_ID
   - LIST_ID_TODO

5. Create the sample_inputs folder if it doesn't exist:
   ```
   mkdir -p sample_inputs
   ```

## Usage

1. Start the file watcher to begin monitoring:
   ```
   python watcher.py
   ```

2. Add email files (text format) or PDF feature requests to the `sample_inputs` folder.

3. The system will automatically:
   - Extract key information (feature name, priority, deadline, teams)
   - Save the data to `output.yaml`
   - Create Trello cards with appropriate details

## File Formats

The system can parse two main types of inputs:

### Emails (text format)
```
Subject: Feature Request - [Feature Name]

Hello Team,

Priority: [High/Medium/Low]
Deadline: [Timeframe]
Teams involved: [Team1, Team2]

Best,
[Name]
```

### PDF Documents
```
Requested Feature: [Feature Name]
Priority Level: [High/Medium/Low]
Deadline: [Timeframe]
Assigned Teams: [Team1, Team2]
Details: [Additional information]
```

## Extending the System

To add support for additional document formats or extraction patterns:
- Modify the regex patterns in `extract_insights()` function in `extract.py`
- Add new extraction methods as needed

## Troubleshooting

- If modules are not found, ensure you're running within the virtual environment
- For Trello API issues, verify your API credentials and permissions
- Check `output.yaml` to ensure proper extraction before Trello card creation

## License