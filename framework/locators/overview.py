"""Locators for root-level pages (Overview, Repositories)."""


class OverViewPageLocators:
    """Locators for the Overview Page"""

    OVERVIEW_HEADER = 'h1:has-text("Overview")'
    SKIP_TOUR_BUTTON = 'button:has-text("Skip tour")'


class RepositoriesPageLocators:
    """Locators for the Repositories Page"""

    # Repository-specific column
    REPOSITORY_COLUMN_HEADER = 'role=columnheader[name="Repository"]'
