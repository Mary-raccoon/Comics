from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.contrib.messages import error
import re
import itertools
from itertools import groupby
import datetime 

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags="login")
        return redirect('/log_reg')
    user = User.objects.get(email = request.POST['email1'])
    if(bcrypt.checkpw(request.POST['password1'].encode(), user.password.encode())):
        print("password match")
        print(user.first_name)
        request.session['id'] = user.id
        request.session['first_name'] = user.first_name
        request.session['email'] = user.email
        messages.success(request, "You successfully loged in")
        return redirect('/my_collection')
    else:
        print("wrong password")
        return redirect('/log_reg')
    print(user.first_name)
 

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for field, msg in errors.items():
            messages.error(request, msg, extra_tags=field)
        return redirect('/log_reg')
    else:
        hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(hash_password)
        hash_pw = str(hash_password)
        new_pw = ""
        for i in range(len(hash_pw)):
            if (len(hash_pw)-1) > i > 1:
                new_pw += hash_pw[i]
        print(new_pw)
        user = User.objects.create(
            first_name=request.POST['first_name'],  
            email=request.POST['email'],
            password = new_pw
        )
        request.session['first_name'] = user.first_name
        request.session['id']=user.id
        messages.success(request, "User successfully created")
        
        return redirect('/my_collection')


def index(request):
    return render(request, 'comic/index.html')


def before(request, methods=['POST']):
    all_comics = Comic.objects.all()
    new = []
    new_obj = []
    new_cr_at = []

    if 'year' in request.POST == '':
        all_comics = Comic.objects.filter(title__icontains=request.POST['title'],
                                          creator__icontains=request.POST['creator'])

    if 'title' in request.POST == '':
        all_comics = Comic.objects.filter(year__icontains=request.POST['year'], 
                                          creator__icontains=request.POST['creator'])

    if 'creator' in request.POST == '':
        all_comics = Comic.objects.filter(year__icontains=request.POST['year'],
                                          title__icontains=request.POST['title'])
       
    if 'year' in request.POST == '' and 'title' in request.POST == '':
        all_comics = Comic.objects.filter(creator__icontains=request.POST['creator'])

    if 'year' in request.POST == '' and 'creator' in request.POST == '':
        all_comics = Comic.objects.filter(title__icontains=request.POST['title'])

    if 'title' in request.POST == '' and 'creator' in request.POST == '':
        all_comics = Comic.objects.filter(year__icontains=request.POST['year'])

    if 'title' in request.POST == '' and 'creator' in request.POST == '' and 'year' in request.POST == '':
        all_comics = Comic.objects.all()

    if 'title' in request.POST != '' and 'creator' in request.POST != '' and 'year' in request.POST != '':
        all_comics = Comic.objects.filter(year__icontains=request.POST['year'],
                                          title__icontains=request.POST['title'],
                                          creator__icontains=request.POST['creator'])
    
    for a in all_comics:
        obj_a = {'title': a.title, 'cover': a.cover, 'creator':a.creator}
        created_at_obj = {'title': a.title,'created_at': a.created_at}
        if obj_a in new:
            print(a.title)
        else:
            new.append({'title': a.title, 'cover': a.cover, 'creator':a.creator})
            new_obj.append(a)
            new_cr_at.append({'title': a.title,'created_at': a.created_at})
    all_comics = new_obj  

    context = {
        'all_comics': all_comics,
    }
    
    return render(request, 'comic/before.html', context)



def all_c(request, methods=['POST']):
    user = User.objects.get(id=request.session['id'])
    all_comics = Comic.objects.all()
    wishlist = user.added_to_wishlist_comic.all()
    my_comics = user.added_to_my_collect_comic.all()
    sold = user.added_to_sold_comic.all()

    print("user: ", request.session['id'])
    new = []
    new_obj = []
    new_cr_at = []

    if 'year' in request.POST == '':
        all_comics = Comic.objects.filter(title__icontains=request.POST['title'],
                                          creator__icontains=request.POST['creator'])

    if 'title' in request.POST == '':
        all_comics = Comic.objects.filter(year__icontains=request.POST['year'], 
                                          creator__icontains=request.POST['creator'])

    if 'creator' in request.POST == '':
        all_comics = Comic.objects.filter(year__icontains=request.POST['year'],
                                          title__icontains=request.POST['title'])
       
    if 'year' in request.POST == '' and 'title' in request.POST == '':
        all_comics = Comic.objects.filter(creator__icontains=request.POST['creator'])

    if 'year' in request.POST == '' and 'creator' in request.POST == '':
        all_comics = Comic.objects.filter(title__icontains=request.POST['title'])

    if 'title' in request.POST == '' and 'creator' in request.POST == '':
        all_comics = Comic.objects.filter(year__icontains=request.POST['year'])

    if 'title' in request.POST == '' and 'creator' in request.POST == '' and 'year' in request.POST == '':
        all_comics = Comic.objects.all()

    if 'title' in request.POST != '' and 'creator' in request.POST != '' and 'year' in request.POST != '':
        all_comics = Comic.objects.filter(year__icontains=request.POST['year'],
                                          title__icontains=request.POST['title'],
                                          creator__icontains=request.POST['creator'])
    
    for w in wishlist:
        obj_a = {'title': w.title, 'cover': w.cover, 'creator':w.creator}
        created_at_obj = {'title': w.title,'created_at': w.created_at}
        if obj_a in new:
            print(w.title)
        else:
            new.append({'title': w.title, 'cover': w.cover, 'creator':w.creator})
            new_obj.append(w)
            new_cr_at.append({'title': w.title,'created_at': w.created_at})
        
    print("len(new_obj) ",len(new_obj))


    for m in my_comics:
        obj_a = {'title': m.title, 'cover': m.cover, 'creator':m.creator}
        created_at_obj = {'title': m.title,'created_at': m.created_at}
        if obj_a in new:
            print(m.title)
        else:
            new.append({'title': m.title, 'cover': m.cover, 'creator':m.creator})
            new_obj.append(m)
            new_cr_at.append({'title': m.title,'created_at': m.created_at})
    print("len(new_obj) ",len(new_obj))


    for m in sold:
        obj_a = {'title': m.title, 'cover': m.cover, 'creator':m.creator}
        created_at_obj = {'title': m.title,'created_at': m.created_at}
        if obj_a in new:
            print(m.title)
        else:
            new.append({'title': m.title, 'cover': m.cover, 'creator':m.creator})
            new_obj.append(m)
            new_cr_at.append({'title': m.title,'created_at': m.created_at})
    print("len(new_obj) ",len(new_obj))

    
    for a in all_comics:
        obj_a = {'title': a.title, 'cover': a.cover, 'creator':a.creator}
        created_at_obj = {'title': a.title,'created_at': a.created_at}
        if obj_a in new:
            print(a.title)
        else:
            new.append({'title': a.title, 'cover': a.cover, 'creator':a.creator})
            new_obj.append(a)
            new_cr_at.append({'title': a.title,'created_at': a.created_at})
    all_comics = new_obj  

    counter = groupby(sorted(new_cr_at, key=lambda x: x['created_at']), lambda x: x['created_at'])
    
    new_counter = []
   
    for k, g in counter:
        my_count = len(list(g))
        print(k.year, k.month, k.day, my_count)
        new_counter.append({'year': k.year, 'mon': k.month, 'day': k.day, 'c': my_count})
    print(new_counter)

    context = {
        'user': user,
        'all_comics': all_comics,
        'new_counter': new_counter,  
        'wishlist': wishlist,
        'comics': Comic.objects.all()
    }
    
    return render(request, 'comic/all_c.html', context)


def sort_all(request, methods=['POST']):
    user = User.objects.get(id=request.session['id'])
    all_comics = []
    wishlist = user.added_to_wishlist_comic.all()
    new = []
    new_obj=[]

    if request.POST['sort'] == 'Title_a':
        all_comics = Comic.objects.order_by('title')

    if request.POST['sort'] == 'Title_z':
        all_comics = Comic.objects.order_by('-title')

    if request.POST['sort'] == 'Year':
        all_comics = Comic.objects.order_by('year')
        
    if request.POST['sort'] == 'Choose':
        all_comics = Comic.objects.all()
    
    if request.POST['sort'] == 'Last_added':
        all_comics = Comic.objects.order_by('-created_at')
       
    for a in all_comics:
        obj_a = {'title': a.title, 'cover': a.cover, 'creator':a.creator}
        if obj_a in new:
            print(a.title)
        else:
            new.append({'title': a.title, 'cover': a.cover, 'creator':a.creator})
            new_obj.append(a)
    all_comics = new_obj  
    user = User.objects.get(id=request.session['id'])
    wishlist = user.added_to_wishlist_comic.all()
    context = {
        'all_comics': all_comics,
        'user': user,
        'wishlist': wishlist 
    }
    return render(request, 'comic/sort_all.html', context)


def edit_all(request, id):
    context = {
		'comic': Comic.objects.get(id=id)
	}
    return render(request, 'comic/edit_all.html', context)


def update_comic_all(request, id):
    docfile = Comic.objects.get(id=id).docfile
    print('docfile: ', docfile)
    if request.method == "POST":
        print("*"*20)
        up_comic = Comic.objects.get(id=id)
        up_comic.title = request.POST['title']
        up_comic.desc = request.POST['desc']
        up_comic.qty = request.POST['qty']
        up_comic.price = request.POST['price']
        up_comic.price_sold = request.POST['price_sold'] 
        up_comic.date_of_purchase = request.POST['date_of_purchase']
        up_comic.date_of_sale = request.POST['date_of_sale']
        up_comic.creator = request.POST['creator']
        up_comic.year = request.POST['year']
        up_comic.cover = request.POST['cover']
        up_comic.docfile = docfile
        up_comic.save()

        return redirect('/all_c', docfile="docfile")


def view_from_all(request, id):
    comic = Comic.objects.get(id=id)
    profit = float(comic.price_sold) - float(comic.price)
    context = {
		'comic': Comic.objects.get(id=id),
        'profit': profit
	}
    print("$ ", profit)
    return render(request, 'comic/view_from_all.html', context)


def from_all_to_wish(request, id):
    
    comic = Comic.objects.get(id=id)
    
    new_comic = Comic.objects.create(
        title = comic.title, 
        desc = comic.desc, 
        docfile = comic.docfile,
        cover = comic.cover,
        price = comic.price, 
        author_id = request.session['id'],
        creator = comic.creator,
        year = comic.year,
        qty = 1, 
        price_sold = 0, 
        profit = 0,
        date_of_purchase = None, 
        date_of_sale = None, 
    )
    this_user = User.objects.get(id=request.session['id'])
    this_comic = Comic.objects.get(id=new_comic.id)
    this_comic.wishlist.add(this_user)
    print("this_comic.id: ", this_comic.id)
    print("new_comic.id: ", new_comic.id)
    return redirect('/all_c')


def wishlist(request, methods=['POST']):
    user = User.objects.get(id=request.session['id'])
    wishlist = user.added_to_wishlist_comic.all()

    if 'year' in request.POST == '':
        wishlist = user.added_to_wishlist_comic.filter(title__icontains=request.POST['title'],
                                                       creator__icontains=request.POST['creator'])

    if 'title' in request.POST == '':
        wishlist = user.added_to_wishlist_comic.filter(year__icontains=request.POST['year'], 
                                                       creator__icontains=request.POST['creator'])

    if 'creator' in request.POST == '':
        wishlist = user.added_to_wishlist_comic.filter(year__icontains=request.POST['year'],
                                                       title__icontains=request.POST['title'])

    if 'year' in request.POST == '' and 'title' in request.POST == '':
        wishlist = user.added_to_wishlist_comic.filter(creator__icontains=request.POST['creator'])

    if 'year' in request.POST == '' and 'creator' in request.POST == '':
        wishlist = user.added_to_wishlist_comic.filter(title__icontains=request.POST['title'])

    if 'title' in request.POST == '' and 'creator' in request.POST == '':
        wishlist = user.added_to_wishlist_comic.filter(year__icontains=request.POST['year'])

    if 'title' in request.POST == '' and 'creator' in request.POST == '' and 'year' in request.POST == '':
        wishlist = user.added_to_wishlist_comic.all()

    if 'title' in request.POST != '' and 'creator' in request.POST != '' and 'year' in request.POST != '':
        wishlist = user.added_to_wishlist_comic.filter(year__icontains=request.POST['year'],
                                                       title__icontains=request.POST['title'],
                                                       creator__icontains=request.POST['creator'])

    context = {
        'user': user,
        'wishlist': wishlist
    }
    return render(request, 'comic/wishlist.html', context)


def new_comic_wishlist(request):
    return render(request, 'comic/new_comic_wishlist.html')


def add_to_wishlist(request):
    errors = Comic.objects.comic_validator(request.POST)
    if len(errors):
        for key, msg in errors.items():
            messages.error(request, msg, extra_tags=key)
        return redirect('/new_comic_wishlist')
    else:
        if request.method == 'POST':
        
            comic = Comic.objects.create(
                title = request.POST['title'].capitalize(), 
                desc = request.POST['desc'], 
                docfile = request.FILES['docfile'],
                cover = request.POST['cover'],
                price = request.POST['price'], 
                author_id = request.session['id'],
                creator = request.POST['creator'],
                year = request.POST['year'],
                qty = 1, 
                price_sold = 0, 
                profit = 0,
                date_of_purchase = None, 
                date_of_sale = None, 
            )
            request.session['title'] = comic.title
            messages.success(request, "Comics successfully created")
            print("id: ", comic.id)
            print("title: ", comic.title)
            print(comic.docfile.name)
            this_user = User.objects.get(id=request.session['id'])
            this_comic = Comic.objects.get(id=comic.id)
            this_comic.wishlist.add(this_user)
            print('comic.year:', comic.year)
            return redirect('/wishlist')


def sort_wish(request, methods=['POST']):
    user = User.objects.get(id=request.session['id'])
    wishlist = []
   
    if request.POST['sort'] == 'Title_a':
        wishlist = user.added_to_wishlist_comic.order_by('title')

    if request.POST['sort'] == 'Title_z':
        wishlist = user.added_to_wishlist_comic.order_by('-title')

    if request.POST['sort'] == 'Year':
        wishlist = user.added_to_wishlist_comic.order_by('year')
    
    if request.POST['sort'] == 'Choose':
        wishlist = user.added_to_wishlist_comic.all()
    
    if request.POST['sort'] == 'Last_added':
        wishlist = user.added_to_wishlist_comic.order_by('-created_at')
    
    context = {
        'wishlist': wishlist,
    }
    return render(request, 'comic/sort_wish.html', context)


def edit_wish(request, id):
    context = {
		'comic': Comic.objects.get(id=id)
	}
    return render(request, 'comic/edit_wish.html', context)


def update_comic_wish(request, id):
    docfile = Comic.objects.get(id=id).docfile
    print('docfile: ', docfile)
    if request.method == "POST":
        print("*"*20)
        up_comic = Comic.objects.get(id=id)
        up_comic.title = request.POST['title']
        up_comic.desc = request.POST['desc']
        up_comic.price = request.POST['price']
        up_comic.creator = request.POST['creator']
        up_comic.year = request.POST['year']
        up_comic.cover = request.POST['cover']
        up_comic.docfile = docfile
        # up_comic.qty = request.POST['qty']
        # up_comic.price_sold = request.POST['price_sold'] 
        # up_comic.date_of_purchase = request.POST['date_of_purchase']
        # up_comic.date_of_sale = request.POST['date_of_sale']
        up_comic.save()

        return redirect('/wishlist', docfile="docfile")


def view_from_wishlist(request, id):
    comic = Comic.objects.get(id=id)
    profit = float(comic.price_sold) - float(comic.price)
    context = {
		'comic': Comic.objects.get(id=id),
        'profit': profit
	}
    print("$ ", profit)
    return render(request, 'comic/view_from_wishlist.html', context)


def destroy_from_wishlist(request, id):
    Comic.objects.get(id=id).delete()
    print('cancel ', id)
    return redirect('/wishlist')


def from_wish_to_collect(request, id):
    comic = Comic.objects.get(id=id)
   
    if request.method == "POST":
        print("*"*20)
        this_user = User.objects.get(id=request.session['id'])
         
        my_comic = Comic.objects.get(id=id)
        my_comic.title = comic.title
        my_comic.desc = comic.desc
        my_comic.qty = request.POST['qty']
        my_comic.price = request.POST['price']
        my_comic.date_of_purchase = request.POST['date_of_purchase']
        my_comic.creator = comic.creator
        my_comic.year = comic.year
        my_comic.cover = comic.cover
        my_comic.docfile = comic.docfile
        # sold_comic.date_of_sale = request.POST['date_of_sale']
        # sold_comic.price_sold = request.POST['price_sold'] 
        # sold_comic.profit = 0
        my_comic.save()

        my_comic.wishlist.remove(this_user)
        my_comic.my_collection.add(this_user)


    return redirect('/wishlist')


def to_collect(request, id):
    context = {
		'comic': Comic.objects.get(id=id)
	}
    return render(request, 'comic/to_collect.html', context)


def my_collection(request, methods=['POST']):
    print("request.session['id'] ", request.session['id'])
    user = User.objects.get(id=request.session['id'])
    my_comics = user.added_to_my_collect_comic.all()

    if 'year' in request.POST == '':
        my_comics = user.added_to_my_collect_comic.filter(title__icontains=request.POST['title'],
                                                          creator__icontains=request.POST['creator'])

    if 'title' in request.POST == '':
        my_comics = user.added_to_my_collect_comic.filter(year__icontains=request.POST['year'], 
                                                          creator__icontains=request.POST['creator'])

    if 'creator' in request.POST == '':
        my_comics = user.added_to_my_collect_comic.filter(year__icontains=request.POST['year'],
                                                          title__icontains=request.POST['title'])

    if 'year' in request.POST == '' and 'title' in request.POST == '':
        my_comics = user.added_to_my_collect_comic.filter(creator__icontains=request.POST['creator'])

    if 'year' in request.POST == '' and 'creator' in request.POST == '':
         my_comics = user.added_to_my_collect_comic.filter(title__icontains=request.POST['title'])

    if 'title' in request.POST == '' and 'creator' in request.POST == '':
        my_comics = user.added_to_my_collect_comic.filter(year__icontains=request.POST['year'])

    if 'title' in request.POST == '' and 'creator' in request.POST == '' and 'year' in request.POST == '':
        my_comics = user.added_to_my_collect_comic.all()

    if 'title' in request.POST != '' and 'creator' in request.POST != '' and 'year' in request.POST != '':
        my_comics = user.added_to_my_collect_comic.filter(year__icontains=request.POST['year'],
                                                          title__icontains=request.POST['title'],
                                                          creator__icontains=request.POST['creator'])
    context = {
        'user': user,
        'my_comics': my_comics,
    }
    
    return render(request, 'comic/my_collection.html', context)


def new_comic_my_collection(request):
    return render(request, 'comic/new_comic_my_collection.html')


def add_to_my_collection(request):
    errors = Comic.objects.comic_validator(request.POST)
    if len(errors):
        for key, msg in errors.items():
            messages.error(request, msg, extra_tags=key)
        return redirect('/new_comic_my_collection')
    else:
        if request.method == 'POST':

            comic = Comic.objects.create(
                title = request.POST['title'].capitalize(), 
                desc = request.POST['desc'], 
                docfile = request.FILES['docfile'],
                qty = request.POST['qty'], 
                price = request.POST['price'], 
                price_sold = 0, 
                profit = 0,
                date_of_purchase = request.POST['date_of_purchase'], 
                date_of_sale = None, 
                author_id = request.session['id'],
                year = request.POST['year'],
                cover = request.POST['cover'],
                creator = request.POST['creator'],
            )
            messages.success(request, "Comics successfully created")
            print("id: ", comic.id)
            print("title: ", comic.title)
            print(comic.docfile.name)
            this_user = User.objects.get(id=request.session['id'])
            this_comic = Comic.objects.get(id=comic.id)
            this_comic.wishlist.remove(this_user)
            this_comic.my_collection.add(this_user)
            
            return redirect('/my_collection')


def sort_collect(request, methods=['POST']):
    user = User.objects.get(id=request.session['id'])
    my_comics = []
    
    if request.POST['sort'] == 'Title_a':
        my_comics = user.added_to_my_collect_comic.order_by('title')

    if request.POST['sort'] == 'Title_z':
        my_comics = user.added_to_my_collect_comic.order_by('-title')

    if request.POST['sort'] == 'Year':
        my_comics = user.added_to_my_collect_comic.order_by('year')
    
    if request.POST['sort'] == 'Price_low':
        my_comics = user.added_to_my_collect_comic.order_by('price')
    
    if request.POST['sort'] == 'Price_high':
        my_comics = user.added_to_my_collect_comic.order_by('-price')
    
    if request.POST['sort'] == 'Choose':
        my_comics = user.added_to_my_collect_comic.all()
    
    if request.POST['sort'] == 'Last_added':
        my_comics = user.added_to_my_collect_comic.order_by('-created_at')
    
    context = {
        'my_comics': my_comics,
    }
    return render(request, 'comic/sort_collect.html', context)


def edit_collect(request, id):
    context = {
		'comic': Comic.objects.get(id=id)
	}
    return render(request, 'comic/edit_collect.html', context)

def update_comic_collect(request, id):
    docfile = Comic.objects.get(id=id).docfile
    print('docfile: ', docfile)
    if request.method == "POST":
        print("*"*20)
        up_comic = Comic.objects.get(id=id)
        up_comic.title = request.POST['title']
        up_comic.desc = request.POST['desc']
        up_comic.qty = request.POST['qty']
        up_comic.price = request.POST['price']
        up_comic.date_of_purchase = request.POST['date_of_purchase']
        up_comic.creator = request.POST['creator']
        up_comic.year = request.POST['year']
        up_comic.cover = request.POST['cover']
        up_comic.docfile = docfile
        # up_comic.date_of_sale = request.POST['date_of_sale']
        # up_comic.price_sold = request.POST['price_sold'] 
        up_comic.save()

        return redirect('/my_collection', docfile="docfile")


def view_from_my_collection(request, id):
    comic = Comic.objects.get(id=id)
    profit = float(comic.price_sold) - float(comic.price)
    context = {
		'comic': Comic.objects.get(id=id),
        'profit': profit
	}
    print("$ ", profit)
    return render(request, 'comic/view_from_my_collection.html', context)


def destroy_from_my_collection(request, id):
    Comic.objects.get(id=id).delete()
    print('cancel ', id)
    return redirect('/my_collection')


def to_sell(request, id):
    context = {
		'comic': Comic.objects.get(id=id)
	}
    return render(request, 'comic/to_sell.html', context)


def from_collect_to_sold(request, id):
    comic = Comic.objects.get(id=id)
    qty = comic.qty
   
    if request.method == "POST":
        print("*"*20)
        this_user = User.objects.get(id=request.session['id'])
         
        sold_comic = Comic.objects.get(id=id)
        sold_comic.title = comic.title
        sold_comic.desc = comic.desc
        sold_comic.qty = request.POST['qty']
        sold_comic.price = request.POST['price']
        sold_comic.price_sold = request.POST['price_sold'] 
        sold_comic.profit = 0
        sold_comic.date_of_purchase = request.POST['date_of_purchase']
        sold_comic.date_of_sale = request.POST['date_of_sale']
        sold_comic.creator = comic.creator
        sold_comic.year = comic.year
        sold_comic.cover = comic.cover
        sold_comic.docfile = comic.docfile
        sold_comic.save()

        print("qty: ", qty) 

        if int(qty) == int(sold_comic.qty):
            sold_comic.profit = float(sold_comic.price_sold) - float(sold_comic.price)
            sold_comic.save()
            sold_comic.my_collection.remove(this_user)
            sold_comic.sold.add(this_user)

            print("int(qty) == int(sold_comic.qty)" )
            print("sold_comic.profit: ", sold_comic.profit) 
        elif int(qty) > int(sold_comic.qty):
            
            sold_comic = Comic.objects.create(
                title = comic.title,
                desc = comic.desc,
                qty = request.POST['qty'],
                price = request.POST['price'],
                price_sold = request.POST['price_sold'],
                date_of_purchase = request.POST['date_of_purchase'],
                date_of_sale = request.POST['date_of_sale'],
                author_id = comic.author_id,
                creator = comic.creator,
                year = comic.year,
                cover = comic.cover,
                docfile = comic.docfile,
                profit = 0
            )
            sold_comic.profit = float(sold_comic.price_sold) - float(sold_comic.price)
            sold_comic.save()
            sold_comic.sold.add(this_user)
            print("sold_comic.profit: ", sold_comic.profit) 
            this_comic = comic
            this_comic.qty = int(qty) - int(sold_comic.qty)
            this_comic.save()
            print("this_comic.qty: ", this_comic.qty)
        else:
            sold_comic = comic
            sold_comic.save()
            print("error")
             
        return redirect('/my_collection')


def sold(request):
    user = User.objects.get(id=request.session['id'])
    sold = user.added_to_sold_comic.all()
    if sold:
        profit = sold[0].price_sold - sold[0].price
        print(profit)
    if request.method == 'POST':
        if 'year' in request.POST == '':
            sold = user.added_to_sold_comic.filter(title__icontains=request.POST['title'],
                                                creator__icontains=request.POST['creator'])

        if 'title' in request.POST == '':
            sold = user.added_to_sold_comic.filter(year__icontains=request.POST['year'], 
                                                creator__icontains=request.POST['creator'])

        if 'creator' in request.POST == '':
            sold = user.added_to_sold_comic.filter(year__icontains=request.POST['year'],
                                                title__icontains=request.POST['title'])

        if 'year' in request.POST == '' and 'title' in request.POST == '':
            sold = user.added_to_sold_comic.filter(creator__icontains=request.POST['creator'])

        if 'year' in request.POST == '' and 'creator' in request.POST == '':
            sold = user.added_to_sold_comic.filter(title__icontains=request.POST['title'])

        if 'title' in request.POST == '' and 'creator' in request.POST == '':
            sold = user.added_to_sold_comic.filter(year__icontains=request.POST['year'])

        if 'title' in request.POST == '' and 'creator' in request.POST == '' and 'year' in request.POST == '':
            sold = user.added_to_sold_comic.all()

        if 'title' in request.POST != '' and 'creator' in request.POST != '' and 'year' in request.POST != '':
            sold = user.added_to_sold_comic.filter(year__icontains=request.POST['year'],
                                                title__icontains=request.POST['title'],
                                                creator__icontains=request.POST['creator'])

    context = {
        'user': user,
        'sold': sold, 
    }
    return render(request, 'comic/sold.html', context)



def sort_sold(request, methods=['POST']):
    user = User.objects.get(id=request.session['id'])
    sold = []
    
    if request.POST['sort'] == 'Title_a':
        sold = user.added_to_sold_comic.order_by('title')

    if request.POST['sort'] == 'Title_z':
        sold = user.added_to_sold_comic.order_by('-title')

    if request.POST['sort'] == 'Year':
        sold = user.added_to_sold_comic.order_by('year')
    
    if request.POST['sort'] == 'Profit_low':
        sold = user.added_to_sold_comic.order_by('profit')
    
    if request.POST['sort'] == 'Profit_high':
        sold = user.added_to_sold_comic.order_by('-profit')
    
    if request.POST['sort'] == 'Choose':
        sold = user.added_to_sold_comic.all()
    
    if request.POST['sort'] == 'Last_added':
        sold = user.added_to_sold_comic.order_by('-created_at')
    
    context = {
        'sold': sold,
    }
    return render(request, 'comic/sort_sold.html', context)


def edit_sold(request, id):
    context = {
		'comic': Comic.objects.get(id=id)
	}
    return render(request, 'comic/edit_sold.html', context)


def update_comic_sold(request, id):
    docfile = Comic.objects.get(id=id).docfile
    print('docfile: ', docfile)
    if request.method == "POST":
        print("*"*20)
        up_comic = Comic.objects.get(id=id)
        up_comic.title = request.POST['title']
        up_comic.desc = request.POST['desc']
        up_comic.qty = request.POST['qty']
        up_comic.price = request.POST['price']
        up_comic.price_sold = request.POST['price_sold'] 
        up_comic.date_of_purchase = request.POST['date_of_purchase']
        up_comic.date_of_sale = request.POST['date_of_sale']
        up_comic.creator = request.POST['creator']
        up_comic.year = request.POST['year']
        up_comic.cover = request.POST['cover']
        up_comic.docfile = docfile
        up_comic.save()

        return redirect('/sold', docfile="docfile")


def view_from_sold(request, id):
    comic = Comic.objects.get(id=id)
    profit = float(comic.price_sold) - float(comic.price)
    context = {
		'comic': Comic.objects.get(id=id),
        'profit': profit
	}
    print("$ ", profit)
    return render(request, 'comic/view_from_sold.html', context)


def destroy_from_sold(request, id):
    Comic.objects.get(id=id).delete()
    print('cancel ', id)
    return redirect('/sold')


def logout(request):
    request.session.flush()
    return redirect('/')
  