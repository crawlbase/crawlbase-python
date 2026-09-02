# Crawlbase API Python class

A lightweight, dependency free Python class that acts as wrapper for Crawlbase API.

## Installing

Choose a way of installing:

- Download the python class from Github.
- Or use [PyPi](https://pypi.org/project/crawlbase/) Python package manager. `pip install crawlbase`

Then import the CrawlingAPI, ScraperAPI, etc as needed.

```python
from crawlbase import CrawlingAPI, ScraperAPI, LeadsAPI, ScreenshotsAPI, StorageAPI
```

## Crawling API

First initialize the CrawlingAPI class.

```python
api = CrawlingAPI({ 'token': 'YOUR_CRAWLBASE_TOKEN' })
```

### GET requests

Pass the url that you want to scrape plus any options from the ones available in the [API documentation](https://crawlbase.com/docs).

```python
api.get(url, options = {})
```

Example:

```python
response = api.get('https://www.facebook.com/britneyspears')
if response['status_code'] == 200:
    print(response['body'])
```

You can pass any options from Crawlbase API.

Example:

```python
response = api.get('https://www.reddit.com/r/pics/comments/5bx4bx/thanks_obama/', {
    'user_agent': 'Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/30.0',
    'format': 'json'
})
if response['status_code'] == 200:
    print(response['body'])
```

### POST requests

Pass the url that you want to scrape, the data that you want to send which can be either a json or a string, plus any options from the ones available in the [API documentation](https://crawlbase.com/docs).

```python
api.post(url, dictionary or string data, options = {})
```

Example:

```python
response = api.post('https://producthunt.com/search', { 'text': 'example search' })
if response['status_code'] == 200:
    print(response['body'])
```

You can send the data as `application/json` instead of `x-www-form-urlencoded` by setting option `post_content_type` as json.

```python
import json
response = api.post('https://httpbin.org/post', json.dumps({ 'some_json': 'with some value' }), { 'post_content_type': 'json' })
if response['status_code'] == 200:
    print(response['body'])
```

### Javascript requests

If you need to scrape any website built with Javascript like React, Angular, Vue, etc. You just need to pass your javascript token and use the same calls. Note that only `.get` is available for javascript and not `.post`.

```python
api = CrawlingAPI({ 'token': 'YOUR_JAVASCRIPT_TOKEN' })
```

```python
response = api.get('https://www.nfl.com')
if response['status_code'] == 200:
    print(response['body'])
```

Same way you can pass javascript additional options.

```python
response = api.get('https://www.freelancer.com', { 'page_wait': 5000 })
if response['status_code'] == 200:
    print(response['body'])
```

## Original status

You can always get the original status and Crawlbase status from the response. Read the [Crawlbase documentation](https://crawlbase.com/docs) to learn more about those status.

`cb_status` is the preferred Crawlbase status field. The library reads `cb_status` from the API when present, and falls back to `pc_status` otherwise. Both keys are set on `response['headers']` to the resolved value.

```python
response = api.get('https://craiglist.com')
print(response['headers']['original_status'])
print(response['headers']['cb_status'])
```

### Migration from `pc_status`

`pc_status` is deprecated but still supported temporarily for backward compatibility. Prefer `cb_status` in new code:

```python
# Deprecated (still works temporarily)
print(response['headers']['pc_status'])

# Preferred
print(response['headers']['cb_status'])
```

If you have questions or need help using the library, please open an issue or [contact us](https://crawlbase.com/contact).

## Scraper API

> ⚠️ **Deprecated.** The standalone Scraper API has been closed to new sign-ups since October 1, 2024. Existing integrations continue to work and no shutdown is scheduled, but new code should use the Crawling API with the `scraper` parameter instead (same scrapers, simpler endpoint, more parameters). The class below stays available for backward compatibility. See the [scrapers documentation](https://crawlbase.com/docs/scrapers).

The usage of the Scraper API is very similar, just change the class name to initialize.

```python
scraper_api = ScraperAPI({ 'token': 'YOUR_NORMAL_TOKEN' })

response = scraper_api.get('https://www.amazon.com/DualSense-Wireless-Controller-PlayStation-5/dp/B08FC6C75Y/')
if response['status_code'] == 200:
    print(response['json']['name']) # Will print the name of the Amazon product
```

## Leads API

> ⚠️ **Deprecated.** The Leads API has been closed to new sign-ups since October 1, 2024. Existing integrations continue to work and no shutdown is scheduled. There is no direct replacement; for similar workflows use the Crawling API with the [`email-extractor`](https://crawlbase.com/docs/scrapers/email-extractor) scraper (any URL → emails) or the [`google-serp`](https://crawlbase.com/docs/scrapers/google-serp) scraper for domain-scoped contact discovery. The class below stays available for backward compatibility.

To find email leads you can use the leads API, you can check the full [API documentation](https://crawlbase.com/docs/leads-api/) if needed.

```python
leads_api = LeadsAPI({ 'token': 'YOUR_NORMAL_TOKEN' })

response = leads_api.get_from_domain('microsoft.com')

if response['status_code'] == 200:
    print(response['json']['leads'])
```

## Screenshots API

> ⚠️ **Deprecated.** The standalone Screenshots API has been closed to new sign-ups since November 1, 2024. Existing integrations continue to work and no shutdown is scheduled, but new code should use the Crawling API with the `screenshot=true` parameter — same JS-rendering pipeline, screenshot parameters on the standard endpoint. The class below stays available for backward compatibility. See the [Crawling API screenshots section](https://crawlbase.com/docs/crawling-api#screenshots).

Initialize with your Screenshots API token and call the `get` method.

```python
screenshots_api = ScreenshotsAPI({ 'token': 'YOUR_NORMAL_TOKEN' })
response = screenshots_api.get('https://www.apple.com')
if response['status_code'] == 200:
    print(response['headers']['success'])
    print(response['headers']['url'])
    print(response['headers']['remaining_requests'])
    print(response['file'])
```

or specifying a file path

```python
screenshots_api = ScreenshotsAPI({ 'token': 'YOUR_NORMAL_TOKEN' })
response = screenshots_api.get('https://www.apple.com', { 'save_to_path': 'apple.jpg' })
if response['status_code'] == 200:
    print(response['headers']['success'])
    print(response['headers']['url'])
    print(response['headers']['remaining_requests'])
    print(response['file'])
```

or if you set `store=true` then `screenshot_url` is set in the returned headers 

```python
screenshots_api = ScreenshotsAPI({ 'token': 'YOUR_NORMAL_TOKEN' })
response = screenshots_api.get('https://www.apple.com', { 'store': 'true' })
if response['status_code'] == 200:
    print(response['headers']['success'])
    print(response['headers']['url'])
    print(response['headers']['remaining_requests'])
    print(response['file'])
    print(response['headers']['screenshot_url'])
```

Note that `screenshots_api.get(url, options)` method accepts an [options](https://crawlbase.com/docs/screenshots-api/parameters)

## Smart AI Proxy usage

The [Smart AI Proxy](https://crawlbase.com/docs/smart-proxy) is a standard rotating HTTP(S) proxy endpoint, so it needs no SDK: point any HTTP client at `smartproxy.crawlbase.com:8012` (HTTP) or `smartproxy.crawlbase.com:8013` (HTTPS) with your token as the proxy username and an empty password. Crawlbase handles proxy rotation, retries and anti-bot bypass on its side.

```python
import requests

proxies = {
    'http':  'http://YOUR_TOKEN:@smartproxy.crawlbase.com:8012',
    'https': 'https://YOUR_TOKEN:@smartproxy.crawlbase.com:8013',
}
res = requests.get('https://httpbin.org/ip', proxies=proxies, verify=False)
print(res.text)
```

Note: the proxy re-signs HTTPS traffic, so certificate verification must be disabled on the client (as in the example). See the [Smart AI Proxy documentation](https://crawlbase.com/docs/smart-proxy) for all options.

## Storage API

Initialize the Storage API using your private token.

```python
storage_api = StorageAPI({ 'token': 'YOUR_NORMAL_TOKEN' })
```

Pass the [url](https://crawlbase.com/docs/storage-api/parameters/#url) that you want to get from [Crawlbase Storage](https://crawlbase.com/dashboard/storage).

```python
response = storage_api.get('https://www.apple.com')
if response['status_code'] == 200:
    print(response['headers']['original_status'])
    print(response['headers']['cb_status'])
    print(response['headers']['url'])
    print(response['headers']['rid'])
    print(response['headers']['stored_at'])
    print(response['body'])
```

or you can use the [RID](https://crawlbase.com/docs/storage-api/parameters/#rid)

```python
response = storage_api.get('RID_REPLACE')
if response['status_code'] == 200:
    print(response['headers']['original_status'])
    print(response['headers']['cb_status'])
    print(response['headers']['url'])
    print(response['headers']['rid'])
    print(response['headers']['stored_at'])
    print(response['body'])
```

Note: One of the two RID or URL must be sent. So both are optional but it's mandatory to send one of the two.

### [Delete](https://crawlbase.com/docs/storage-api/delete/) request

To delete a storage item from your storage area, use the correct RID

```python
if storage_api.delete('RID_REPLACE'):
  print('delete success')
else:
  print('Unable to delete')
```

### [Bulk](https://crawlbase.com/docs/storage-api/bulk/) request

To do a bulk request with a list of RIDs, please send the list of rids as an array

```python
response = storage_api.bulk(['RID1', 'RID2', 'RID3', ...])
if response['status_code'] == 200:
    for item in response['json']:
        print(item['original_status'])
        # Bulk items use API payload keys; prefer cb_status, fall back to pc_status
        print(item.get('cb_status', item.get('pc_status')))
        print(item['url'])
        print(item['rid'])
        print(item['stored_at'])
        print(item['body'])
```

### [RIDs](https://crawlbase.com/docs/storage-api/rids) request

To request a bulk list of RIDs from your storage area

```python
rids = storage_api.rids()
print(rids)
```

You can also specify a limit as a parameter

```python
storage_api.rids(100)
```

### [Total Count](https://crawlbase.com/docs/storage-api/total_count)

To get the total number of documents in your storage area

```python
total_count = storage_api.totalCount()
print(total_count)
```

## Custom timeout

If you need to use a custom timeout, you can pass it to the class instance creation like the following:

```python
api = CrawlingAPI({ 'token': 'TOKEN', 'timeout': 120 })
```

Timeout is in seconds.

---

Copyright 2026 Crawlbase
