class Order:
    def __init__(self, id_order, id_status, status_name, id_pick_up_ponit, id_pick_up_ponit_name, date_order, date_delivery):
        self.id = id_order
        self.id_status = id_status
        self.status_name = status_name
        self.id_pick_up_ponit = id_pick_up_ponit
        self.id_pick_up_ponit_name = id_pick_up_ponit_name
        self.date_order = date_order
        self.date_delivery = date_delivery
