import random


class Generator:

    def generate_string(self):
        return "".join([random.choice("abcdefghijklmnopqrstuvwxyz_-1234567890") for i in range(random.randint(5, 20))])

    def generate_customer(self):
        customerschema = {
            "lname": self.generate_string(),
            "fname": self.generate_string(),
            "birthYear": random.randint(1920, 2010),
            "birthMonth": random.randint(1, 10),
            "birthday": random.randint(1, 31),
            "email": self.generate_string() + "@" + self.generate_string(),
            "password": self.generate_string(),

            "adress": {
                "country": self.generate_string(),
                "city": self.generate_string(),
                "Street": self.generate_string(),
                "number": random.randint(1, 100),
                "postCode": random.randint(1000, 9999)
            },
            "update": self.generate_string(),
            '_deleted': False

        }
        return customerschema

    def generate_customers(self, n):
        return [self.generate_customer() for i in range(n)]

    def generate_product(self):
        productschema = {
            "name": self.generate_string(),
            "price": random.randint(1, 100),
            "description": self.generate_string(),
            "category": self.generate_string(),
            "update": self.generate_string()
        }

        return productschema

    def generate_products(self, n):
        return [self.generate_product() for i in range(n)]

    def update_docs(self, docs):
        for doc in docs:
            doc["update"] = self.generate_string()

    def delete_docs(self, docs):
        for doc in docs:
            doc['_deleted'] = True