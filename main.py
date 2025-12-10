from fastapi import FastAPI, HTTPException
from typing import Optional, List
from model import Product, Review
from fastapi.responses import JSONResponse

app = FastAPI(title='Product Management')
import json

def getProductJson() -> list[dict]:
    with open('products.json', 'r') as File:
        response = json.load(File)
        return response

PRODUCT_JSON = getProductJson()


@app.get('/product', response_model=List[Product], name='Get All')
def getAll():
    return PRODUCT_JSON


@app.get('/product/{id}', response_model=Product, name='Get By Id')
async def getById(id: int):
        filtered_product = list(filter(lambda e:e['id'] == id, PRODUCT_JSON))
        dbProduct = filtered_product[0] if filtered_product else None
        print(bool(filtered_product))
        if dbProduct is None:
            raise HTTPException(status_code=404, detail='Product does not exist.')
        
        return dbProduct


@app.post('/product', name='Create Product')
async def createProduct(product: Product):
    productExists = list(filter(lambda e: product.id == e['id'], PRODUCT_JSON))
    if productExists:
        raise HTTPException(status_code=400, detail='Product id exists')
    
    new_product = product.model_dump() # convert pydantic model to dict
    PRODUCT_JSON.append(new_product)
    return JSONResponse(status_code=201, content='Product created successfully')

@app.put('/product/{id}', name='Update Product')
async def updateProduct(id: int, product: Product):

    product_index = next((i for i, e in enumerate(PRODUCT_JSON) if e['id'] == id), None)

    if product_index is None:
        raise HTTPException(status_code=404, detail=f'Product id {id} not found.')

    if product.id != id:
         raise HTTPException(status_code=400, detail="Product ID in path does not match ID in request body.")

    updated_data = product.model_dump() 
    
    PRODUCT_JSON[product_index] = updated_data

    return updated_data


@app.delete('/product/{id}', name='Delete Product')
async def delete(id: int):
    product_index = next((i for i, e in enumerate(PRODUCT_JSON) if e['id'] == id), None)

    if product_index is None:
        raise HTTPException(status_code=404, detail=f'Product id {id} not found.')

    del PRODUCT_JSON[product_index]

    return JSONResponse(status_code=200, content={'message': 'Deleted successfully.'})

@app.get('/search')
async def search(q: Optional[str] = None):
    if not q:
        return PRODUCT_JSON
    results = list(filter(lambda e: q.lower() in e['description'].lower(), PRODUCT_JSON))
    print(f'============> product list', results)

    return results

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
