import psycopg2
import random
import time


class BenchmarkPostgres:
    def __init__(self):
        self.db = None
        self.countries_id = 0
        self.cities_id = 0
        self.addresses_id = 0
        self.inventory_id = []
        self.sku = []
        self.customers_id = []
        self.products_id = []

    def connect(self):
        self.db = psycopg2.connect(
            host="localhost",
            database="wishzon",
            user="postgres",
            password="imane"
        )

    def close(self):
        self.db.close()

    def generate_string(self):
        return "".join([random.choice("abcdefghijklmnopqrstuvwxyz_-1234567890") for i in range(random.randint(5, 12))])

    def insert_countries(self):
        self.countries_id += 1
        self.connect()
        cur = self.db.cursor()
        cur.execute("INSERT INTO Country (country_id, country) VALUES (%s, %s)",
                    (self.countries_id, self.generate_string()))
        self.db.commit()
        self.close()

    def insert_cities(self):
        self.cities_id += 1
        self.insert_countries()
        self.connect()
        cur = self.db.cursor()
        cur.execute("INSERT INTO City (city_id, country_id, city) VALUES (%s, %s, %s)",
                    (self.cities_id, self.countries_id, self.generate_string()))
        self.db.commit()
        self.close()

    def insert_addresses(self):
        self.addresses_id += 1
        self.insert_cities()
        self.connect()
        cur = self.db.cursor()
        cur.execute("INSERT INTO Address (address_id, city_id, street, number, postcode) VALUES (%s,%s,%s,%s,%s)", (
        self.addresses_id, self.cities_id, self.generate_string(), random.randint(1, 1000), random.randint(1000, 9999)))
        self.db.commit()
        self.close()

    def insert_customers(self, n, begin):
        begin = 1
        if len(self.customers_id) != 0:
            begin = self.customers_id[-1] + 1
        start = time.time()
        self.insert_addresses()
        self.connect()
        cur = self.db.cursor()
        for i in range(begin, begin + n):
            cur.execute("INSERT INTO Customer(customer_id, fname, lname, email, password, address_id)\
                VALUES(%s, %s, %s, %s, %s, %s)", (
            i, self.generate_string(), self.generate_string(), self.generate_string(), self.generate_string(),
            self.addresses_id))
            self.customers_id.append(i)
        self.db.commit()
        self.close()
        end = time.time()
        print("Insertion of ", n, " customers took: ", end - start, " ms")
        return end - start

    def insert_inventory(self):
        self.connect()
        cur = self.db.cursor()
        for i in range(1, 1001):
            cur.execute("INSERT INTO Inventory(inventory_id, title) VALUES (%s, %s)", (i, self.generate_string()))
            self.inventory_id.append(i)
        self.db.commit()
        self.close()

    def insert_item(self):
        self.connect()
        cur = self.db.cursor()
        for i in range(1, 10001):
            cur.execute("INSERT INTO Item(sku, price) VALUES (%s, %s)", (i, random.randint(1, 100)))
            self.sku.append(i)
        self.db.commit()
        self.close()

    def insert_products(self, n):
        begin = 1
        if len(self.customers_id) != 0:
            begin = self.customers_id[-1] + 1
        start = time.time()
        self.connect()
        cur = self.db.cursor()
        for i in range(self.customers_id, n + n):
            cur.execute("INSERT INTO InventorySku(inventory_id, item_sku, quantity) VALUES(%s, %s, %s)",
                        (random.choice(self.inventory_id), random.choice(self.sku), random.randint(1, 100)))
            self.products_id.append(i)
        self.db.commit()
        self.close()
        end = time.time()
        print("Insertion of ", n, " products took ", end - start, " s")
        return end - start

    def update_customers(self, n):
        start = time.time()
        self.connect()
        cur = self.db.cursor()
        for i in range(n):
            cur.execute(
                "UPDATE Customer SET lname = %s WHERE  address_id in (SELECT address_id FROM Address where city_id =%s)",
                (self.generate_string(), random.randint(1, self.cities_id)))
        self.db.commit()
        end = time.time()
        self.close()
        print("Update of ", n, " customers took: ", end - start)
        return end - start

    def update_products(self, n):
        self.connect()
        cur = self.db.cursor()
        start = time.time()
        for i in range(n):
            cur.execute("UPDATE InventorySku SET quantity = %s WHERE inventory_id = %s",
                        (random.randint(1, 100), random.choice(self.products_id)))
        self.db.commit()
        end = time.time()
        print("Update of ", n, " products took: ", end - start)
        self.close()
        return end - start

    def select_customers(self, n):
        start = time.time()
        self.connect()
        cur = self.db.cursor()
        for i in range(n):
            cur.execute("SELECT * FROM Customer WHERE address_id in (SELECT address_id from Address where city_id=%s)",
                        (random.randint(1, self.cities_id),))
        self.db.commit()
        end = time.time()
        self.close()
        print("Select of ", n, " customers took: ", end - start)
        return end - start

    def select_products(self, n):
        self.connect()
        start = time.time()
        cur = self.db.cursor()
        for i in range(n):
            cur.execute("SELECT * FROM InventorySku WHERE inventory_id = %s", (random.choice(self.products_id),))
        self.db.commit()
        end = time.time()
        print("Select of ", n, " products took: ", end - start)
        self.close()
        return end - start

    def delete_customers(self, n):
        self.connect()
        cur = self.db.cursor()
        start = time.time()
        for i in range(n):
            id = self.customers_id.pop()
            cur.execute("DELETE FROM Customer WHERE address_id in (SELECT address_id from Address where city_id=%s)",
                        (random.randint(1, self.cities_id),))
        self.db.commit()
        end = time.time()
        print("Delete of ", n, " customers took: ", end - start)
        self.close()
        return end - start

    def delete_products(self, n):
        self.connect()
        cur = self.db.cursor()
        start = time.time()
        for i in range(n):
            id = self.products_id.pop()
            cur.execute("DELETE FROM InventorySku WHERE inventory_id=%s", (id,))
        self.db.commit()
        end = time.time()
        print("Delete of ", n, " products took: ", end - start)
        self.close()
        return end - start


if __name__ == "__main__":
    b = BenchmarkPostgres()
    size = [10, 100, 500, 1000, 5000, 10000, 100000, 1000000]
    insertTime = []
    updateTime = []
    readTime = []
    deleteTime = []

    # insert test
    begin = 1
    for n in size:
        t1 = b.insert_customers(n, begin)
        insertTime.append(t1)
        print("Moyenne insertion for ", n, " values = ", t1, "s")
        begin = n + 1
    # update test
    for n in size:
        t1 = b.update_customers(n)
        updateTime.append(1)
        print("Moyenne update for ", n, " values = ", t1, "s")
    # Select test
    for n in size:
        t1 = b.select_customers(n)
        readTime.append(t1)
        print("Moyenne read for ", n, " values = ", t1, "s")
    # Delete test
    for n in size:
        t1 = b.delete_customers(n)
        deleteTime.append(t1)
        print("Moyenne delete for ", n, " values = ", t1, "s")




