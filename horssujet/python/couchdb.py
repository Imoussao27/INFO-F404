from time2relax import CouchDB
from Generator import Generator
import time


class Benchmarks:
    def __init__(self) -> None:
        self.db = CouchDB('http://admin:admin@localhost:5984/wishzone')
        self.generator = Generator()
        self.bulkSize = [10, 100, 500, 1000, 5000,10000, 50000, 100000]
        self.insertTime = []
        self.readTime = []
        self.updateTime = []
        self.deleteTime = []

    def benchmark(self):
        for n in self.bulkSize:
            self.bulk(n)

    def bulk(self, n):
        customers = self.generator.generate_customers(n)
        products = self.generator.generate_products(n)
        docs = customers + products

        # inserts
        start = time.time()
        self.db.bulk_docs(docs)
        end = time.time()
        self.insertTime.append(end - start)
        print(len(docs), " docs inserted in ", end - start, " ms")

        # reads
        start = time.time()
        res = self.db.all_docs().json()
        end = time.time()
        self.readTime.append(end - start)
        print(len(docs), " docs read in ", end - start, " ms")

        # updates
        docs = [self.db.get(doc['id']).json() for doc in res['rows']]
        self.generator.update_docs(docs)
        start = time.time()
        self.db.bulk_docs(docs)
        end = time.time()
        self.updateTime.append(end - start)
        print(len(docs), " rows updated in ", end - start, " ms")

        # deleted
        res = self.db.all_docs().json()
        docs = [self.db.get(doc['id']).json() for doc in res['rows']]
        self.generator.delete_docs(docs)
        start = time.time()
        self.db.bulk_docs(docs)
        end = time.time()
        self.deleteTime.append(end - start)
        print(len(docs), " docs deleted in ", end - start, " ms")


if __name__ == "__main__":
    b = Benchmarks()
    #[10, 100, 500, 1000, 5000,10000, 50000, 100000, 1000000]
    b.bulk(25000)