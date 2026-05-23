from playwright.sync_api import Page, TimeoutError

class BasePage:
    """
    Base Page Object containing common element interaction methods.
    Supports locator fallbacks to handle dynamic UI updates.
    """
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigates to a specific URL."""
        print(f"[BASE PAGE] Navigating to: {url}")
        self.page.goto(url)

    def wait_for_selector_with_fallback(self, selectors: list, state: str = "visible", timeout: float = 8000) -> str:
        """
        Waits for any of the listed selectors to become ready in the given state.
        Returns the first selector that successfully resolved.
        """
        last_error = None
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first
                locator.wait_for(state=state, timeout=timeout)
                return selector
            except Exception as e:
                last_error = e
        raise TimeoutError(f"None of the selectors in {selectors} reached state '{state}'. Last error: {last_error}")

    def fill_with_fallback(self, selectors: list, text: str, timeout: float = 8000):
        """
        Fills an input field with text, trying multiple alternative locators in order.
        """
        last_error = None
        for selector in selectors:
            try:
                # Wait for the first match of selector to be ready
                locator = self.page.locator(selector).first
                locator.wait_for(state="visible", timeout=timeout)
                # Scroll into view if needed
                locator.scroll_into_view_if_needed()
                # Focus and fill
                locator.focus()
                locator.fill(text)
                print(f"[BASE PAGE] Successfully filled element using: '{selector}'")
                return
            except Exception as e:
                print(f"[BASE PAGE] Selector failed: '{selector}' | Error: {e}. Trying next fallback...")
                last_error = e
        raise Exception(f"Failed to fill element using any of the selectors: {selectors}. Last error: {last_error}")

    def click_with_fallback(self, selectors: list, timeout: float = 8000):
        """
        Clicks an element, trying multiple alternative locators in order.
        """
        last_error = None
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first
                locator.wait_for(state="visible", timeout=timeout)
                locator.scroll_into_view_if_needed()
                locator.click()
                print(f"[BASE PAGE] Successfully clicked element using: '{selector}'")
                return
            except Exception as e:
                print(f"[BASE PAGE] Selector failed: '{selector}' | Error: {e}. Trying next fallback...")
                last_error = e
        raise Exception(f"Failed to click element using any of the selectors: {selectors}. Last error: {last_error}")

    def get_text_with_fallback(self, selectors: list, timeout: float = 8000) -> str:
        """
        Retrieves the inner text of an element, trying multiple alternative locators.
        Using .first completely avoids Playwright's strict mode violation errors on duplicate elements.
        """
        last_error = None
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first
                locator.wait_for(state="visible", timeout=timeout)
                text = locator.inner_text().strip()
                print(f"[BASE PAGE] Successfully retrieved text using: '{selector}'")
                return text
            except Exception as e:
                print(f"[BASE PAGE] Selector failed: '{selector}' | Error: {e}. Trying next fallback...")
                last_error = e
        raise Exception(f"Failed to get text using any of the selectors: {selectors}. Last error: {last_error}")

    def is_visible_with_fallback(self, selectors: list, timeout: float = 2000) -> bool:
        """
        Checks visibility across alternative selectors. Returns True if any is visible.
        """
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first
                # Wait briefly to check visibility
                locator.wait_for(state="visible", timeout=timeout)
                if locator.is_visible():
                    return True
            except Exception:
                pass
        return False
