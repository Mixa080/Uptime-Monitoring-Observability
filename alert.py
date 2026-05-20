from database import get_last_results, get_all_urls

def check_alerts():
    urls = get_all_urls()
    for url in urls:
        results = get_last_results(url, 3)
        if len(results) == 3:
            all_down = all(res[0] == 0 or res[0] >= 400 for res in results)
            if all_down:
                print(f"[CRITICAL ALERT] {url} is DOWN for the last 3 checks!")

if __name__ == "__main__":
    check_alerts()
