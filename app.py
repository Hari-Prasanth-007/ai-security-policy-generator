from flask import Flask, render_template, request, send_file
from io import BytesIO
from datetime import date
import re

app = Flask(__name__)

def clean(value, default="Not specified"):
    value = (value or "").strip()
    return value[:200] if value else default

def generate_policy(data):
    org = clean(data.get("org_name"), "Small Organisation")
    industry = clean(data.get("industry"))
    employees = clean(data.get("employees"))
    data_types = [x for x in request.form.getlist("data_types") if x in {
        "Customer information", "Employee information", "Financial records",
        "Intellectual property", "Public information"
    }]
    needs = [x for x in request.form.getlist("needs") if x in {
        "Passwords and accounts", "Data protection", "Email and phishing",
        "Backups and recovery", "Incident response", "Remote work", "AI tool usage"
    }]
    data_label = ", ".join(data_types) if data_types else "Information handled by the organisation"
    needs_label = ", ".join(needs) if needs else "Core security controls"

    sections = [
        ("1. Purpose and scope",
         f"This policy establishes minimum information-security practices for {org}, operating in {industry}. "
         f"It applies to employees, contractors, temporary staff, approved devices, accounts, and systems. "
         f"The policy is intended for an organisation with approximately {employees} employees. "
         "Management must communicate this policy and review it at least annually."),
        ("2. Information classification and handling",
         f"The organisation handles: {data_label}. Information owners must identify confidential and sensitive "
         "records, limit access to authorised people, use approved storage locations, and securely dispose of "
         "records when retention is no longer required. Do not place confidential data in public links or "
         "unapproved applications. Collect only information needed for a legitimate business purpose."),
        ("3. Identity, passwords and access control",
         "Give each worker a unique account; shared accounts should be avoided. Use long, unique passwords and "
         "a reputable password manager where approved. Enable multi-factor authentication (MFA), especially for "
         "email, administrator accounts, cloud services, and remote access. Grant the minimum access needed for "
         "each role, review permissions periodically, and promptly disable accounts when access is no longer needed. "
         "Administrator privileges must be limited and used only when necessary."),
        ("4. Devices, updates and malware protection",
         "Keep operating systems, browsers, applications, and security tools updated. Enable supported endpoint "
         "protection and device screen locks. Install software only from trusted, authorised sources. Lost devices, "
         "unexpected security warnings, or suspected malware must be reported promptly. Do not bypass security "
         "controls or use unsupported devices to access sensitive information."),
        ("5. Email, web and phishing",
         "Check unexpected requests for payments, credentials, or confidential information using a separate trusted "
         "channel. Do not open suspicious links or attachments. Report suspected phishing to the designated "
         "security contact without forwarding it widely. Verify changes to supplier bank details independently. "
         "Use approved file-sharing services and avoid public Wi-Fi for sensitive work unless an approved secure "
         "connection is used."),
        ("6. Data protection and privacy",
         "Restrict access to sensitive information, protect transfers with approved encryption, and use secure "
         "storage. Do not send passwords or authentication codes by email or chat. Handle personal information "
         "according to applicable privacy and contractual requirements. Report accidental disclosure immediately. "
         "Do not collect or retain personal data without a defined business need."),
        ("7. Backup and recovery",
         "Identify critical files and systems and back them up on a documented schedule. Protect backups from "
         "unauthorised access and ransomware; keep an isolated or immutable copy where feasible. Test restoration "
         "at planned intervals and document recovery steps, responsibilities, and recovery priorities."),
        ("8. Incident reporting and response",
         "Report suspected account compromise, malware, lost devices, data disclosure, or unusual system activity "
         "immediately to the designated manager or security contact. Preserve relevant evidence and avoid deleting "
         "logs or messages. The response lead should assess severity, contain affected systems when appropriate, "
         "reset compromised credentials, preserve evidence, restore safely, and document decisions. Notify affected "
         "parties or authorities when required by applicable law or contract. Only authorised people may make public statements."),
        ("9. Remote work and physical security",
         "Use approved devices and secure connections for remote work. Keep devices physically secure and lock "
         "screens when unattended. Do not allow unauthorised people to use work accounts or view confidential "
         "records. Report lost equipment promptly and return organisational equipment when employment or engagement ends."),
        ("10. Responsible use of AI tools",
         "Use only AI tools approved by the organisation for work. Do not enter passwords, authentication codes, "
         "customer personal data, confidential documents, source code, or other restricted information into public "
         "AI services unless management has explicitly approved the tool and data handling. Verify AI-generated "
         "security advice and code before relying on it; AI output can be incorrect or unsafe. A human owner must "
         "approve policies and consequential decisions."),
        ("11. Training and responsibilities",
         "Management is responsible for approving this policy and assigning a security contact. Users must follow "
         "the policy, complete security awareness training, protect credentials, and report incidents. System "
         "administrators must maintain updates, access controls, backups, and logs appropriate to the organisation's risk."),
        ("12. Exceptions, enforcement and review",
         "Exceptions must be documented, justified, approved by management, and given an expiry or review date. "
         "Policy violations may lead to corrective action consistent with organisational rules and applicable law. "
         "Review this policy annually and after significant incidents, system changes, or changes in legal obligations."),
        ("13. Implementation checklist",
         "□ Name a policy owner and incident contact.\n"
         "□ Enable MFA on email and important accounts.\n"
         "□ Review employee and administrator access.\n"
         "□ Apply updates and enable device protection.\n"
         "□ Set up and test protected backups.\n"
         "□ Train staff to report phishing and incidents.\n"
         "□ Approve AI tools and define data-sharing restrictions.\n"
         "□ Record the approval date and next review date.")
    ]
    chosen = "\n".join(f"- {n}" for n in needs) if needs else "- Core security controls"
    content = [
        f"{org.upper()}",
        "INFORMATION SECURITY POLICY",
        f"Generated on: {date.today().isoformat()}",
        f"Industry: {industry} | Approximate employees: {employees}",
        f"Priority requirements selected: {needs_label}",
        "",
        "IMPORTANT: This is a starter template generated from user inputs. It is not legal advice or a guarantee "
        "of compliance. A responsible manager should review, adapt, approve, and communicate it before use.",
        ""
    ]
    for title, body in sections:
        content.extend([title, body, ""])
    content.extend([
        "Approval record",
        "Policy owner: ______________________________",
        "Approved by: _______________________________",
        "Approval date: _____________________________",
        "Next review date: __________________________",
        "",
        "Selected priorities for follow-up",
        chosen
    ])
    return "\n".join(content)

@app.route("/", methods=["GET", "POST"])
def index():
    policy = None
    if request.method == "POST":
        policy = generate_policy(request.form)
    return render_template("index.html", policy=policy)

@app.route("/download", methods=["POST"])
def download():
    policy = request.form.get("policy", "")
    if not policy.strip():
        return "No policy to download. Generate a policy first.", 400
    output = BytesIO(policy.encode("utf-8"))
    output.seek(0)
    return send_file(output, mimetype="text/plain; charset=utf-8",
                     as_attachment=True, download_name="security_policy.txt")

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
