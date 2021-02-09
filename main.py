import sys
import math
import time
import threading
from collections import deque
from shlex import split

class Inventory:
    def __init__(self):
        self.products = {}      # product catalog (key: str (item sku), value: Product)
        self.warehouses = {}    # list of warehouses (key: int (warehouse id), value: Warehouse)

    # Add a new product to our product catalog.
    def add_product(self, pname, sku):
        if sku in self.products:
            print("ERROR adding product", pname, sku, ": existing SKU")
        else:
            self.products[sku] = Product(sku, pname)

    # Create a new warehouse where we can stock products.
    def add_warehouse(self, wID, limit):
        if wID in self.warehouses:
            print("ERROR adding warehouse", wID, ": existing warehouse ID")
        else:
            self.warehouses[wID] = Warehouse(wID, limit)

    # List all products in the product catalog.
    def list_products(self):
        tabulate(self.products, ["pname", "sku"], ["ITEM NAME", "ITEM SKU"])

    # List all warehouses.
    def list_warehouses(self):
        tabulate(self.warehouses, ["wID", "total_qty", "limit"], ["WAREHOUSE ID", "TOTAL QTY", "LIMIT"])

    # List information about the warehouse with the given warehouse#
    # along with a listing of all product stocked in the warehouse.
    def list_warehouse(self, wID):
        if wID not in self.warehouses:
            print("ERROR listing the warehouse", wID, ": not existing warehouse ID")
        else:
            self.warehouses[wID].list(self.products)

    # Stock QTY amount of product with SKU in WAREHOUSE# warehouse.
    def stock(self, sku, wID, qty):
        if sku not in self.products:
            print("ERROR stocking", sku, "in the warehouse", wID, ": not existing SKU")
        elif wID not in self.warehouses:
            print("ERROR stocking", sku, "in the warehouse", wID, ": not existing warehouse ID")
        elif qty <= 0:
            print("ERROR stocking", sku, "in the warehouse", wID, ": not positive quantity")
        else:
            self.warehouses[wID].stock(sku, qty)

    # Unstock QTY amount of product with SKU in WAREHOUSE# warehouse.
    def unstock(self, sku, wID, qty):
        if sku not in self.products:
            print("ERROR unstocking", sku, "in the warehouse", wID, ": not existing SKU")
        elif wID not in self.warehouses:
            print("ERROR unstocking", sku, "in the warehouse", wID, ": not existing warehouse ID")
        elif qty <= 0:
            print("ERROR stocking", sku, "in the warehouse", wID, ": not positive quantity")
        else:
            self.warehouses[wID].unstock(sku, qty)

    # Check and execute valid commands
    def check_cmd(self, cmd, queue):
        # Write command history to a file in batches of 2
        queue.append(cmd)
        if len(queue) >= 2:
            dump = [queue.popleft()]
            dump.append(queue.popleft())
            tr = threading.Thread(target=log, args=(dump,))
            tr.start()

        # Parse command and check validity
        cmds = split(cmd)
        # print(cmds)
        if cmds[0] == "ADD":
            if len(cmds) == 4 and cmds[1] == "PRODUCT":
                self.add_product(cmds[2], cmds[3])
            elif (len(cmds) == 3 or (len(cmds) == 4 and cmds[3].isnumeric())) and cmds[1] == "WAREHOUSE" and cmds[
                2].isnumeric():
                limit = math.inf if len(cmds) < 4 else int(cmds[3])
                self.add_warehouse(int(cmds[2]), limit)
            else:
                print("ERROR: Enter valid commands")
        elif cmds[0] == "STOCK" and len(cmds) == 4 and cmds[2].isnumeric() and cmds[3].isnumeric():
            self.stock(cmds[1], int(cmds[2]), int(cmds[3]))
        elif cmds[0] == "UNSTOCK" and len(cmds) == 4 and cmds[2].isnumeric() and cmds[3].isnumeric():
            self.unstock(cmds[1], int(cmds[2]), int(cmds[3]))
        elif cmds[0] == "LIST":
            if len(cmds) == 2 and cmds[1] == "PRODUCTS":
                self.list_products()
            elif len(cmds) == 2 and cmds[1] == "WAREHOUSES":
                self.list_warehouses()
            elif len(cmds) == 3 and cmds[1] == "WAREHOUSE" and cmds[2].isnumeric():
                self.list_warehouse(int(cmds[2]))
            else:
                print("ERROR: Enter valid commands")
        else:
            print("ERROR: Enter valid commands")

class Product:
    def __init__(self, sku, pname):
        self.sku = sku      # Item SKU (str)
        self.pname = pname  # Item name (str)

class Warehouse:
    def __init__(self, wID, limit):
        self.wID = wID      # Warehouse ID (int)
        self.limit = limit  # stock limit (int)
        self.total_qty = 0  # current stock quantity (int)
        self.shelf = {}     # current stocks (key: item str (sku), value: item qty (int))

    # Stocks QTY amount of product with SKU.
    def stock(self, sku, qty):
        if self.limit <= self.total_qty + qty:
            print("WARNING stocking quantity", qty, "adjusted to", self.limit - self.total_qty)
            qty = self.limit - self.total_qty
        if sku in self.shelf:
            self.shelf[sku] += qty
        else:
            self.shelf[sku] = qty
        self.total_qty += qty

    # Unstocks QTY amount of product with SKU.
    def unstock(self, sku, qty):
        if sku not in self.shelf:
            print("ERROR unstocking", sku, "in the warehouse", self.wID, ": not in stock")
            return
        if self.shelf[sku] < qty:
            print("WARNING unstocking quantity", qty, "adjusted to", qty - self.shelf[sku])
            qty = self.shelf[sku]
        self.shelf[sku] -= qty
        if self.shelf[sku] == 0:
            del self.shelf[sku]
        self.total_qty -= qty

    # List information about the warehouse including a listing of all stocked product.
    def list(self, products):
        print("Warehouse #", self.wID, "(", self.total_qty, "/", self.limit, ")")
        if self.total_qty <= 0:
            return
        headers = ["ITEM NAME", "ITEM SKU", "QTY"]
        maxLengths = [len(h) for h in headers]
        for sku, qty in self.shelf.items():
            if maxLengths[0] < len(getattr(products[sku], "pname")):
                maxLengths[0] = len(getattr(products[sku], "pname"))
            if maxLengths[1] < len(sku):
                maxLengths[1] = len(sku)
            if maxLengths[2] < len(str(qty)):
                maxLengths[2] = len(str(qty))
        row_format = " | ".join(["{:<" + str(i) + "}" for i in maxLengths])
        print("-" * (sum(maxLengths) + 3 * len(maxLengths) - 3))
        print(row_format.format(*headers))
        print("-" * (sum(maxLengths) + 3 * len(maxLengths) - 3))
        for sku, qty in self.shelf.items():
            print(row_format.format(getattr(products[sku], "pname"), sku, qty))
        print("-" * (sum(maxLengths) + 3 * len(maxLengths) - 3))

# Helper function to print lists of products or warehouses
def tabulate(dic, attrs, headers):
    maxLengths = [len(h) for h in headers]
    for v in dic.values():
        for i in range(len(attrs)):
            if maxLengths[i] < len(str(getattr(v, attrs[i]))):
                maxLengths[i] = len(str(getattr(v, attrs[i])))
    row_format = " | ".join(["{:<" + str(i) + "}" for i in maxLengths])
    print("-" * (sum(maxLengths) + 3 * len(maxLengths) - 3))
    print(row_format.format(*headers))
    print("-" * (sum(maxLengths) + 3 * len(maxLengths) - 3))
    for v in dic.values():
        values = [getattr(v, h) for h in attrs]
        print(row_format.format(*values))
    print("-" * (sum(maxLengths) + 3 * len(maxLengths) - 3))

global_lock = threading.Lock()
# Helper function to write command history to a file
def log(dump):
    with global_lock:
        with open("log.txt", "a") as file:
            for cmd in dump:
                file.write(cmd+"\n")

def main():
    inv = Inventory()
    queue = deque()
    while True:
        try:
            cmd = input("> ")
            inv.check_cmd(cmd, queue)
        except Exception as e:
            print(e)

def test():
    inv = Inventory()
    queue = deque()
    with open("sample_commands.txt", "r") as file:
        for line in file:
            print("> " + line.rstrip())
            inv.check_cmd(line.rstrip(), queue)

if __name__ == "__main__":
    open("log.txt", "w").close()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test()
    else:
        main()

