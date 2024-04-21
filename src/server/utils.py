import hashlib
import datetime
import os
import uuid

def format_arxiv_documents(documents):
    """
    Formats a list of document objects into a list of strings.
    Each document object is assumed to have a 'metadata' dictionary with 'Title' and 'Entry ID',
    and a 'page_content' attribute for content.

    Parameters:
    - documents (list): A list of document objects.

    Returns:
    - list: A list of formatted strings with titles, links, and content snippets.
    """
    formatted_documents = [
        "Title: {title}, Link: {link}, Summary: {snippet}".format(
            title=doc.metadata['Title'],
            link=doc.metadata['Entry ID'],
            snippet=doc.page_content  # Adjust the snippet length as needed
        )
        for doc in documents
    ]
    return formatted_documents

def parse_list_to_dicts(items: list) -> list:
    parsed_items = []
    for item in items:
        # Extract title, link, and summary from each string
        title_start = item.find('Title: ') + len('Title: ')
        link_start = item.find('Link: ') + len('Link: ')
        summary_start = item.find('Summary: ') + len('Summary: ')

        title_end = item.find(', Link: ')
        link_end = item.find(', Summary: ')
        summary_end = len(item)

        title = item[title_start:title_end]
        link = item[link_start:link_end]
        summary = item[summary_start:summary_end]

        # Use the hash_text function for the hash_id
        hash_id = hash_text(link)

        # Construct the dictionary for each item
        parsed_item = {
            "url": link,
            "title": title,
            "hash_id": hash_id,
            "summary": summary
        }
        parsed_items.append(parsed_item)
    return parsed_items

def hash_text(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def format_search_results(search_results):
    """
    Formats a list of dictionaries containing search results into a list of strings.
    Each dictionary is expected to have the keys 'title', 'link', and 'snippet'.

    Parameters:
    - search_results (list): A list of dictionaries, each containing 'title', 'link', and 'snippet'.

    Returns:
    - list: A list of formatted strings based on the search results.
    """
    formatted_results = [
        "Title: {title}, Link: {link}, Summary: {snippet}".format(**i)
        for i in search_results
    ]
    return formatted_results

def format_wiki_summaries(input_text):
    """
    Parses a given text containing page titles and summaries, formats them into a list of strings,
    and appends Wikipedia URLs based on titles.
    
    Parameters:
    - input_text (str): A string containing titles and summaries separated by specific markers.
    
    Returns:
    - list: A list of formatted strings with titles, summaries, and Wikipedia URLs.
    """
    # Splitting the input text into individual records based on double newlines
    records = input_text.split("\n\n")
    
    formatted_records_with_urls = []
    for record in records:
        if "Page:" in record and "Summary:" in record:
            title_line, summary_line = record.split("\n", 1)  # Splitting only on the first newline
            title = title_line.replace("Page: ", "").strip()
            summary = summary_line.replace("Summary: ", "").strip()
            # Replace spaces with underscores for the URL and construct the Wikipedia URL
            url_title = title.replace(" ", "_")
            wikipedia_url = f"https://en.wikipedia.org/wiki/{url_title}"
            # Append formatted string with title, summary, and URL
            formatted_record = "Title: {title}, Link: {wikipedia_url}, Summary: {summary}".format(
                title=title, summary=summary, wikipedia_url=wikipedia_url)
            formatted_records_with_urls.append(formatted_record)
        else:
            print("Record format error, skipping record:", record)
    
    return formatted_records_with_urls