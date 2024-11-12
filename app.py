from flask import Flask, jsonify, render_template, request, redirect, url_for, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from forms import ClientForm
from models import User, Client
from dbs import db
from flask import Flask, render_template, jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@127.0.0.1/admin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']="waayaabee"

db.init_app(app)   
with app.app_context():
    db.create_all()  # Create tables in the database

@app.route('/')
def home():
    return render_template('dashboard/index.html')

@app.route('/api/clients')  
def get_clients():
    # Query the database for user data
    clients = Client.query.all()
    client_list = [client.to_dict() for client in clients]
    return jsonify(client_list)
    
@app.route('/report')
def show_report():
    return render_template("client/client_report.html")

# Datatable data fetch
@app.route('/api/search-options', methods=['GET'])
def search_options():
    # Get search term from Select2 (if provided)
    search_term = request.args.get('q', '')

    # Query the database and filter by the search term
    if search_term:
        clients = Client.query.filter(Client.clientname.ilike(f'%{search_term}%')).all()
    else:
        clients = Client.query.all()

    # Format data for Select2
    client_data = [client.to_select2() for client in clients]

    # Return data in a format compatible with Select2
    return jsonify({"results": client_data})



@app.route('/client')
def client():
    result = Client.query.all()
    return render_template('client/client.html', data=result)


@app.route("/client/add", methods=['GET', 'POST'])
def client_add():
    form = ClientForm()
    if form.validate_on_submit():
       new_client = Client()
       form.populate_obj(new_client)
       new_client.save()
       return redirect(url_for('client'))
    return render_template("client/client_add.html", form=form )

@app.route('/client/edit/<client_id>', methods=['GET', 'POST'])
def client_edit(client_id):
    data=Client.query.get(client_id)
    form = ClientForm(obj=data)
    if form.validate_on_submit():
        form.populate_obj(data)
        data.save()
        return redirect(url_for('client'))
    return render_template('client/client_edit.html',form=form)

@app.route('/client/delete/<client_id>', methods=['GET', 'POST'])
def client_delete(client_id):
    data=Client.query.get(client_id)
    form = ClientForm(obj=data)
    if form.validate_on_submit():
        form.populate_obj(data)
        data.delete()  
        return redirect(url_for('client')) 
    return render_template('client/client_delete.html', form=form)

@app.route('/user')
def user():
    result = User.query.all()
    return render_template('user/user.html', data=result)


@app.route('/user/add', methods=['GET', 'POST'])
def user_add():
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['email']
        user_type = request.form['user_type']
        
        data = User(username=username, full_name=fullname, email=email, user_type=user_type, is_active=True)
        data.save()
        return redirect(url_for('user'))

    return render_template('user/user_add.html', data=[])


@app.route('/user/edit/<user_id>', methods=['GET', 'POST'])
def user_edit(user_id):
    data = User.query.get(user_id)
    if request.method == 'POST':
        data.username = request.form['username']
        data.full_name = request.form['fullname']
        data.email = request.form['email']
        data.user_type = request.form['user_type']
        data.save()
        return redirect(url_for('user'))
    return render_template('user/user_edit.html', data=data)

@app.route('/user/delete/<user_id>', methods=['GET', 'POST'])
def user_delete(user_id):
    data = User.query.get(user_id)
    if request.method == 'POST':
        data.delete()
        return redirect(url_for('user'))
    return render_template('user/user_delete.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
