WEBSITES = [
    {
        "name": "Degewo Search",
        "url": "https://immosuche.degewo.de/de/search",
        "pages": [1, 2, 3,4,5,6],  # Define the pages to scrape
        "params": {
            "size": 10,
            "property_type_id": 1,
            "categories[]": 1,
            "order": "rent_total_without_vat_asc",
        },
        "selectors": {
            "title": ".article__title",  # CSS selector for room titles
            "link_parent": "a"          # Parent tag for the link
        }
    },
     

]
