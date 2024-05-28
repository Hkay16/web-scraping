# main.py
import os
import sys
import subprocess

def run_scraper():
    try:
        # Navigate to the scripts directory
        os.chdir(os.path.join(os.path.dirname(__file__), 'scripts'))
        
        # Run the scraper script
        subprocess.run([sys.executable, 'scraper.py'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the scraper: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_scraper()
