from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import requests


def test_proxy(proxy):
    # print(f"testing proxy: {proxy["ip"]}:{proxy["port"]}")
    try:
        # for protocol in protocols:
        proxies = {
            "http": f"{proxy["protocol"]}://{proxy["ip"]}:{proxy["port"]}",
            "https": f"{proxy["protocol"]}://{proxy["ip"]}:{proxy["port"]}",
        }
        # print("waiting ", proxy["timeout"], " seconds")
        res = requests.get(
            "https://httpbin.org/ip", proxies=proxies, timeout=proxy["timeout"]
        )

        res.raise_for_status()
        print(res.json())
        return True
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        exit()
    except Exception as e:
        # print("Not working proxy")
        pass


# def run(driver, options):
#     options.add_argument(f"--proxy-server=http://{proxy['ip']}:{proxy['port']}")
#     driver.get("https://cfr.gov.mt/en/Pages/Home.aspx")
#     print(driver.title)
#     driver.quit()


# res = requests.get(
#     "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
# )

res = requests.get(
    "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=json"
)

proxies = res.json()["proxies"]

if proxies:
    ua = UserAgent().random
    options = Options()
    # options.add_argument("--headless")
    options.add_argument(f"user-agent={ua}")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    print("Finding working proxy...")
    for proxy in proxies:
        if test_proxy(proxy):
            options.add_argument(f"--proxy-server=http://{proxy["ip"]}:{proxy["port"]}")
            driver = Chrome(options=options)
            print("Starting...")

            driver.get("https://cfr.gov.mt/en/Pages/Home.aspx")
            print(driver.title)

            driver.quit()
            break
