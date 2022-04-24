from django.shortcuts import render
from django.contrib.auth.models import User

from .models import *
from .forms import *



def index(request):
    products = ProductName.objects.all()
    form = SearchForm()

    if request.method == 'POST':
        find_product = request.POST.get('search_product')
        product_find = ProductName.objects.get(name=find_product)

        return product_info(request, product_find.id)

    else:
        context = {'products': products, 'form':form}
        return render(request, 'main_page/index.html', context)


def product_info(request, pk):
    products = ProductName.objects.get(id=pk)
    a = User.objects.get(id=request.user.id)
    
    

    # Добавление в корзину
    if request.method == 'POST':
        # Получаем данные из формы
        get_user = User.objects.get(id=request.user.id)
        print(products.price)
        user_cart = CartWeb.objects.create(product_name=products, user_id=get_user.id, product_count=1)
        return render(request, 'main_page/index.html')
    
    else:
        print('hahaha')
        context = {'products': products}
        return render(request, 'main_page/product_info.html', context)




def cart(request):
    cart = CartWeb.objects.filter(user_id=request.user.id)
    for i in cart:
        print(i.product_name.name)
    return render(request, 'shopping_cart/cart.html', {'cart': cart})