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

#gpt-3

# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import json

# # Initialize Chrome with options
# options = Options()
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
# options.add_argument('--headless')
# driver = Chrome(options=options)

# # Function to extract menu items
# def extract_menu(driver):
#     menu_items = []
#     try:
#         header_menu = driver.find_elements(By.CSS_SELECTOR, 'nav a')  # Adjust CSS selector as needed
#         for item in header_menu:
#             menu_items.append({
#                 "menu_item": item.text.strip(),
#                 "link": item.get_attribute('href')
#             })
#     except Exception as e:
#         print(f"Error extracting menu: {e}")
#     return menu_items

# # Function to extract sections from a page
# def extract_sections(driver):
#     sections = []
#     try:
#         page_sections = driver.find_elements(By.CSS_SELECTOR, 'section, div')  # Adjust selectors based on structure
#         for section in page_sections:
#             title = section.find_element(By.TAG_NAME, 'h2').text if section.find_elements(By.TAG_NAME, 'h2') else "No title"
#             content = section.text.strip()
#             links = [
#                 {"text": link.text.strip(), "url": link.get_attribute('href')}
#                 for link in section.find_elements(By.TAG_NAME, 'a')
#             ]
#             sections.append({"section_title": title, "content": content, "links": links})
#     except Exception as e:
#         print(f"Error extracting sections: {e}")
#     return sections

# # Function to extract links to other pages
# def extract_links(driver):
#     links = []
#     try:
#         global_links = driver.find_elements(By.CSS_SELECTOR, 'a')  # Adjust CSS selector as needed
#         for link in global_links:
#             links.append({
#                 "link_text": link.text.strip(),
#                 "url": link.get_attribute('href')
#             })
#     except Exception as e:
#         print(f"Error extracting links: {e}")
#     return links

# # Main scraping function
# def scrape_website(url):
#     site_data = {
#         "site_overview": {
#             "homepage": {
#                 "title": "",
#                 "header_menu": [],
#                 "sections": []
#             },
#             "other_pages": []
#         },
#         "global_links": [],
#         "contact_information": {
#             "email": "",
#             "phone": "",
#             "fax": "",
#             "address": ""
#         },
#         "downloads": []
#     }

#     try:
#         # Open the homepage
#         driver.get(url)
#         site_data["site_overview"]["homepage"]["title"] = driver.title.strip()
#         site_data["site_overview"]["homepage"]["header_menu"] = extract_menu(driver)
#         site_data["site_overview"]["homepage"]["sections"] = extract_sections(driver)

#         # Extract all global links
#         global_links = extract_links(driver)
#         site_data["global_links"] = global_links

#         # Visit other pages and extract content
#         for link in global_links:
#             page_url = link["url"]
#             if page_url and "http" in page_url:  # Filter valid URLs
#                 driver.get(page_url)
#                 page_title = driver.title.strip()
#                 sections = extract_sections(driver)
#                 site_data["site_overview"]["other_pages"].append({
#                     "page_title": page_title,
#                     "url": page_url,
#                     "sections": sections,
#                     "downloads": []  # Add logic for downloads here if needed
#                 })

#     except Exception as e:
#         print(f"Error scraping website: {e}")
#     finally:
#         driver.quit()

#     return site_data

# # Scrape the website and save data to a JSON file
# url = "https://cfr.gov.mt/en/Pages/Home.aspx"
# scraped_data = scrape_website(url)

# # Save the data in JSON format
# with open("scraped_data.json", "w", encoding="utf-8") as f:
#     json.dump(scraped_data, f, ensure_ascii=False, indent=4)

# print("Scraping complete. Data saved to scraped_data.json")


#claudia works 1

# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import json
# import re
# import time

# def get_file_details(link_element):
#     """Extract file details from download links"""
#     href = link_element.get_attribute('href') or ""
#     file_name = link_element.text or "Unknown"
#     file_type = href.split('.')[-1] if '.' in href else "Unknown"
#     return {
#         "file_name": file_name,
#         "file_type": file_type,
#         "file_size": "N/A",
#         "link": href
#     }

# def scrape_section(section_element):
#     """Scrape a single section's content"""
#     try:
#         title_element = section_element.find_element(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")
#         title = title_element.text
#     except:
#         title = "Untitled Section"

#     content = section_element.text
#     links = []

#     try:
#         for link in section_element.find_elements(By.TAG_NAME, "a"):
#             href = link.get_attribute("href")
#             if href:  # Only add links that have an href attribute
#                 links.append({
#                     "text": link.text.strip(),
#                     "url": href
#                 })
#     except:
#         pass

#     return {
#         "section_title": title,
#         "content": content,
#         "links": links
#     }

# def scrape_website():
#     options = Options()
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
#     options.add_argument('--headless')

#     driver = Chrome(options=options)
#     wait = WebDriverWait(driver, 20)  # Increased wait time

#     try:
#         url = "https://cfr.gov.mt/en/Pages/Home.aspx"
#         driver.get(url)
#         time.sleep(5)  # Allow time for JavaScript to load

#         site_data = {
#             "site_overview": {
#                 "homepage": {
#                     "title": driver.title,
#                     "header_menu": [],
#                     "sections": []
#                 },
#                 "other_pages": []
#             },
#             "global_links": [],
#             "contact_information": {
#                 "email": "",
#                 "phone": "",
#                 "fax": "",
#                 "address": ""
#             },
#             "downloads": []
#         }

#         # Get header menu items - updated selector
#         try:
#             menu_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "nav a, .menu a, .navigation a")))
#             for item in menu_items:
#                 if item.is_displayed() and item.text.strip():
#                     site_data["site_overview"]["homepage"]["header_menu"].append({
#                         "menu_item": item.text.strip(),
#                         "link": item.get_attribute("href")
#                     })
#         except:
#             print("Warning: Could not find main navigation menu")

#         # Get main sections - updated selector
#         try:
#             main_content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "main, .main-content, #main, article, .content")))
#             main_sections = main_content.find_elements(By.CSS_SELECTOR, "section, div[class*='section'], div[class*='content']")

#             if not main_sections:  # If no sections found, treat main content as one section
#                 site_data["site_overview"]["homepage"]["sections"].append(scrape_section(main_content))
#             else:
#                 for section in main_sections:
#                     site_data["site_overview"]["homepage"]["sections"].append(scrape_section(section))
#         except:
#             print("Warning: Could not find main content sections")

#         # Get global links
#         try:
#             global_links = driver.find_elements(By.CSS_SELECTOR, "footer a, .footer a")
#             for link in global_links:
#                 if link.is_displayed() and link.get_attribute("href"):
#                     site_data["global_links"].append({
#                         "link_text": link.text.strip(),
#                         "url": link.get_attribute("href")
#                     })
#         except:
#             print("Warning: Could not find global links")

#         # Get contact information
#         try:
#             contact_elements = driver.find_elements(By.CSS_SELECTOR,
#                 "footer, .footer, [class*='contact'], [id*='contact']")
#             contact_text = " ".join([elem.text for elem in contact_elements])

#             email_match = re.search(r'[\w\.-]+@[\w\.-]+', contact_text)
#             phone_match = re.search(r'(?:Phone|Tel|T)[\s:]+([+\d\s-]+)', contact_text, re.IGNORECASE)
#             fax_match = re.search(r'(?:Fax|F)[\s:]+([+\d\s-]+)', contact_text, re.IGNORECASE)

#             site_data["contact_information"].update({
#                 "email": email_match.group(0) if email_match else "",
#                 "phone": phone_match.group(1).strip() if phone_match else "",
#                 "fax": fax_match.group(1).strip() if fax_match else "",
#                 "address": contact_text.split('\n')[0] if '\n' in contact_text else ""
#             })
#         except:
#             print("Warning: Could not find contact information")

#         # Get downloads
#         try:
#             download_links = driver.find_elements(By.CSS_SELECTOR,
#                 "a[href$='.pdf'], a[href$='.doc'], a[href$='.docx'], a[href$='.xls'], a[href$='.xlsx']")
#             for link in download_links:
#                 if link.is_displayed():
#                     site_data["downloads"].append(get_file_details(link))
#         except:
#             print("Warning: Could not find downloads")

#         return site_data

#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     try:
#         site_data = scrape_website()
#         # Save to JSON file
#         with open('cfr_gov_mt_data.json', 'w', encoding='utf-8') as f:
#             json.dump(site_data, f, indent=2, ensure_ascii=False)
#         print("Scraping completed. Data saved to cfr_gov_mt_data.json")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

#claudia works 2

# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import json
# import re
# import time
# from urllib.parse import urljoin, urlparse

# def get_file_details(link_element):
#     """Extract file details from download links"""
#     href = link_element.get_attribute('href') or ""
#     file_name = link_element.text.strip() or href.split('/')[-1]
#     file_type = href.split('.')[-1] if '.' in href else "Unknown"
#     return {
#         "file_name": file_name,
#         "file_type": file_type,
#         "file_size": "N/A",
#         "link": href
#     }

# def is_valid_url(url, base_domain):
#     """Check if URL is valid and belongs to the same domain"""
#     if not url:
#         return False
#     try:
#         parsed_url = urlparse(url)
#         parsed_base = urlparse(base_domain)
#         return parsed_url.netloc == parsed_base.netloc and not url.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx'))
#     except:
#         return False

# def scrape_page_content(driver, wait, url, visited_urls):
#     """Scrape content from a single page"""
#     if url in visited_urls:
#         return None

#     visited_urls.add(url)
#     print(f"Scraping page: {url}")

#     try:
#         driver.get(url)
#         time.sleep(3)  # Allow time for JavaScript to load

#         page_data = {
#             "url": url,
#             "title": driver.title,
#             "content_sections": [],
#             "sub_pages": [],
#             "downloads": []
#         }

#         # Get main content sections
#         try:
#             main_content = wait.until(EC.presence_of_element_located((
#                 By.CSS_SELECTOR, "main, .main-content, #main, article, .content, body")))

#             sections = main_content.find_elements(
#                 By.CSS_SELECTOR, "section, div[class*='section'], div[class*='content'], div[role='main']")

#             if not sections:
#                 sections = [main_content]

#             for section in sections:
#                 section_data = {
#                     "title": "",
#                     "text_content": "",
#                     "links": []
#                 }

#                 # Try to find section title
#                 try:
#                     title_elem = section.find_element(
#                         By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")
#                     section_data["title"] = title_elem.text.strip()
#                 except:
#                     pass

#                 # Get section content
#                 section_data["text_content"] = section.text.strip()

#                 # Get links within section
#                 links = section.find_elements(By.TAG_NAME, "a")
#                 for link in links:
#                     href = link.get_attribute("href")
#                     if href:
#                         section_data["links"].append({
#                             "text": link.text.strip(),
#                             "url": href
#                         })

#                 page_data["content_sections"].append(section_data)

#         except Exception as e:
#             print(f"Error scraping sections: {str(e)}")

#         # Get downloads
#         try:
#             download_links = driver.find_elements(
#                 By.CSS_SELECTOR, "a[href$='.pdf'], a[href$='.doc'], a[href$='.docx'], a[href$='.xls'], a[href$='.xlsx']")
#             for link in download_links:
#                 if link.is_displayed():
#                     page_data["downloads"].append(get_file_details(link))
#         except Exception as e:
#             print(f"Error scraping downloads: {str(e)}")

#         return page_data

#     except Exception as e:
#         print(f"Error scraping page {url}: {str(e)}")
#         return None

# def scrape_website():
#     options = Options()
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
#     options.add_argument('--headless')

#     driver = Chrome(options=options)
#     wait = WebDriverWait(driver, 20)

#     try:
#         base_url = "https://cfr.gov.mt/en/Pages/Home.aspx"
#         visited_urls = set()
#         urls_to_visit = {base_url}

#         site_data = {
#             "base_url": base_url,
#             "main_pages": [],
#             "contact_information": {
#                 "email": "",
#                 "phone": "",
#                 "fax": "",
#                 "address": ""
#             }
#         }

#         while urls_to_visit:
#             current_url = urls_to_visit.pop()
#             page_data = scrape_page_content(driver, wait, current_url, visited_urls)

#             if page_data:
#                 site_data["main_pages"].append(page_data)

#                 # Add new URLs to visit
#                 for section in page_data["content_sections"]:
#                     for link in section["links"]:
#                         url = link["url"]
#                         if is_valid_url(url, base_url) and url not in visited_urls:
#                             urls_to_visit.add(url)

#         # Extract contact information from all pages
#         contact_text = ""
#         for page in site_data["main_pages"]:
#             for section in page["content_sections"]:
#                 contact_text += section["text_content"] + " "

#         # Parse contact information
#         email_match = re.search(r'[\w\.-]+@[\w\.-]+', contact_text)
#         phone_match = re.search(r'(?:Phone|Tel|T)[\s:]+([+\d\s-]+)', contact_text, re.IGNORECASE)
#         fax_match = re.search(r'(?:Fax|F)[\s:]+([+\d\s-]+)', contact_text, re.IGNORECASE)
#         address_match = re.search(r'(?:Address|Location)[\s:]+([^\n]+)', contact_text, re.IGNORECASE)

#         site_data["contact_information"].update({
#             "email": email_match.group(0) if email_match else "",
#             "phone": phone_match.group(1).strip() if phone_match else "",
#             "fax": fax_match.group(1).strip() if fax_match else "",
#             "address": address_match.group(1).strip() if address_match else ""
#         })

#         return site_data

#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     try:
#         site_data = scrape_website()
#         # Save to JSON file
#         with open('cfr_gov_mt_data.json', 'w', encoding='utf-8') as f:
#             json.dump(site_data, f, indent=2, ensure_ascii=False)
#         print("Scraping completed. Data saved to cfr_gov_mt_data.json")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

#claudia works 3 # we got 12 pages from this code

# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import json
# import re
# import time
# import random
# from urllib.parse import urljoin, urlparse

# def get_file_details(link_element):
#     """Extract file details from download links"""
#     href = link_element.get_attribute('href') or ""
#     file_name = link_element.text.strip() or href.split('/')[-1]
#     file_type = href.split('.')[-1] if '.' in href else "Unknown"
#     return {
#         "file_name": file_name,
#         "file_type": file_type,
#         "file_size": "N/A",
#         "link": href
#     }

# def is_valid_url(url, base_domain):
#     """Check if URL is valid and belongs to the same domain"""
#     if not url:
#         return False
#     try:
#         parsed_url = urlparse(url)
#         parsed_base = urlparse(base_domain)
#         return parsed_url.netloc == parsed_base.netloc and not url.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx'))
#     except:
#         return False

# def random_delay():
#     """Add random delay between requests"""
#     time.sleep(random.uniform(2, 4))

# def scrape_page_content(driver, wait, url, visited_urls, retry_count=0):
#     """Scrape content from a single page"""
#     if url in visited_urls or retry_count >= 3:
#         return None

#     visited_urls.add(url)
#     print(f"Scraping page: {url}")

#     try:
#         driver.get(url)
#         random_delay()

#         page_data = {
#             "url": url,
#             "title": driver.title,
#             "content_sections": [],
#             "downloads": []
#         }

#         # Get main content
#         try:
#             # Wait for any main content to load
#             wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

#             # Get all visible text content
#             elements = driver.find_elements(By.XPATH, "//*[normalize-space(text())][not(self::script)][not(self::style)]")

#             current_section = {
#                 "title": "",
#                 "text_content": "",
#                 "links": []
#             }

#             for element in elements:
#                 if element.tag_name.startswith('h'):
#                     # If we find a header, start a new section
#                     if current_section["text_content"] or current_section["links"]:
#                         page_data["content_sections"].append(current_section.copy())
#                     current_section = {
#                         "title": element.text.strip(),
#                         "text_content": "",
#                         "links": []
#                     }
#                 else:
#                     # Add text content
#                     text = element.text.strip()
#                     if text:
#                         current_section["text_content"] += text + "\n"

#                     # Check for links within this element
#                     links = element.find_elements(By.TAG_NAME, "a")
#                     for link in links:
#                         href = link.get_attribute("href")
#                         if href:
#                             current_section["links"].append({
#                                 "text": link.text.strip(),
#                                 "url": href
#                             })

#             # Add the last section if it has content
#             if current_section["text_content"] or current_section["links"]:
#                 page_data["content_sections"].append(current_section)

#             # Get downloads
#             download_links = driver.find_elements(
#                 By.CSS_SELECTOR, "a[href$='.pdf'], a[href$='.doc'], a[href$='.docx'], a[href$='.xls'], a[href$='.xlsx']")
#             for link in download_links:
#                 page_data["downloads"].append(get_file_details(link))

#         except Exception as e:
#             print(f"Error extracting content: {str(e)}")

#         return page_data

#     except Exception as e:
#         print(f"Error accessing page {url}: {str(e)}")
#         if retry_count < 3:
#             print(f"Retrying {url}...")
#             random_delay()
#             return scrape_page_content(driver, wait, url, visited_urls, retry_count + 1)
#         return None

# def scrape_website():
#     # Configure undetected-chromedriver
#     options = uc.ChromeOptions()
#     options.add_argument('--disable-gpu')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-notifications')

#     driver = uc.Chrome(options=options)
#     wait = WebDriverWait(driver, 20)

#     try:
#         base_url = "https://cfr.gov.mt/en/Pages/Home.aspx"
#         visited_urls = set()
#         urls_to_visit = {base_url}
#         max_pages = 50  # Limit number of pages to scrape

#         site_data = {
#             "base_url": base_url,
#             "main_pages": [],
#             "contact_information": {
#                 "email": "",
#                 "phone": "",
#                 "fax": "",
#                 "address": ""
#             }
#         }

#         page_count = 0

#         while urls_to_visit and page_count < max_pages:
#             current_url = urls_to_visit.pop()
#             page_data = scrape_page_content(driver, wait, current_url, visited_urls)

#             if page_data:
#                 site_data["main_pages"].append(page_data)
#                 page_count += 1
#                 print(f"Successfully scraped page {page_count} of {max_pages}")

#                 # Add new URLs to visit
#                 for section in page_data["content_sections"]:
#                     for link in section["links"]:
#                         url = link["url"]
#                         if is_valid_url(url, base_url) and url not in visited_urls:
#                             urls_to_visit.add(url)

#                 # Extract contact information
#                 contact_text = " ".join([section["text_content"] for section in page_data["content_sections"]])

#                 email_match = re.search(r'[\w\.-]+@[\w\.-]+', contact_text)
#                 phone_match = re.search(r'(?:Phone|Tel|T)[\s:]+([+\d\s-]+)', contact_text, re.IGNORECASE)
#                 fax_match = re.search(r'(?:Fax|F)[\s:]+([+\d\s-]+)', contact_text, re.IGNORECASE)
#                 address_match = re.search(r'Address:?\s*([^\n]+)', contact_text, re.IGNORECASE)

#                 if email_match and not site_data["contact_information"]["email"]:
#                     site_data["contact_information"]["email"] = email_match.group(0)
#                 if phone_match and not site_data["contact_information"]["phone"]:
#                     site_data["contact_information"]["phone"] = phone_match.group(1).strip()
#                 if fax_match and not site_data["contact_information"]["fax"]:
#                     site_data["contact_information"]["fax"] = fax_match.group(1).strip()
#                 if address_match and not site_data["contact_information"]["address"]:
#                     site_data["contact_information"]["address"] = address_match.group(1).strip()

#             random_delay()

#         return site_data

#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     try:
#         site_data = scrape_website()
#         with open('cfr_gov_mt_data.json', 'w', encoding='utf-8') as f:
#             json.dump(site_data, f, indent=2, ensure_ascii=False)
#         print("Scraping completed. Data saved to cfr_gov_mt_data.json")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

#claudia works 4

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