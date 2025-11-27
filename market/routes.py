from flask import render_template, redirect, url_for, flash, request
from market import app, db
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename


# ---------------- HOME PAGE ----------------
@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")


# ---------------- MARKET PAGE ----------------
@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()

    if request.method == "POST":
        # BUY ITEM
        purchased_item_name = request.form.get("purchased_item")
        item_object = Item.query.filter_by(name=purchased_item_name).first()

        if item_object and current_user.can_purchase(item_object):
            item_object.buy(current_user)
            flash(f"Successfully purchased {item_object.name}!", "success")
        else:
            flash("Not enough money to purchase this item.", "danger")

        # SELL ITEM
        sold_item_name = request.form.get("sold_item")
        sell_item_object = Item.query.filter_by(name=sold_item_name).first()

        if sell_item_object and current_user.can_sell(sell_item_object):
            sell_item_object.sell(current_user)
            flash(f"You sold {sell_item_object.name}.", "success")

        return redirect(url_for('market_page'))

    # GET — show items
    items = Item.query.filter_by(owner=None).all()
    owned_items = Item.query.filter_by(owner=current_user.id).all()

    return render_template(
        "market.html",
        items=items,
        owned_items=owned_items,
        purchase_form=purchase_form,
        selling_form=sell_form
    )


# ---------------- REGISTER PAGE ----------------
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Account created successfully!", "success")
        return redirect(url_for('market_page'))

    if form.errors:
        for error in form.errors.values():
            flash(error[0], "danger")

    return render_template("register.html", form=form)


# ---------------- LOGIN PAGE ----------------
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()

        if attempted_user and attempted_user.check_password(form.password.data):
            login_user(attempted_user)
            flash(f"Welcome back, {attempted_user.username}!", "success")
            return redirect(url_for('market_page'))
        else:
            flash("Incorrect username or password!", "danger")

    return render_template("login.html", form=form)


# ---------------- LOGOUT ----------------
@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home_page"))


# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Access denied!", "danger")
        return redirect(url_for("market_page"))

    products = Item.query.all()
    users = User.query.all()

    return render_template("admin/admin_dashboard.html", products=products, users=users)


# ---------------- ADMIN ADD PRODUCT ----------------
@app.route('/admin/add', methods=['GET', 'POST'])
@login_required
def admin_add_item():
    if not current_user.is_admin:
        return redirect(url_for("market_page"))

    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        barcode = request.form.get("barcode")
        description = request.form.get("description")
        image_file = request.files.get("image")

        image_path = None

        # Save Uploaded Image
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(save_path)
            image_path = f"/static/product_images/{filename}"

        # Save Item to DB
        new_item = Item(
            name=name,
            price=price,
            barcode=barcode,
            description=description,
            image=image_path
        )

        db.session.add(new_item)
        db.session.commit()

        flash("Item added successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("admin/add_item.html")


# ---------------- ADMIN DELETE PRODUCT ----------------
@app.route('/admin/delete/<int:item_id>')
@login_required
def admin_delete_item(item_id):
    if not current_user.is_admin:
        return redirect(url_for("market_page"))

    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Item deleted!", "info")

    return redirect(url_for('admin_dashboard'))


# ---------------- ADMIN EDIT PRODUCT ----------------
@app.route('/admin/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_item(item_id):
    if not current_user.is_admin:
        return redirect(url_for("market_page"))

    item = Item.query.get(item_id)

    if request.method == "POST":
        item.name = request.form.get("name")
        item.price = request.form.get("price")
        item.barcode = request.form.get("barcode")
        item.description = request.form.get("description")

        image_file = request.files.get("image")
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(save_path)
            item.image = f"/static/product_images/{filename}"

        db.session.commit()
        flash("Item updated successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("admin/edit_item.html", item=item)
