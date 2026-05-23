import os

class Config:
    """
    Configuration helper for the test framework.
    Reads setting environment variables or falls back to default values.
    """
    # Active Environment: 'QA' or 'PROD'
    ENV = os.getenv("TEST_ENV", "QA").upper()
    
    # Active Run Mode: 'UI' or 'API'
    RUN_MODE = os.getenv("RUN_MODE", "UI").upper()
    
    # Target URL definitions
    URLS = {
        "QA": "https://parabank.parasoft.com/parabank/index.htm?ConnType=JDBC",
        "PROD": "https://parabank.parasoft.com/parabank/index.htm",
    }
    
    # Browser Config
    BROWSER = os.getenv("BROWSER", "chromium").lower()
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))  # Milliseconds
    SLOW_MO = int(os.getenv("SLOW_MO", "500"))  # Milliseconds delay between each action
    KEEP_BROWSER_OPEN = os.getenv("KEEP_BROWSER_OPEN", "false").lower() == "true"
    
    @classmethod
    def get_base_url(cls) -> str:
        """Retrieves the URL based on the active environment."""
        url = cls.URLS.get(cls.ENV, cls.URLS["QA"])
        print(f"[CONFIG] Active Environment: {cls.ENV} | Target URL: {url}")
        return url

    @classmethod
    def is_ui_mode(cls) -> bool:
        """Checks if the run mode is UI."""
        return cls.RUN_MODE == "UI"

    @classmethod
    def is_api_mode(cls) -> bool:
        """Checks if the run mode is API."""
        return cls.RUN_MODE == "API"
