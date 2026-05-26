class Product:
    def __init__(self, id_product, article, id_type, type_name, unit,
                 price, id_suppliers,suppliers_name, id_producer,
                 producer_name, id_category, category_name, discount,
                 amount_storage, descrition, photo=None, photo_name=""):
        self.id = id_product
        self.article = article
        self.id_type = id_type
        self.type_name = type_name
        self.unit = unit
        self.price = price
        self.id_suppliers = id_suppliers
        self.suppliers_name = suppliers_name
        self.id_producer = id_producer
        self.producer_name = producer_name
        self.id_category = id_category
        self.category_name = category_name
        self.discount = discount
        self.amount_storage = amount_storage
        self.descrition = descrition
        self.photo = photo
        self.photo_name = photo_name