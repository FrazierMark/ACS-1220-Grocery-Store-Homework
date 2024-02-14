from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db
from grocery_app.forms import SignUpForm
from grocery_app.models import User
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from grocery_app.forms import LoginForm
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)
bcrypt = Bcrypt()

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    form = GroceryStoreForm()
    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data
        )
        db.session.add(new_store)
        db.session.commit()
        flash('New store was added successfully.')
        return redirect(url_for('main.store_detail', store_id=new_store.id))

    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    item_form = GroceryItemForm()
    
    if item_form.validate_on_submit():
        new_item = GroceryItem(
            name=item_form.name.data,
            price=item_form.price.data,
            category=item_form.category.data,
            photo_url=item_form.photo_url.data,
            store=item_form.store.data
        )
        db.session.add(new_item)
        db.session.commit()
        flash('New item was added successfully.')
        return redirect(url_for('main.item_detail', item_id=new_item.id))

    return render_template('new_item.html', form=item_form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    
    if store is None:
        flash('Store not found.')
        return redirect(url_for('main.homepage'))

    form = GroceryStoreForm(obj=store)
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        db.session.commit()
        flash('Store was updated successfully.')
        return redirect(url_for('main.store_detail', store_id=store.id))

    store = GroceryStore.query.get(store_id)
    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    
    if item is None:
        flash('Error retrieving item.')
        return redirect(url_for('main.homepage'))
    
    form = GroceryItemForm(obj=item)
    
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data
        db.session.commit()
        
        flash('Item was updated successfully.')
        return redirect(url_for('main.item_detail', item_id=item.id))
    
    return render_template('item_detail.html', item=item, form=form)

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
def add_to_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    current_user.shopping_list_users.append(item)
    db.session.add(current_user)
    db.session.commit()
    flash('Item successfully added to your shopping list!')
    return redirect(url_for('main.shopping_list', item_id=item_id))

@main.route('/shopping_list')
@login_required
def shopping_list():
    shopping_list = current_user.shopping_list_users
    return render_template("shopping_list.html", shopping_list=shopping_list)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))

    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))