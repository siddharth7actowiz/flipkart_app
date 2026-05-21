from itemadapter import ItemAdapter
import mysql.connector



class FlipkartPipeline:
    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host= "localhost",
            port= 3306,
            user= "root",
            password= "actowiz",
            database= "flipkart"
        )
        self.cursor = self.conn.cursor()


        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_data_flipkart2 (
            Id int  AUTO_INCREMENT PRIMARY KEY,
            product_id varchar(40) NOT NULL,
            catalog_name varchar(500) NOT NULL,
            catalog_id varchar(40) NOT NULL,
            source varchar(40) DEFAULT 'Flipkart',
            scraped_date datetime DEFAULT CURRENT_TIMESTAMP,
            product_name varchar(500) DEFAULT 'N/A',
            image_url varchar(500) DEFAULT 'N/A',
            category_hierarchy json DEFAULT NULL,
            product_price decimal(9,2) DEFAULT NULL,
            arrival_date varchar(40) DEFAULT 'N/A',
            shipping_charges float DEFAULT NULL,
            is_sold_out varchar(40) DEFAULT 'false',
            discount varchar(40) DEFAULT 'N/A',
            mrp decimal(9,2) DEFAULT NULL,
            page_url varchar(500) DEFAULT 'N/A',
            product_url varchar(500) NOT NULL,
            number_of_ratings int DEFAULT NULL,
            avg_rating float DEFAULT NULL,
            position varchar(5) DEFAULT 'N/A',
            country_code varchar(2) DEFAULT 'IN',
            others json DEFAULT NULL
            
        )
        """)

        self.cursor.execute("""
             CREATE TABLE IF NOT EXISTS product_links (
                 id INT AUTO_INCREMENT PRIMARY KEY,
                 product_id VARCHAR(40),
                 url VARCHAR(600) UNIQUE,
                 status VARCHAR(20) DEFAULT 'pending'
             )
             """)

        self.conn.commit()

    def process_item(self, item, spider):
        if spider.name == "pdp":
            item = ItemAdapter(item)

            cols = ",".join(item.keys())
            placeholders = ",".join(["%s"] * len(item))
            values = tuple(item.values())

            query = f"INSERT INTO product_data_flipkart2 ({cols}) VALUES ({placeholders})"

            self.cursor.execute(query, values)
            self.update_url_status("product_links",item["product_id"])
            self.conn.commit()
            return item
        if spider.name=="pl":
            item = ItemAdapter(item)

            cols = ",".join(item.keys())
            placeholders = ",".join(["%s"] * len(item))
            values = tuple(item.values())
            query = f"INSERT  IGNORE INTO   product_links ({cols}) VALUES ({placeholders})"

            self.cursor.execute(query, values)
            self.conn.commit()
            return item
        return item

    # def fetch_pending_url(self, tab_name: str):
    #
    #     if not hasattr(self, "conn") or self.conn is None:
    #         raise Exception("DB connection not initialized. open_spider not called yet.")
    #
    #     dict_cur = self.conn.cursor(dictionary=True, buffered=True)
    #
    #     query = f"SELECT * FROM {tab_name} WHERE status='pending'"
    #     dict_cur.execute(query)
    #
    #     rows = dict_cur.fetchall()
    #     dict_cur.close()
    #
    #     return rows

    def update_url_status(self, tab_name, url, new_status="done")->None:
        """Updates the status of a specific row by its ID."""
        query = f"UPDATE {tab_name} SET status = %s WHERE product_id = %s"
        self.cursor.execute(query, (new_status, url))
        self.conn.commit()
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()