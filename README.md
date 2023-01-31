# cfc-insight
cfc-insight-technical-challenge


# Solutions
All scripts written in Python 3.10.6

Install dependencies: json, collections, re are included in python standard library.  
`pip install -r requirements.txt`

Running script:  
`python3 cfc_web_scrape.py`

Output:
External sources JSON format. **Note that images are included but are all hosted on cfcunderwriting.com**  
```
[
    {
        'type':'images'
        'src': 'src'
    },
    {
        'type':'scripts'
        'src': 'src'
    },
]
```


Word frequency count JSON format:  
```
[
    {
        'term':'privacy'
        'count': 11
    },
]
```

# The Challenge
Produce a program that:
1. Scrape the index webpage hosted at `cfcunderwriting.com`
2. Writes a list of *all externally loaded resources* (e.g. images/scripts/fonts not hosted
on cfcunderwriting.com) to a JSON output file.
3. Enumerates the page's hyperlinks and identifies the location of the "Privacy Policy"
page
4. Use the privacy policy URL identified in step 3 and scrape the pages content.
Produce a case-insensitive word frequency count for all of the visible text