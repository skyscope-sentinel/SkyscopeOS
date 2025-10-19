from smolagents import tool
from playwright.sync_api import sync_playwright, Page, Browser
import time

class ChromiumBrowser:
    """A dedicated, agent-controlled Chromium browser instance."""

    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser: Browser = self.playwright.chromium.launch(headless=True)
        self.page: Page = self.browser.new_page()

    def go_to(self, url: str) -> str:
        """Navigates to a specific URL."""
        try:
            self.page.goto(url, timeout=60000)
            return f"Successfully navigated to {url}."
        except Exception as e:
            return f"Error navigating to {url}: {str(e)}"

    def click(self, selector: str) -> str:
        """Clicks on an element matching the given selector."""
        try:
            self.page.click(selector, timeout=10000)
            return f"Successfully clicked on '{selector}'."
        except Exception as e:
            return f"Error clicking on '{selector}': {str(e)}"

    def fill(self, selector: str, text: str) -> str:
        """Fills an input field with the given text."""
        try:
            self.page.fill(selector, text, timeout=10000)
            return f"Successfully filled '{selector}' with text."
        except Exception as e:
            return f"Error filling '{selector}': {str(e)}"

    def get_content(self) -> str:
        """Returns the full HTML content of the current page."""
        try:
            return self.page.content()
        except Exception as e:
            return f"Error getting page content: {str(e)}"

    def get_text_content(self) -> str:
        """Returns the user-visible text content of the current page."""
        try:
            return self.page.evaluate("() => document.body.innerText")
        except Exception as e:
            return f"Error getting text content: {str(e)}"

    def close(self):
        """Closes the browser instance."""
        self.browser.close()
        self.playwright.stop()

# --- Tool Interface ---
# We'll manage a single browser instance for the agent's lifecycle.
_browser_instance = None

def get_browser():
    global _browser_instance
    if _browser_instance is None:
        _browser_instance = ChromiumBrowser()
    return _browser_instance

@tool
def web_navigate(url: str) -> str:
    """Navigates the integrated browser to a specific URL."""
    return get_browser().go_to(url)

@tool
def web_click(selector: str) -> str:
    """Clicks on an element in the browser."""
    return get_browser().click(selector)

@tool
def web_fill(selector: str, text: str) -> str:
    """Fills an input field in the browser."""
    return get_browser().fill(selector, text)

@tool
def web_get_text() -> str:
    """Returns the user-visible text of the current page."""
    return get_browser().get_text_content()

@tool
def web_get_html() -> str:
    """Returns the full HTML of the current page."""
    return get_browser().get_content()

# A function to be called at the end of the agent's lifecycle
def shutdown_browser():
    global _browser_instance
    if _browser_instance:
        _browser_instance.close()
        _browser_instance = None
