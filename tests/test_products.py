from typing import List
from app import ProductOut

def test_get_all_products(authorized_client, test_products):
    res = authorized_client.get("/products/")
    
    def validate(product):
        return ProductOut(**product)
    
    products_map = map(validate, res.json())
    products_list = list(products_list)

    assert len(res.json()) == len(test_products)
    assert res.status_code == 200
