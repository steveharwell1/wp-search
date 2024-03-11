# install
`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

# usage
`source venv/bin/activate`

`cd wp_search`

## Default command example
`scrapy crawl re_search -a expression="vice-president-for-research-and-economic-development" -o 2023-11-08-archive.jl && say "Scan complete"`

## Full page command example
scrapy crawl re_search -a expression="cost-and-aid" -a full_page=true -o 2024-02-23-archive.jl && say "Scan complete"

# help
use https://regex101.com/ for testing regular expression