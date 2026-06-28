from scrapers.eventbrite import scrape_eventbrite


def run_scrapers():
    """Run all event scrapers."""

    print("Starting Eventbrite scraper...")
    scrape_eventbrite()
    print("Eventbrite complete.")


if __name__ == "__main__":
    run_scrapers()