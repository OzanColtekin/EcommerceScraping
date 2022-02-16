import pyodbc


class Database:
    def __init__(self, hostname, database, username, password):
        self.hostname = hostname
        self.database = database
        self.username = username
        self.password = password
        self.connection = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=' + self.hostname + ';DATABASE=' + self.database + ';UID=' +
            self.username + ';PWD=' + self.password)
        self.cursor = self.connection.cursor()

    def addproduct(self, product):
        self.sql = f"INSERT INTO Products(ProductBarcode, ProductBrand, ProductName, ProductPoint, Favories," \
                   f" SellerPoint, IsFreeCargo, RatingCount, CategoryID, Price, Date, Status) VALUES " \
                   f"('{product.ProductBarcode}', '{product.ProductBrand}', '{product.ProductName}', " \
                   f"'{product.ProductPoint}', '{product.Favories}', '{product.SellerPoint}', " \
                   f"'{product.IsFreeCargo}', '{product.RatingCount}', '{product.CategoryID}', " \
                   f"'{product.Price}', '{product.Date}', '{product.Status}')"
        self.cursor.execute(self.sql)
        self.connection.commit()
