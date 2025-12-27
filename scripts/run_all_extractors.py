import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.extractors.rozee import RozeeExtractor

def main():
    print("Starting Rozee.pk scraper...")
    
    extractor = RozeeExtractor(role="python",base_url="https://www.rozee.pk/job/jsearch/q/",cards_class="job")
    jobs = extractor.fetch_jobs(max_pages=2)
    
    print(f"\nTotal jobs scraped: {len(jobs)}")
    
    if jobs:
        extractor.save_jobs("data/raw/rozee.json", jobs)
        print(f"Saved to data/raw/rozee_python_{len(jobs)}_jobs.json")
        
        print("\nFirst job sample:")
        print("-" * 40)
        sample = jobs[0]
        for key in ["title", "company", "location", "skills_count"]:
            if key in sample:
                print(f"{key}: {sample[key]}")
    
    print("\nDone.")

if __name__ == "__main__":
    main()
