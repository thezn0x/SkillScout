import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

HEADERS = {
    'User-Agent': 'SkillScout/1.0 (Job Market Analytics; +https://github.com/ZN-0X/skillscout)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

def fetch_rozee_jobs(skill="python", max_pages=1):
    jobs = []
    base_url = f"https://www.rozee.pk/job/jsearch/q/{skill}"
    
    print(f"Searching for '{skill}' jobs on Rozee.pk...")
    print("=" * 60)
    
    for page in range(1, max_pages + 1):
        print(f"\nScraping page {page}...")
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}/p{page}"
        
        print(f"URL: {url}")
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            print(f"Request successful (Status: {response.status_code})")
            soup = BeautifulSoup(response.text, 'html.parser')
            job_container = soup.find('div', {'class': 'jlist', 'id': 'jobs'})
            
            if not job_container:
                print(f"No job container found on page {page}")
                break
            
            job_cards = job_container.find_all('div', class_='job')
            print(f"Found {len(job_cards)} job cards")
            for i, card in enumerate(job_cards, 1):
                print(f"Extracting job {i}...", end=" ")
                job_data = extract_job_data(card)
                
                if job_data:
                    jobs.append(job_data)
                    print(f"{job_data['title']}")
                else:
                    print(" Failed")

            if page < max_pages:
                print(f"\nWaiting 2 seconds before next page...")
                time.sleep(2)
                
        except requests.RequestException as e:
            print(f"Error: {e}")
            break
    
    print("\n" + "=" * 60)
    print(f"Scraping complete! Total jobs: {len(jobs)}")
    return jobs

def extract_job_data(card):
    try:
        job = {}
        title_tag = card.find('h3', class_='s-18')
        if title_tag:
            link = title_tag.find('a')
            if link:
                job['title'] = link.get_text(strip=True)
                href = link.get('href')
                job['url'] = f"https:{href}" if href and href.startswith('//') else href

        company_tag = card.find('div', class_='cname')
        if company_tag:
            links = company_tag.find_all('a')

            if len(links) > 0:
                company_text = links[0].get_text(strip=True)
                job['company'] = company_text.rstrip(',').strip()
            
            if len(links) > 1:
                job['city'] = links[1].get_text(strip=True)

            if len(links) > 2:
                job['country'] = links[2].get_text(strip=True).lstrip(',').strip()

            location_parts = []
            if job.get('city'):
                location_parts.append(job['city'])
            if job.get('country'):
                location_parts.append(job['country'])
            job['location'] = ', '.join(location_parts)
        desc_tag = card.find('div', class_='jbody')
        if desc_tag:
            job['description'] = desc_tag.get_text(strip=True)
        calendar_icon = card.find('i', class_='rz-calendar')
        if calendar_icon:
            date_span = calendar_icon.parent
            if date_span:
                date_text = date_span.get_text(strip=True)
                job['posted_date'] = date_text
        exp_tag = card.find('span', class_='func-area-drn')
        if exp_tag:
            job['experience'] = exp_tag.get_text(strip=True)
        skills_tags = card.find_all('span', class_='label label-default')
        skills = [skill.get_text(strip=True) for skill in skills_tags]
        job['skills'] = skills
        job['source'] = 'rozee'
        job['scraped_date'] = datetime.now().isoformat()
        
        return job
        
    except Exception as e:
        # If anything goes wrong, print error and return None
        print(f"Error extracting job: {e}")
        return None

if __name__ == "__main__":
    """
    This only runs when you execute the file directly:
    python src/extractors/rozee_scraper.py
    """
    
    print("\n" + "=" * 60)
    print("SKILLSCOUT - ROZEE.PK SCRAPER")
    print("=" * 60)
    
    # Scrape 1 page of Python jobs
    jobs = fetch_rozee_jobs("python", max_pages=1)
    
    # Display results
    print(f"\nRESULTS:")
    print(f"   Total jobs scraped: {len(jobs)}")
    
    if jobs:
        print(f"\nEXAMPLE JOB (First result):")
        print("-" * 60)
        
        # Print first job in readable format
        first_job = jobs[0]
        for key, value in first_job.items():
            # Handle skills list specially
            if key == 'skills' and isinstance(value, list):
                print(f"   {key}: {', '.join(value)}")
            else:
                # Truncate long descriptions
                if key == 'description' and len(str(value)) > 100:
                    print(f"   {key}: {str(value)[:100]}...")
                else:
                    print(f"   {key}: {value}")
        
        print("-" * 60)
        
        # Show all job titles
        print(f"\nALL JOB TITLES:")
        for i, job in enumerate(jobs, 1):
            print(f"   {i}. {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
    
    else:
        print("No jobs found!")
    
    print("\n" + "=" * 60)
    print("Done!")