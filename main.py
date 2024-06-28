import requests
import random

VALID_STATUSES = [200, 301, 302, 307, 404]

proxies_list = open("rotating_proxies_list.txt", "r").read().strip().split("\n")
unchecked = set(proxies_list[0:10])
working = set()
not_working = set()

session = requests.Session()


def get_random_proxy():
    # create a tuple from unchecked and working sets
    available_proxies = tuple(unchecked.union(working))
    if not available_proxies:
        raise Exception("no proxies available")
    return random.choice(available_proxies)


def reset_proxy(proxy):
    unchecked.add(proxy)
    working.discard(proxy)
    not_working.discard(proxy)


def set_working(proxy):
    unchecked.discard(proxy)
    working.add(proxy)
    not_working.discard(proxy)


def set_not_working(proxy):
    unchecked.discard(proxy)
    working.discard(proxy)
    not_working.add(proxy)


def get(url, proxy=None):
    if not proxy:
        proxy = get_random_proxy()

    try:
        response = session.get(url, proxies={"http": f"http://{proxy}"}, timeout=30)
        if response.status_code in VALID_STATUSES:
            set_working(proxy)
        else:
            set_not_working(proxy)

        return response
    except Exception as e:
        set_not_working(proxy)
        #raise e  # raise exception


def check_proxies():
    
    for proxy in list(unchecked):
        get("http://ident.me/", proxy)


check_proxies()

# print("unchecked ->", unchecked)  # unchecked -> set()
# print("working ->", working)  # working -> {"152.0.209.175:8080", ...}
# print("not_working ->", not_working)  # not_working -> {"167.71.5.83:3128", ...}

# rest of the rotating proxy script

# real scraping part comes here
def main():
    result = get("http://ident.me/")
    print(result.status_code)  # 200
    print(result.text)  # 152.0.209.175


main()
