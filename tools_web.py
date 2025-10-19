from smolagents import tool
from helium import start_chrome, go_to, click, write, get_driver
from selenium.webdriver import ChromeOptions
import arxiv
import json

@tool
def browser_automate(url: str, actions: str = "") -> str:
    """
    Perform headless browser tasks. Actions are semi-colon separated.
    Example: 'write username to #user; write password to #pass; click Login Button'
    """
    driver = None
    try:
        opts = ChromeOptions()
        opts.add_argument("--headless=new")
        driver = start_chrome(headless=True, options=opts)
        go_to(url)

        if actions:
            for act in actions.split(";"):
                act = act.strip()
                if not act:
                    continue
                if "click" in act:
                    target = act.replace("click", "").strip()
                    click(target)
                elif "write" in act:
                    parts = act.replace("write", "").split(" to ", 1)
                    if len(parts) == 2:
                        text, target = parts
                        write(text.strip(), to=target.strip())

        # Give a moment for any async actions to complete
        import time
        time.sleep(2)

        page_title = get_driver().title
        return f"Browser automation complete. Final page title: '{page_title}'"

    except Exception as e:
        return f"Browser automation failed: {str(e)}"
    finally:
        if driver:
            driver.quit()

@tool
def arxiv_search(query: str, max_results: int = 5) -> str:
    """Searches for research papers on Arxiv and returns a JSON string of the results."""
    try:
        search = arxiv.Search(query=query, max_results=max_results)
        results = []
        for result in search.results():
            results.append({
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary[:500] + '...', # Truncate for brevity
                "published": result.published.strftime("%Y-%m-%d"),
                "pdf_url": result.pdf_url
            })
        if not results:
            return "No papers found for the given query."
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error searching Arxiv: {str(e)}"
