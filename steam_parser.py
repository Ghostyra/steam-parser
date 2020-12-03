import re
import csv


def to_str_with_sep(arr, sep):
    return sep.join(str(x) for x in arr)


class SteamParser:
    def __init__(self):
        self.url = ""

    def set_url(self, url):
        self.url = url

    def parsing(self):
        from creating_soup import get_links

        links = get_links(self.url)
        headers = ["Title", "Release date", "Developer", "Publisher", "Reviews count",
                   "Reviews summary", "Positive percent", "Price", "Languages", "Achievements count",
                   "Genres", "Steam categories"]

        with open("steam_data.csv", "w", encoding='utf-8', newline="\n") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for link in links:
                row = self.parse_data(link)
                if row:
                    writer.writerow(row)

    @staticmethod
    def parse_data(link):
        from creating_soup import create_soup

        page_soup = create_soup(link)

        # If game not released
        if page_soup.find(attrs={"class": "not_yet"}):
            return 0

        # Parse title
        title = page_soup.find("div", attrs={"class": "apphub_AppName"}).text

        # Get users review, date, devs and publisher block
        user_reviews = page_soup.find("div", attrs={"class": "user_reviews"})

        # Parse release date
        date = user_reviews.find("div", attrs={"class": "date"}).text

        # Parse devs and publisher
        dev_rows = user_reviews.find_all("div", attrs={"class": "dev_row"})
        dev = [word.text for word in dev_rows[0].find_all("a")]
        publisher = [word.text for word in dev_rows[1].find_all("a")]

        # Parse reviews count, text-value, percent of positive review
        review_spans = user_reviews.find("div", attrs={"class": "subtitle column all"}). \
            next_sibling.next_sibling.find_all("span")
        game_review_summary = review_spans[0].text.strip()
        reviews_count = review_spans[1].text.strip().strip("()")
        # Check for trash-span
        if review_spans[2].text == "*":
            percent = re.findall(r"[0-9]+%", review_spans[3].text)[0]
        else:
            percent = re.findall(r"[0-9]+%", review_spans[2].text)[0]

        # Get price block
        price_panel = page_soup.find_all("div", attrs={"class": "game_purchase_action"})

        # Ignore demo
        if page_soup.find("div", attrs={"class": "game_area_purchase_game demo_above_purchase"}):
            price_panel = price_panel[1]
        else:
            price_panel = price_panel[0]
        price_panel_discount = price_panel.find("div", attrs={"class": "discount_original_price"})
        # Parse original price, ignore discount
        if price_panel_discount:
            price = price_panel_discount.text
        else:
            price = price_panel.find("div", attrs={"class": "game_purchase_price price"}).text.strip()

        # Parse languages
        languages_table = page_soup.find("table", attrs={"class": "game_language_options"})
        languages = [re.sub(r"\s+", " ", lang.text).strip() for lang in
                     languages_table.find_all("td", attrs={"class": "ellipsis"})]

        # Parse achievements count if they are
        achievements_count = 0
        achievements_block = page_soup.find("div", attrs={"class": "communitylink_achievement_images"})
        if achievements_block:
            achievements_count = int(re.findall(r"\d+", achievements_block.previous_sibling.previous_sibling.text)[0])

        # Parse genres without devs and publisher in this block
        genres_table = page_soup.find("div", attrs={"class": "details_block"})
        for div in genres_table.find_all("div", attrs={"class": "dev_row"}):
            div.decompose()
        genres = [genre.text for genre in genres_table.find_all("a")]

        # Parse game steam-categories
        categories_table = page_soup.find("div", attrs={"id": "category_block"})
        categories = [re.sub(r"\s+", " ", a.text).strip() for a in
                      categories_table.find_all("a", attrs={"class": "name"})]

        return [title, date, to_str_with_sep(dev, ","), to_str_with_sep(publisher, ","),
                reviews_count, game_review_summary, percent, price, to_str_with_sep(languages, ","),
                achievements_count, to_str_with_sep(genres, ","), to_str_with_sep(categories, ",")]
