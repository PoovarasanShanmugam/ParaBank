from pom.base_page import BasePage

class AccountsOverviewPage(BasePage):
    """
    Page Object class for the accounts overview dashboard page.
    """
    HEADERS = [
        "h1.title",
        "h1",
        "//h1[@class='title']"
    ]
    ACCOUNT_TABLES = [
        "table#accountTable",
        "table.table",
        "#accountTable"
    ]
    ROWS_LOCATORS = [
        "table#accountTable tbody tr",
        "table.table tbody tr",
        "#accountTable tbody tr"
    ]

    def wait_for_load(self):
        """Wait for the accounts overview dashboard elements to load."""
        print("[ACCOUNTS PAGE] Waiting for Accounts Overview page to load...")
        self.wait_for_selector_with_fallback(self.HEADERS)
        self.wait_for_selector_with_fallback(self.ACCOUNT_TABLES)

    def get_accounts_data(self) -> list:
        """
        Retrieves all account numbers, balances, and available amounts.
        Returns a list of dictionaries containing account details.
        """
        self.wait_for_load()
        
        # Get active row locator
        row_selector = self.wait_for_selector_with_fallback(self.ROWS_LOCATORS)
        rows = self.page.locator(row_selector).all()
        accounts_list = []
        
        print(f"[ACCOUNTS PAGE] Found {len(rows)} table rows. Extracting cell details...")
        for row in rows:
            cells = row.locator("td").all()
            if len(cells) >= 3:
                account_id = cells[0].inner_text().strip()
                balance = cells[1].inner_text().strip()
                available = cells[2].inner_text().strip()
                
                # Exclude the "Total" row from the list of accounts
                if "Total" not in account_id and account_id != "":
                    accounts_list.append({
                        "account_id": account_id,
                        "balance": balance,
                        "available": available
                    })
        return accounts_list

    def get_total_balance(self) -> str:
        """
        Retrieves the Total Balance displayed at the bottom of the table.
        """
        self.wait_for_load()
        row_selector = self.wait_for_selector_with_fallback(self.ROWS_LOCATORS)
        rows = self.page.locator(row_selector).all()
        for row in rows:
            cells = row.locator("td").all()
            if len(cells) >= 2:
                first_cell_text = cells[0].inner_text().strip()
                if "Total" in first_cell_text or first_cell_text == "":
                    # Locate cell starting with "$"
                    for cell in cells[1:]:
                        text = cell.inner_text().strip()
                        if text.startswith("$"):
                            print(f"[ACCOUNTS PAGE] Total Balance identified: {text}")
                            return text
        
        # Fallback: get last row's second column
        last_row_cells = self.page.locator(f"{row_selector}:last-child td").all()
        if len(last_row_cells) >= 2:
            balance = last_row_cells[1].inner_text().strip()
            print(f"[ACCOUNTS PAGE] Fallback Total Balance identified: {balance}")
            return balance
        
        print("[ACCOUNTS PAGE] [WARNING] Could not identify total balance cell.")
        return "$0.00"

    def get_welcome_message(self) -> str:
        """
        Retrieves the welcome message text (e.g. 'Welcome First Last') from the left sidebar.
        """
        selectors = [
            "p.smallText",
            "#leftPanel p.smallText",
            "//div[@id='leftPanel']//p",
            "#leftPanel p"
        ]
        return self.get_text_with_fallback(selectors)

