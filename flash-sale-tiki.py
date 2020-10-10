import os
import requests
import time



headers = {
    'host': 'tiki.vn',
    'accept': 'application/json, text/plain, */*',
    'x-access-token': 'your access token',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://tiki.vn',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://tiki.vn/may-anh-canon-eos-1500d-lens-ef-s-18-55mm-iii-hang-chinh-hang-p1732201.html?spid=1732203&src=lp-1028',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'cookie': 'your cookie'
}

# url = 'https://tiki.vn/may-anh-canon-eos-1500d-lens-ef-s-18-55mm-iii-hang-chinh-hang-p1732201.html?spid=1732203&src=lp-1028' ==> id san pham la 1732203

def get_price_id(idsanpham):
    params = (
        ('platform', 'web'),
    )

    response = requests.get(f'https://tiki.vn/api/v2/products/{idsanpham}/info', headers=headers, params=params)


    null = ''
    true = True
    false = False
    data = str(response.text)
    price = eval(data)['price']
    print(price)
    return price

def book_item(idsanpham):
    data = '{"products":[{"product_id":"%s","qty":1}]}'%(idsanpham)
    print('book san pham')

    response = requests.post('https://tiki.vn/api/v2/carts/mine/items', headers=headers, data=data)
    print(response.text)


def get_don_hang_id():
    params = (
        ('include', 'items'),
    )

    response = requests.get('https://tiki.vn/api/v2/carts/mine', headers=headers, params=params)

    null = ''
    false = False
    true = True
    data = str(response.text)
    return eval(data)['items'][0]['id']

def set_so_luong(donhangid):
    data = '{"qty":"1"}'

    response = requests.put(f'https://tiki.vn/api/v2/carts/mine/items/{donhangid}', headers=headers, data=data)

    null = ''
    false = False
    true = True
    print(response.text)

def get_address():
    params = (
        ('limit', '10000'),
    )

    response = requests.get('https://tiki.vn/api/v2/me/address', headers=headers, params=params)

    null = ''
    false = False
    true = True
    diachiid = eval(response.text)['data'][0]['id']
    print('get dia chi')
    print(diachiid)
    return diachiid

def set_dia_chi(diachiid):
    response = requests.put(f'https://tiki.vn/api/v2/carts/mine/shippings_addresses/{diachiid}', headers=headers)
    print('set dia chi')
    print(response.text)

def set_payment_method(method='cod'):
    print('set pay ment method')
    response = requests.put(f'https://tiki.vn/api/v2/carts/mine/payment_methods/{method}', headers=headers)
    print(response.text)


def set_gift_none():
    data = '{"is_sent_as_gift":false,"gift_info":{"from":"","to":"","message":""}}'

    response = requests.put('https://tiki.vn/api/v2/carts/mine/as_gift', headers=headers, data=data)
    print(response.text)

def completepayment():
    data = '{"payment":{"method":"cod","option_id":null},"tax_info":null,"cybersource_information":{},"customer_note":""}'

    response = requests.post('https://tiki.vn/api/v2/carts/mine/checkout', headers=headers, data=data)
    print(response.text)
    print('finish!')



if __name__ == '__main__':
    idsanpham = input('id san pham: ')
    gia_to_book = int(input('set gia: '))
    while 1:
        try:
            gia_hien_tai = get_price_id(idsanpham)
            print(time.time())
        except:
            print('loi mang')
        if gia_hien_tai == gia_to_book:
            book_item(idsanpham)
            set_so_luong(get_don_hang_id())
            set_dia_chi(get_address())
            set_payment_method()
            set_gift_none()
            completepayment()
            break
        time.sleep(1)