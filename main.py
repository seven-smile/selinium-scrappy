# # main.py francis

# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.options import Options


# options = Options()
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
# options.add_argument('--headless')
# driver = Chrome(options=options)
# url = "https://cfr.gov.mt/en/Pages/Home.aspx"
# driver.get(url)
# print(driver.title)
# driver.quit()

# main.py

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
import time
import random
from urllib.parse import urljoin, urlparse
import atexit
import signal
import sys

def signal_handler(sig, frame):
    print('\nCleaning up before exit...')
    sys.exit(0)

def cleanup_driver(driver):
    try:
        driver.quit()
    except:
        pass

def normalize_url(url, base_url):
    """Normalize URL to avoid duplicates"""
    if not url:
        return None
    # Remove fragments
    url = url.split('#')[0]
    # Remove trailing slash
    url = url.rstrip('/')
    # Ensure URL is absolute
    if not url.startswith('http'):
        url = urljoin(base_url, url)
    return url

def is_valid_url(url, base_domain):
    """Check if URL is valid and belongs to the same domain"""
    if not url:
        return False
    try:
        # Normalize URL first
        url = normalize_url(url, base_domain)
        if not url:
            return False

        parsed_url = urlparse(url)
        parsed_base = urlparse(base_domain)

        # Check if domains match
        if parsed_url.netloc != parsed_base.netloc:
            return False

        # Filter out non-HTML resources
        exclude_patterns = [
            '.pdf', '.doc', '.docx', '.xls', '.xlsx',
            'javascript:', 'mailto:', 'tel:', 'fax:',
            'whatsapp:', 'sms:', '#'
        ]

        return not any(pattern in url.lower() for pattern in exclude_patterns)
    except:
        return False

def get_file_details(link_element):
    """Extract file details from download links"""
    href = link_element.get_attribute('href') or ""
    file_name = link_element.text.strip() or href.split('/')[-1]
    file_type = href.split('.')[-1] if '.' in href else "Unknown"
    return {
        "file_name": file_name,
        "file_type": file_type,
        "file_size": "N/A",
        "link": href
    }

def random_delay():
    """Add random delay between requests"""
    delay = random.uniform(3, 7)
    print(f"Waiting for {delay:.2f} seconds...")
    time.sleep(delay)


def scrape_page_content(driver, wait, url, visited_urls, retry_count=0):
    """Scrape content from a single page"""
    if url in visited_urls:
        return None

    if retry_count >= 3:
        print(f"Max retries reached for {url}, skipping...")
        return None

    print(f"Scraping page: {url} (attempt {retry_count + 1})")

    try:
        driver.get(url)
        random_delay()

        # Print page title for debugging
        print(f"Page title: {driver.title}")

        # Check for Cloudflare block
        if "Attention Required! | Cloudflare" in driver.title:
            print(f"Cloudflare block detected on {url}, waiting and retrying...")
            time.sleep(10)  # Wait longer before retry
            driver.delete_all_cookies()
            return scrape_page_content(driver, wait, url, visited_urls, retry_count + 1)

        visited_urls.add(url)

        page_data = {
            "url": url,
            "title": driver.title,
            "content_sections": [],
            "downloads": [],
            "navigation_links": []  # New field for navigation links
        }

        # Wait for body and links to be present
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Try to find navigation menu first
            nav_selectors = [
                "#zz1_TopNavigationMenu", ".ms-topNavigationMenu",
                "nav", "#navigation", ".navigation",
                "#menu", ".menu", "#nav", ".nav",
                ".top-nav", "#topnav"
            ]

            for selector in nav_selectors:
                try:
                    nav_menu = driver.find_element(By.CSS_SELECTOR, selector)
                    nav_links = nav_menu.find_elements(By.TAG_NAME, "a")
                    for link in nav_links:
                        try:
                            href = link.get_attribute("href")
                            text = link.text.strip()
                            if href and text:
                                page_data["navigation_links"].append({
                                    "text": text,
                                    "url": href
                                })
                        except:
                            continue
                except:
                    continue

            # Get main content
            main_selectors = [
                "main", ".main-content", "#main", "article",
                ".content", "#content", ".page-content", "body"
            ]

            main_content = None
            for selector in main_selectors:
                try:
                    main_content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    if main_content:
                        print(f"Found main content using selector: {selector}")
                        break
                except:
                    continue

            if main_content:
                # Get all text-containing elements
                elements = main_content.find_elements(
                    By.XPATH, ".//*[normalize-space(text())][not(self::script)][not(self::style)]")

                current_section = {
                    "title": "",
                    "text_content": "",
                    "links": []
                }

                for element in elements:
                    if element.tag_name.startswith('h'):
                        # Save previous section if it has content
                        if current_section["text_content"] or current_section["links"]:
                            page_data["content_sections"].append(current_section.copy())
                        current_section = {
                            "title": element.text.strip(),
                            "text_content": "",
                            "links": []
                        }
                    else:
                        try:
                            text = element.text.strip()
                            if text:
                                current_section["text_content"] += text + "\n"

                            # Get links from this element
                            links = element.find_elements(By.TAG_NAME, "a")
                            for link in links:
                                try:
                                    href = link.get_attribute("href")
                                    if href and href.startswith('http'):
                                        current_section["links"].append({
                                            "text": link.text.strip(),
                                            "url": href
                                        })
                                except:
                                    continue
                        except:
                            continue

                # Add the last section if it has content
                if current_section["text_content"] or current_section["links"]:
                    page_data["content_sections"].append(current_section)

        except Exception as e:
            print(f"Error extracting content: {str(e)}")

        # Get downloads
        try:
            download_links = driver.find_elements(
                By.CSS_SELECTOR, "a[href$='.pdf'], a[href$='.doc'], a[href$='.docx'], a[href$='.xls'], a[href$='.xlsx']")
            for link in download_links:
                try:
                    page_data["downloads"].append(get_file_details(link))
                except:
                    continue
        except:
            pass

        return page_data

    except Exception as e:
        print(f"Error accessing page {url}: {str(e)}")
        if retry_count < 3:
            print(f"Retrying {url} after error...")
            time.sleep(10)  # Wait longer after error
            return scrape_page_content(driver, wait, url, visited_urls, retry_count + 1)
        return None

def scrape_website():
    driver = None
    try:
        options = uc.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-blink-features=AutomationControlled')

        driver = uc.Chrome(options=options)
        # Register cleanup function
        atexit.register(cleanup_driver, driver)
        signal.signal(signal.SIGINT, signal_handler)

        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        wait = WebDriverWait(driver, 30)  # Increased wait time

        base_url = "https://cfr.gov.mt/en/Pages/Home.aspx"
        visited_urls = set()
        urls_to_visit = {base_url}

        site_data = {
            "base_url": base_url,
            "main_pages": [],
            "contact_information": {
                "email": "",
                "phone": "",
                "fax": "",
                "address": ""
            }
        }

        # First scrape the homepage
        print("Starting with homepage...")
        home_data = scrape_page_content(driver, wait, base_url, visited_urls)
        if home_data:
            site_data["main_pages"].append(home_data)

            # Process navigation links first
            print("Processing navigation links...")
            for nav_link in home_data.get("navigation_links", []):
                url = nav_link["url"]
                if url and url.startswith(base_url):
                    normalized_url = normalize_url(url, base_url)
                    if normalized_url and normalized_url not in visited_urls:
                        urls_to_visit.add(normalized_url)
                        print(f"Added navigation URL to queue: {normalized_url}")

            # Then process all other links
            print("Processing other links...")
            for section in home_data["content_sections"]:
                for link in section["links"]:
                    url = link["url"]
                    if url and is_valid_url(url, base_url):
                        normalized_url = normalize_url(url, base_url)
                        if normalized_url and normalized_url not in visited_urls:
                            urls_to_visit.add(normalized_url)
                            print(f"Added content URL to queue: {normalized_url}")

        print(f"Found {len(urls_to_visit)} URLs to process")
        total_urls = len(urls_to_visit)
        processed_urls = 0

        # Process remaining pages
        while urls_to_visit:
            current_url = urls_to_visit.pop()
            processed_urls += 1
            print(f"\nProcessing URL {processed_urls} of {total_urls}")

            if current_url not in visited_urls:
                page_data = scrape_page_content(driver, wait, current_url, visited_urls)
                if page_data:
                    site_data["main_pages"].append(page_data)
                    print(f"Successfully scraped: {current_url}")

                    # Add new URLs from navigation links
                    for nav_link in page_data.get("navigation_links", []):
                        url = nav_link["url"]
                        if url and url.startswith(base_url):
                            normalized_url = normalize_url(url, base_url)
                            if normalized_url and normalized_url not in visited_urls:
                                urls_to_visit.add(normalized_url)
                                total_urls = len(urls_to_visit) + processed_urls
                                print(f"Added new navigation URL to queue: {normalized_url}")

                    # Extract contact information if not already found
                    if not all(site_data["contact_information"].values()):
                        contact_text = " ".join([section["text_content"] for section in page_data["content_sections"]])

                        if not site_data["contact_information"]["email"]:
                            email_match = re.search(r'[\w\.-]+@[\w\.-]+', contact_text)
                            if email_match:
                                site_data["contact_information"]["email"] = email_match.group(0)

                        if not site_data["contact_information"]["phone"]:
                            phone_match = re.search(r'(?:Phone|Tel|T)[\s:]+([+\d\s-]+)', contact_text, re.IGNORECASE)
                            if phone_match:
                                site_data["contact_information"]["phone"] = phone_match.group(1).strip()

                        if not site_data["contact_information"]["fax"]:
                            fax_match = re.search(r'(?:Fax|F)[\s:]+([+\d\s-]+)', contact_text, re.IGNORECASE)
                            if fax_match:
                                site_data["contact_information"]["fax"] = fax_match.group(1).strip()

                        if not site_data["contact_information"]["address"]:
                            address_match = re.search(r'Address:?\s*([^\n]+)', contact_text, re.IGNORECASE)
                            if address_match:
                                site_data["contact_information"]["address"] = address_match.group(1).strip()

                random_delay()

        return site_data

    except Exception as e:
        print(f"An error occurred during scraping: {str(e)}")
        raise
    finally:
        if driver:
            try:
                atexit.unregister(cleanup_driver)  # Unregister cleanup if we're handling it here
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    try:
        print("Starting scraping process...")
        site_data = scrape_website()
        print("\nSaving data to file...")
        with open('cfr_gov_mt_data.json', 'w', encoding='utf-8') as f:
            json.dump(site_data, f, indent=2, ensure_ascii=False)
        print("Scraping completed successfully!")
        print(f"Total pages scraped: {len(site_data['main_pages'])}")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        print("\nScript finished executing.")
