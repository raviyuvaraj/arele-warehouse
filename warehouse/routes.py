from warehouse import app, db, User, Item, LoginManager
from flask import render_template,redirect,url_for,flash,request
# from warehouse.models import Item
from warehouse.forms import RegisterForm ,LoginForm, MoveItemForm,ReturnItemForm
from flask_login import login_user,logout_user,login_required,current_user

@app.route('/')

@app.route('/home')
def homepage():
    return render_template('homepage.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(first_name=form.first_name.data,
                               last_name=form.last_name.data,
                                email=form.email.data,
                                password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created Successfully Logged in as {user_to_create.first_name}')
        return redirect(url_for('homepage'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error creating user: {err_msg}',category='danger')
    return render_template('register.html',form=form)
 

@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_email = User.query.filter_by(email = form.email.data).first()
        # attempted_password = User.query.filter_by(password_hash = form.password.data).first()
        if attempted_email and attempted_email.check_password_correction(form.password.data):
            login_user(attempted_email)
            flash('Success! Logged in', category='success')
            return redirect(url_for('products'))
        else:
            flash(f"Email and password don't match",category='danger')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash(f"You've been Logged Out",category='info')
    return redirect(url_for('homepage'))



@app.route('/Products',methods=['POST','GET'])
@login_required
def products():
    move_form = MoveItemForm()
    transfer_form = ReturnItemForm()
    if request.method == 'POST':
        #  move item
        moved_item = request.form.get('moved_item')
        m_item_object = Item.query.filter_by(Product=moved_item).first()
        if m_item_object:
            m_item_object.owner = current_user.id
            # db.session.add(m_item_object.owner)
            db.session.commit()
            flash(f"Thank you we have transferred the item to your Warehouse...", category='success')
            return redirect(url_for('products'))
        
        
        
        # Return item
        return_item = request.form.get('return_item')
        r_item_object =Item.query.filter_by(Product=return_item).first()
        if r_item_object:
            if current_user.can_return(r_item_object):
                r_item_object.owner = None
                # db.session.add(r_item_object)
                db.session.commit()
                flash("Succesfully returned item to inventory!",category='success')
            else:
                flash(f"You don't have the item to return",category='danger')
            
        return redirect(url_for('products'))
 
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('Products.html',items=items,move_form=move_form,owned_items=owned_items,transfer_form=transfer_form)


