from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
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
def new_item():
    # TODO: Create a GroceryItemForm
    item_form = GroceryItemForm()

    # TODO: If form was submitted and was valid:
    # - create a new GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
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

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_item.html', form=item_form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    # TODO: Create a GroceryStoreForm and pass in `obj=store`
    
    if store is None:
        flash('Store not found.')
        return redirect(url_for('main.homepage'))

    # TODO: If form was submitted and was valid:
    # - update the GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.
    
    form = GroceryStoreForm(obj=store)
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        db.session.commit()
        flash('Store was updated successfully.')
        return redirect(url_for('main.store_detail', store_id=store.id))

    # TODO: Send the form to the template and use it to render the form fields
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

