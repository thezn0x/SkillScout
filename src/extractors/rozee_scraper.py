from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import re
import json
import os
import random as rd

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)
roles = [
    # ==================== SOFTWARE DEVELOPMENT ====================
    "Software Engineer",
    "Software Developer",
    "Full Stack Developer",
    "Frontend Developer",
    "Backend Developer",
    "Web Developer",
    "Mobile Developer",
    "iOS Developer",
    "Android Developer",
    "React Native Developer",
    "Flutter Developer",
    "DevOps Engineer",
    "Site Reliability Engineer (SRE)",
    "Embedded Systems Engineer",
    "Firmware Engineer",
    "Game Developer",
    "Unity Developer",
    "Unreal Engine Developer",
    "Desktop Application Developer",
    "API Developer",
    "Integration Engineer",
    "Middleware Developer",
    
    # ==================== DATA & ANALYTICS ====================
    "Data Scientist",
    "Data Analyst",
    "Data Engineer",
    "Machine Learning Engineer",
    "AI Engineer",
    "Business Intelligence Analyst",
    "BI Developer",
    "Data Architect",
    "Database Administrator (DBA)",
    "Big Data Engineer",
    "Data Quality Analyst",
    "Quantitative Analyst",
    "Research Scientist (AI/ML)",
    "Computer Vision Engineer",
    "NLP Engineer",
    "MLOps Engineer",
    
    # ==================== CLOUD & INFRASTRUCTURE ====================
    "Cloud Engineer",
    "Cloud Architect",
    "AWS Solutions Architect",
    "Azure Cloud Engineer",
    "Google Cloud Engineer",
    "Infrastructure Engineer",
    "Network Engineer",
    "Systems Engineer",
    "Systems Administrator",
    "Linux Administrator",
    "Windows Server Administrator",
    "Virtualization Engineer",
    "Containerization Engineer",
    "Kubernetes Administrator",
    "Docker Engineer",
    
    # ==================== SECURITY ====================
    "Cybersecurity Engineer",
    "Security Engineer",
    "Information Security Analyst",
    "Penetration Tester",
    "Ethical Hacker",
    "Security Operations Center (SOC) Analyst",
    "Security Architect",
    "Network Security Engineer",
    "Application Security Engineer",
    "Cloud Security Engineer",
    "Cryptographer",
    "Security Consultant",
    "Vulnerability Analyst",
    "Threat Intelligence Analyst",
    "Digital Forensics Analyst",
    
    # ==================== QUALITY & TESTING ====================
    "QA Engineer",
    "Test Engineer",
    "Automation Test Engineer",
    "Performance Test Engineer",
    "Manual Tester",
    "QA Analyst",
    "Test Automation Developer",
    "SDET (Software Development Engineer in Test)",
    "Quality Assurance Lead",
    "Test Architect",
    
    # ==================== PRODUCT & PROJECT ====================
    "Product Manager",
    "Technical Product Manager",
    "Product Owner",
    "Project Manager",
    "Technical Project Manager",
    "Scrum Master",
    "Agile Coach",
    "Program Manager",
    "Delivery Manager",
    
    # ==================== UX/UI & DESIGN ====================
    "UX Designer",
    "UI Designer",
    "UX/UI Designer",
    "Product Designer",
    "Interaction Designer",
    "Visual Designer",
    "UX Researcher",
    "Information Architect",
    "Motion Designer",
    "Design System Designer",
    "UX Writer",
    
    # ==================== BUSINESS & SYSTEMS ====================
    "Business Analyst",
    "Technical Business Analyst",
    "Systems Analyst",
    "Solution Architect",
    "Enterprise Architect",
    "Technical Architect",
    "Application Architect",
    "Integration Architect",
    "CRM Developer",
    "ERP Consultant",
    "SAP Consultant",
    "Salesforce Developer",
    "Dynamics 365 Developer",
    
    # ==================== WEB & DIGITAL ====================
    "WordPress Developer",
    "Shopify Developer",
    "Magento Developer",
    "E-commerce Developer",
    "CMS Developer",
    "Frontend Architect",
    "JavaScript Developer",
    "TypeScript Developer",
    
    # ==================== EMERGING TECH ====================
    "Blockchain Developer",
    "Smart Contract Developer",
    "Web3 Developer",
    "IoT Engineer",
    "AR/VR Developer",
    "Metaverse Developer",
    "Robotics Engineer",
    "5G Engineer",
    "Edge Computing Engineer",
    
    # ==================== SUPPORT & OPERATIONS ====================
    "Technical Support Engineer",
    "IT Support Specialist",
    "Help Desk Technician",
    "Desktop Support Engineer",
    "Application Support Engineer",
    "Database Support Engineer",
    "NOC Technician",
    "IT Operations Manager",
    
    # ==================== MANAGEMENT & LEADERSHIP ====================
    "Engineering Manager",
    "Development Manager",
    "Technical Lead",
    "Team Lead",
    "CTO (Chief Technology Officer)",
    "VP of Engineering",
    "Head of Engineering",
    "Director of Engineering",
    "IT Manager",
    "IT Director",
    "CIO (Chief Information Officer)",
    
    # ==================== CONSULTING ====================
    "Technical Consultant",
    "IT Consultant",
    "Software Consultant",
    "Cloud Consultant",
    "Security Consultant",
    "Digital Transformation Consultant",
    
    # ==================== ACADEMIC & RESEARCH ====================
    "Research Engineer",
    "Academic Researcher",
    "Computer Science Instructor",
    "Technical Trainer",
    "Curriculum Developer",
    
    # ==================== CONTENT & TECHNICAL WRITING ====================
    "Technical Writer",
    "Documentation Engineer",
    "API Documentation Writer",
    "Developer Advocate",
    "Developer Relations Engineer",
    "Community Manager",
    "Technical Content Writer",
    
    # ==================== SPECIALIZED ROLES ====================
    "GIS Developer",
    "Bioinformatics Engineer",
    "Quantitative Developer",
    "Algorithm Engineer",
    "High-Frequency Trading Developer",
    "Graphics Programmer",
    "Shader Programmer",
    "Audio Programmer",
    "Tools Developer",
    "Compiler Engineer",
    "Kernel Developer",
    "Firmware Developer",
    
    # ==================== LOW-CODE/NO-CODE ====================
    "Power Platform Developer",
    "Power Apps Developer",
    "Power BI Developer",
    "Low-Code Developer",
    "RPA Developer",
    "Automation Engineer",
    
    # ==================== PLATFORM SPECIFIC ====================
    "SharePoint Developer",
    "ServiceNow Developer",
    "Oracle Developer",
    "SAP ABAP Developer",
    "Mainframe Developer",
    "COBOL Developer",
    
    # ==================== FRAMEWORK SPECIALISTS ====================
    "React Developer",
    "Vue.js Developer",
    "Angular Developer",
    "Node.js Developer",
    "Django Developer",
    "Flask Developer",
    "Spring Boot Developer",
    ".NET Developer",
    "Laravel Developer",
    "Ruby on Rails Developer"]
roles = sorted(roles)
one_role = rd.choice(roles)

def fetch_rozee_jobs(skill, max_pages=1):
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        base_url = f"https://www.rozee.pk/job/jsearch/q/{skill}"

        for page_num in range(1, max_pages + 1):
            url = base_url if page_num == 1 else f"{base_url}/p{page_num}"
            print(f"Loading: {url}")

            page.goto(url, timeout=60000)
            time.sleep(5)

            job_cards = page.query_selector_all("div.job")
            print(f"Found {len(job_cards)} jobs")

            for card in job_cards:
                job = extract_single_job(card)
                if job and job.get("title"):
                    jobs.append(job)

            if page_num < max_pages:
                time.sleep(2)

        browser.close()

    print(f"Scraping complete. Total jobs: {len(jobs)}")
    return jobs


# ==========================================
# PAGE EXTRACTION
# ==========================================
def extract_single_job(card):
    job = {}

    title_el = card.query_selector("div.jhead h3 a, h3 a")
    if not title_el:
        return None

    job["title"] = clean_text(title_el.inner_text())
    href = title_el.get_attribute("href")
    job["url"] = f"https://www.rozee.pk/{href.lstrip('/')}" if href else None

    # COMPANY
    company_el = card.query_selector("div.cname a, div.jcompany a")
    job["company"] = clean_text(company_el.inner_text()) if company_el else "Unknown"

    # LOCATION
    location = "Pakistan"
    cname_div = card.query_selector("div.cname")
    if cname_div:
        links = cname_div.query_selector_all("a")
        if len(links) > 1:
            parts = [clean_text(l.inner_text()) for l in links[1:] if clean_text(l.inner_text())]
            if parts:
                location = ", ".join(parts) + ", Pakistan"

    job["location"] = location

    # DESCRIPTION
    desc_el = card.query_selector("div.jbody")
    if desc_el:
        text = clean_text(desc_el.inner_text())
        job["description"] = text[:500]

    # POSTED DATE
    footer = card.query_selector("div.jfooter")
    if footer:
        text = clean_text(footer.inner_text())
        abs_date = re.search(
            r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}",
            text
        )
        rel_date = re.search(r"\d+\s+(day|days|hour|hours|week|weeks)\s+ago", text, re.I)

        if abs_date:
            job["posted_date"] = abs_date.group(0)
        elif rel_date:
            job["posted_date"] = rel_date.group(0)

    # EXPERIENCE
    exp_el = card.query_selector("span.func-area-drn")
    if exp_el:
        exp_text = clean_text(exp_el.inner_text())
        job["experience_text"] = exp_text

        match = re.search(r"(\d+)\s*(Year|Years)", exp_text, re.I)
        if match:
            job["experience_years"] = int(match.group(1))

    # SKILLS
    skills = []
    for s in card.query_selector_all("span.label"):
        val = clean_text(s.inner_text())
        if val and len(val) < 50:
            skills.append(val)

    job["skills"] = skills
    job["skill_count"] = len(skills)

    # METADATA
    job["source"] = "rozee.pk"
    job["scraped_at"] = datetime.utcnow().isoformat()

    return job


# ==========================================
# HELPERS
# ==========================================
def clean_text(text):
    return " ".join(text.split()).strip(" ,.-") if text else ""


def save_jobs_to_json(jobs, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(jobs)} jobs to {filename}")


# ==========================================
# RUN
# ==========================================
if __name__ == "__main__":
    print("Starting rozee.pk scraper...")
    
    jobs = fetch_rozee_jobs(skill=one_role, max_pages=1)

    if jobs:
        output_path = os.path.join(OUTPUT_DIR, "rozee_raw_data.json")
        save_jobs_to_json(jobs, output_path)
        print(f"Data saved to: {output_path}")
    else:
        print("No jobs found")
