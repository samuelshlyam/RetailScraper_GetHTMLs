import json
import os
from urllib.parse import urlparse
class FilterURLS:
    def filter_urls(self, urls, brand_settings, whitelisted_domains):
        variation=urls.get("Variation")
        unfiltered_urls=urls.get("Unfiltered URLs")
        brand_domains = [domain.replace('www.', '') for domain in brand_settings.get("domain_hierarchy", [])]
        whitelisted_domains = [domain.replace('www.', '') for domain in whitelisted_domains]
        filtered_urls=[]
        if isinstance(unfiltered_urls, str):
            unfiltered_urls = unfiltered_urls.split(',')

        for url in unfiltered_urls:
            url = str(url).strip()
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url

            try:
                parsed_url = urlparse(url)
                domain = parsed_url.netloc
                if domain.startswith('www.'):
                    domain = domain[4:]
                print(f"Domain: {domain}")
                if domain in brand_domains:
                    filtered_urls.append({"Variation":variation,"URL":url, "Level":"brand"})
                elif domain in whitelisted_domains:
                    filtered_urls.append({"Variation":variation,"URL":url, "Level":"whitelist"})
                elif 'modesens' in domain:
                    filtered_urls.append({"Variation":variation,"URL":url, "Level":"modesens"})
                else:
                    filtered_urls.append({"Variation":variation,"URL":url, "Level":"unapproved"})
            except Exception as e:
                print(f"Error parsing URL '{url}': {e}")
        return filtered_urls

    def filter_urls_by_currency(self, currency_items, sorted_input):
        filtered_output=[]
        for input in sorted_input:
            url=input.get("URL","")
            input["Currency"]="Wrong Currency"
            for item in currency_items:
                # print(f'item: {item} url: {url}')
                # print(f'item: {type(item)} url: {type(url)}')
                # print(url)
                if str(item.lower()) in str(url).lower():
                    print(f"item: {item} url: {url}")
                    input["Currency"]="Correct Currency"
                    break
            filtered_output.append(input)

        return filtered_output

    def sortURLs(self,filtered_input):
        flattened = []
        for sublist in filtered_input:
            flattened.extend(sublist)

        url_map = {}
        for entry in flattened:
            url = entry.get("URL", "").strip()
            variation = entry.get("Variation", "").strip()
            level = entry.get("Level", "").strip()

            if not url:
                continue

            if url not in url_map:
                url_map[url] = {
                    "URL": url,
                    "Variations": set(),
                    "Level": level,
                }

            url_map[url]["Variations"].add(variation)

        result = []
        for url_info in url_map.values():
            result.append({
                "URL": url_info["URL"],
                "Variations": sorted(url_info["Variations"]),
                "Level": url_info["Level"],
            })
        level_priority = {
            "brand": 0,
            "whitelist": 1,
            "modesens": 2,
            "unapproved": 3
        }
        def get_min_priority(level):
            return level_priority.get(level, 999)
        result.sort(key=lambda item: get_min_priority(item["Level"]))
        return result

class BrandSettings:
    def __init__(self, settings):
        self.settings = settings

    def get_rules_for_brand(self, brand_name):
        for rule in self.settings['brand_rules']:
            if str(brand_name).lower() in str(rule['names']).lower():
                return rule
        return None


#Test Filter and Sorting
#Manager 2 Sorts and filters URL's
current_directory=os.getcwd()
brand_settings_directory=os.path.join(current_directory,"brand_settings.json")
currency_settings_directory=os.path.join(current_directory,"currency_filter_settings.json")
brand_settings = json.loads(open(brand_settings_directory).read())
brand_settings = BrandSettings(brand_settings)
currency_settings=json.loads(open(currency_settings_directory).read())
currency_items=currency_settings["US"]
test_settings=brand_settings.get_rules_for_brand("Givenchy")
input=[{'Variation': 'BB50V.9B1UC 105', 'Search Query': '"BB50V.9B1UC 105" GIV', 'Unfiltered URLs': ['http://www.hadabima.gov.lk/index.php/si/aecjbrshop/co/p/voyou-medium-shopper-bag-givenchy-bag-1652078']}, {'Variation': 'BB50V.9B1UC 105', 'Search Query': '"BB50V.9B1UC 105" Givenchy', 'Unfiltered URLs': ['http://www.jecr.org/eadjbrshop/pr/p/voyou-medium-shopper-bag-givenchy-bag-1652078', 'http://www.anatomia.fmed.edu.uy/bcejbjshop/hk/p/voyou-medium-shopper-bag-givenchy-bag-1652078', 'https://tgkb5.ru/index.php/ecfjbtshop/uy/p/voyou-medium-shopper-bag-givenchy-bag-1652078', 'http://www.anatomia.fmed.edu.uy/bcejbjshop/mz/p/voyou-medium-shopper-bag-givenchy-bag-1652078']}, {'Variation': 'BB50V.9B1UC 105', 'Search Query': '"BB50V.9B1UC 105" GIVENCHY', 'Unfiltered URLs': ['http://www.jecr.org/eadjbrshop/pr/p/voyou-medium-shopper-bag-givenchy-bag-1652078', 'http://www.anatomia.fmed.edu.uy/bcejbjshop/hk/p/voyou-medium-shopper-bag-givenchy-bag-1652078', 'https://tgkb5.ru/index.php/ecfjbtshop/uy/p/voyou-medium-shopper-bag-givenchy-bag-1652078', 'http://www.anatomia.fmed.edu.uy/bcejbjshop/mz/p/voyou-medium-shopper-bag-givenchy-bag-1652078']}, {'Variation': 'BB50V.9B1UC 105', 'Search Query': '"BB50V.9B1UC 105"', 'Unfiltered URLs': ['http://www.jecr.org/eadjbrshop/pr/p/voyou-medium-shopper-bag-givenchy-bag-1652078', 'http://www.anatomia.fmed.edu.uy/bcejbjshop/mz/p/voyou-medium-shopper-bag-givenchy-bag-1652078', 'https://tgkb5.ru/index.php/ecfjbtshop/uy/p/voyou-medium-shopper-bag-givenchy-bag-1652078', 'http://www.anatomia.fmed.edu.uy/bcejbjshop/hk/p/voyou-medium-shopper-bag-givenchy-bag-1652078']}]
whitelisted_domains = [
        "fwrd.com",
        "saksfifthavenue.com",
        "saksoff5th.com",
        "nordstrom.com",
        "nordstromrack.com"
    ]
test_Filter=FilterURLS()
filtered_input=[]
for URLs in input:
    filtered_urls=test_Filter.filter_urls(URLs,test_settings,whitelisted_domains)
    filtered_input.append(filtered_urls)
print(filtered_input)
sorted_input=test_Filter.sortURLs(filtered_input)
print(sorted_input)
final_output=test_Filter.filter_urls_by_currency(currency_items,sorted_input)
print(final_output)
