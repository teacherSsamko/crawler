word1 = 'python'
word2 = '123'
word3 = 'python123'

word4 = 'python' + word2

print(word4)
print(word3)
print(word4 == word3)


prod_id = '10095285'
detail_img_api = 'http://www.shoppingntmall.com/display/goods/detail/describe/' + prod_id
detail_img_api1 = 'http://www.shoppingntmall.com/display/goods/detail/describe/10095285'

print(detail_img_api)
print(detail_img_api1)
print(detail_img_api == detail_img_api1)


for i in range(10):
    prod_id = str(i)
    prod_id = word1
    detail_img_api = 'http://www.shoppingntmall.com/display/goods/detail/describe/' + prod_id
    detail_img_api1 = 'http://www.shoppingntmall.com/display/goods/detail/describe/python'

    print(detail_img_api)
    print(detail_img_api1)
    print(detail_img_api == detail_img_api1)
    break