# AI Security Policy Generator for a Small Organisation

A small Flask web application that creates a tailored security-policy starter template from form inputs. It uses a rule-based generator and does not send information to an external AI service, so it works without an API key or internet access after installation.

## Requirements
- Python 3.9 or newer
- Internet connection only for installing Flask (unless Flask is already installed)

## Run on Windows
1. Extract the ZIP file.
2. Open the extracted `ai_security_policy_generator` folder.
3. Click the folder address bar, type `cmd`, and press Enter.
4. Run:
   `python -m pip install -r requirements.txt`
5. Then run:
   `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.
7. To stop the server, press `Ctrl+C` in the command window.

## Run on Linux/macOS
`python3 -m pip install -r requirements.txt`
`python3 app.py`
Then open `http://127.0.0.1:5000`.

## Features
- Organisation name, industry and size
- Select data types and security priorities
- Generates a policy with access control, data protection, incident response, backups, device security, remote work, AI use and review sections
- Edit, copy, print/save as PDF, or download the policy as a text file

## Project structure
- `app.py` — Flask routes and policy generation logic
- `templates/index.html` — user interface
- `requirements.txt` — Python dependency

## Important note
This is an educational prototype. The policy generator is template/rule-based rather than a connected generative-AI model. Review all content with an appropriate responsible person and adapt it to the organisation's actual risks, contracts, and applicable law before use. Do not enter real confidential information into a demo system.
