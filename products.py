class Product:
    def __init__(self, pbarcode, pbrand, pname, ppoint, pfav, pselpoint, pcargo, prating, pcategory, pprice, pdate, pstatus):
        self.ProductBarcode = pbarcode
        self.ProductBrand = pbrand
        self.ProductName = pname
        self.ProductPoint = ppoint
        self.Favories = pfav
        self.SellerPoint = pselpoint
        self.IsFreeCargo = pcargo
        self.RatingCount = prating
        self.CategoryID = pcategory
        self.Price = pprice
        self.Date = pdate
        self.Status = pstatus
