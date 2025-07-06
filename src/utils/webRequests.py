import requests
from rich import print_json, print
from json import loads
from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout, RequestException
import time

# Custom User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

# Validate proxy by sending request to a simple site
def validate_proxy(proxy):
    try:
        test_url = 'http://httpbin.org/ip'
        response = requests.get(test_url, proxies=proxy, headers=headers, timeout=5)
        return response.status_code == 200
    except:
        return False

# Get proxy from API
def getProxies():
    retry = 0
    try:
        url = 'https://proxylist.geonode.com/api/proxy-list?protocols=socks4&limit=100&page=1&sort_by=lastChecked&sort_type=desc'
        response = requests.get(url, headers=headers, timeout=10)
        data = loads(response.text).get('data', [])
        if retry > len(data):
            return None
    except Exception as e:
        print(f"[red]Failed to fetch proxy list: {e}[/red]")
        return None
    
    for proxy_data in data:
        if retry > len(data):
            return None
        else:
            if not proxy_data:
                return False
            proxies = {
                'http': f'socks4://{proxy_data["ip"]}:{proxy_data["port"]}',
                'https': f'socks4://{proxy_data["ip"]}:{proxy_data["port"]}'
            }

            
            if validate_proxy(proxies):
                print(f"[green]✔ Valid proxy:[/green] {proxies}")
                return (proxies, True)
            else:
                print(f"[yellow]✖ Dead proxy, skipping...[/yellow]")
                retry += 1
                time.sleep(0.5)


class webRequests:
    def __init__(self):
        self.headers = headers
        self.proxies = {}
        self.get_proxies()

    def get_proxies(self):
        proxy, valid = getProxies()
        if valid:
            self.proxies = proxy
            return True
        print("Proxy not found");
        exit()
        
    def get(self, url):
        try:
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10)
            if response.status_code == 200:
                return response
            else:
                print(f"[yellow]Non-200 response: {response.status_code}[/yellow]")
        except ProxyError:
            print("[red]Proxy error: Unable to connect via proxy.[/red]")
        except ConnectTimeout:
                print("[red]Connection timeout: The proxy didn't respond in time.[/red]")
        except ReadTimeout:
            print("[red]Read timeout: Server didn't send data in time.[/red]")
        except RequestException as e:
            print(f"[red]Request failed: {e}[/red]")
        return None

if __name__ == '__main__':
    print("[bold green]Starting request...[/bold green]")
    url = 'http://ip-api.com/json/'
    http = WebReq()
    response = http.get(url)
    if response:
        try:
            print(response.json())
        except Exception as e:
            print(f"[red]Failed to parse JSON response: {e}[/red]")
    else:
        print("[red]All proxies failed.[/red]")
