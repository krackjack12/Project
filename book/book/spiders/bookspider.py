import scrapy
import pandas as pd

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    # General Parser for Spider
    def parse(self, response):
        books = response.css("article.product_pod")

        # GET NAME,URL and PRICE of ALL BOOKS <- All pages
        '''
        for book in books:
            yield{
                "name" : book.css("h3 a::text").get(),
                "url" : book.css("h3 a").attrib["href"],
                "price" : book.css(".product_price p::text").get(),
            }

        next_page = response.css("li.next a::attr(href)").get()

        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page

            yield response.follow(next_page_url, callback=self.parse)
        '''

        # Parsing the indiviual book link to function
        for book in books:
            relative_url = book.css("h3 a::attr(href)").get()

            if "catalogue/" in relative_url:
                book_url = "https://books.toscrape.com/" + relative_url
            else:
                book_url = "https://books.toscrape.com/catalogue/" + relative_url
            
            yield response.follow(book_url, callback=self.parse_book_page)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page

            yield response.follow(next_page_url, callback=self.parse)

    # Function for Parsing indiviual book page for Data
    def parse_book_page(self, response):
        page = response.css(".product_page").get()

        book_name = response.css(".product_main h1::text").get()
        book_price = response.css(".product_main p::text").get()

        category = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        product_description = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()

        table = response.css(".table")
        length = len(table)

        rating = response.css("p.star-rating").attrib["class"].split(" ")[-1]

        df = pd.DataFrame(columns=["Column","Value"])

        rows = table = response.css(".table tr")

        for row in rows:
            column_name = row.css("th::text").get()
            column_value = row.css("td::text").get()
            
            if column_name is not None and column_value is not None:
                record = [column_name,column_value]
                df.loc[len(df)] = record
        
        # To save the table of Product specifications as DataFrame: 
        # df.to_csv("/Users/krishjoshi/Desktop/Python/WebScraping/csv_files/" + book_name + ".csv",index=False)
        # Some are stored in csv_files folder

        yield{
            'url' : response.url,
            'book_name' : book_name,
            'book_price' : book_price,
            'category' : category,
            'rating' : rating,
        }

