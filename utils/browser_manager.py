import os
from playwright.sync_api import sync_playwright, Page
from config.global_config import Config

class BrowserManager:
    """
    Utility class to manage Playwright driver instances, contexts, and viewport pages.
    """
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self) -> Page:
        """
        Starts Playwright, launches the browser, and creates context and page.
        """
        print("[BROWSER] Initializing Playwright engine...")
        self.playwright = sync_playwright().start()
        assert self.playwright is not None, "Playwright engine failed to initialize!"
        
        browser_name = Config.BROWSER.lower()
        headless = Config.HEADLESS
        slow_mo = Config.SLOW_MO
        
        print(f"[BROWSER] Launching {browser_name.upper()} (Headless={headless}, SlowMo={slow_mo}ms)...")
        try:
            if browser_name == "firefox":
                self.browser = self.playwright.firefox.launch(headless=headless, slow_mo=slow_mo)
            elif browser_name == "webkit":
                self.browser = self.playwright.webkit.launch(headless=headless, slow_mo=slow_mo)
            else:
                # Default to Chromium
                self.browser = self.playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
        except Exception as e:
            print(f"[ERROR] Failed to launch {browser_name.upper()} browser: {e}")
            raise e
            
        assert self.browser is not None, f"Playwright browser failed to launch! (Type: {browser_name})"
        assert self.browser.is_connected(), f"Browser is not connected!"

        # Set up visual video evidence storage in a temp directory under proof/videos
        video_dir = os.path.join(os.getcwd(), "proof", "videos")
        os.makedirs(video_dir, exist_ok=True)

        print("[BROWSER] Creating browser context...")
        self.context = self.browser.new_context(
            record_video_dir=video_dir,
            record_video_size={"width": 1280, "height": 720}
        )
        assert self.context is not None, "Failed to create browser context!"
        self.context.set_default_timeout(Config.TIMEOUT)
        
        print("[BROWSER] Opening page viewport...")
        self.page = self.context.new_page()
        assert self.page is not None, "Failed to create new page viewport!"
        
        print("\n" + "=" * 50)
        print("          PLAYWRIGHT BROWSER LAUNCHED")
        print("=" * 50)
        print(f" Browser Engine    : {browser_name.upper()}")
        print(f" Headless Mode     : {headless}")
        print(f" Slow Motion Delay : {slow_mo} ms")
        print(f" Default Timeout   : {Config.TIMEOUT} ms")
        print(f" Keep Browser Open : {Config.KEEP_BROWSER_OPEN}")
        print(f" Video Recording   : Enabled")
        print(f" Launch Status     : Asserted & Verified")
        print("=" * 50 + "\n")
        
        return self.page

    @property
    def video_path(self) -> str:
        """Retrieves the absolute path of the recording video file if enabled."""
        if self.page and self.page.video:
            try:
                return self.page.video.path()
            except Exception:
                pass
        return None

    def stop(self):
        """
        Clean up the page, context, browser, and stop Playwright.
        If KEEP_BROWSER_OPEN is true, pauses so the user can inspect the final state,
        then closes everything when they press Enter.
        """
        if Config.KEEP_BROWSER_OPEN:
            print("\n[BROWSER] Browser kept open for inspection.")
            print("[BROWSER] Press ENTER in the terminal to close the browser and continue...\n")
            try:
                input()
            except EOFError:
                # Running in non-interactive mode (e.g. CI pipeline), just continue
                pass

        if self.page:
            try:
                self.page.close()
            except Exception:
                pass
        if self.context:
            try:
                self.context.close()
            except Exception:
                pass
        if self.browser:
            try:
                self.browser.close()
            except Exception:
                pass
        if self.playwright:
            try:
                self.playwright.stop()
            except Exception:
                pass
