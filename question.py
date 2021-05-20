from flask import Flask, render_template, redirect, url_for, request, session, flash
from sqlalchemy.orm import aliased
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null, exc, and_
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app= Flask(__name__)
app.config['SECRET_KEY']= 'ilovetokeepsecret'
app.config["SQLALCHEMY_DATABASE_URI"]='mysql+mysqlconnector://root:@localhost/ques_answer'
db= SQLAlchemy(app)

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(50), unique=True, nullable=False)
    password= db.Column(db.String(300), nullable=False)
    admin= db.Column(db.Boolean, nullable=True, default=False)
    dttime= db.Column(db.DateTime(), server_default=db.func.now())
    question= db.relationship('Ques_ans', backref='questioner', lazy='dynamic', foreign_keys='Ques_ans.asked_by')
    answer= db.relationship('Ques_ans', backref='answerer', lazy='dynamic', foreign_keys='Ques_ans.answered_by')

class Ques_ans(db.Model):
    q_id= db.Column(db.Integer, primary_key=True)
    question= db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=True)
    asked_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    answered_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    qa_dttime= db.Column(db.DateTime(), server_default=db.func.now())

@app.route('/')
def index():
    asker= aliased(User)
    answerer= aliased(User)
    result= db.session.query(Ques_ans.q_id.label('id'),
                             Ques_ans.question.label('question'),
                             Ques_ans.answer.label('answer'),
                             asker.username.label('asked_by'),
                             answerer.username.label('answered_by')).\
        join(asker, asker.id == Ques_ans.asked_by).\
        join(answerer, answerer.id == Ques_ans.answered_by).\
        filter(Ques_ans.answer != None).order_by(Ques_ans.qa_dttime.desc())
    print("query", result)
    return render_template('index.html', result=result)

'''@app.route('/view_answer/<q_id>')
def view_answer(q_id):
    asker = aliased(User)
    answerer = aliased(User)
    result = db.session.query(Ques_ans.question.label('qid'), Ques_ans.question.label('question'),Ques_ans.answer.label('answer'), asker.username.label('asked_by'), answerer.username.label('answered_by')). \
        join(asker, asker.id == Ques_ans.asked_by).\
        join(answerer, answerer.id == Ques_ans.answered_by).\
        filter(Ques_ans.q_id == q_id).first()
    print("query", result)
    return render_template('view_answer.html', ans_res=result)
'''

@app.route('/give_answer/<q_id>', methods=['GET', 'POST'])
def give_answer(q_id):
    if request.method == 'POST':
        answer= request.form['answer']
        if answer:
            que= Ques_ans.query.get(q_id)
            que.answer= answer
            db.session.commit()
            flash("answer updated in database", "success")
            return redirect(url_for('index'))
        else:
            flash("Please provide answer", "error")
            return redirect(url_for('give_answer', q_id=q_id))
    else:
        asker = aliased(User)
        answerer = aliased(User)
        result = db.session.query(Ques_ans.q_id.label('qid'), Ques_ans.question.label('question'), Ques_ans.answer.label('answer'), asker.username.label('asked_by'), answerer.username.label('answered_by')). \
            join(asker, asker.id == Ques_ans.asked_by).\
            join(answerer, answerer.id == Ques_ans.answered_by).\
            filter(Ques_ans.q_id == q_id).first()
        print("query", result)
        return render_template('give_answer.html', ans_res=result)

@app.route('/ask_question', methods=['GET', 'POST'])
def ask_question():
    if 'logged_in' in session and session['logged_in'] == True:
        if request.method == 'POST':
            question= request.form['question']
            expert_id= int(request.form['expert'])
            if question and expert_id:
                res= Ques_ans(question=question, answered_by=expert_id, asked_by=session['user_id'])
                db.session.add(res)
                db.session.commit()
                return redirect(url_for('index'))
            else:
                flash("please enter the question", "error")
                return redirect(url_for('ask_question'))
        else:
            expert_list= User.query.filter_by(admin=1).all()
            print("expert", expert_list)
            return render_template('ask_question.html', expert_list=expert_list)
    else:
        flash("Please provide username and password", 'error')
        render_template(url_for('login'))

@app.route('/answer_question/')
def answer_question():
    if 'logged_in' in session and session['logged_in'] == True:
        asker = aliased(User)
        answerer = aliased(User)
        result=db.session.query(Ques_ans.question.label('question'), Ques_ans.answer.label('answer'), asker.username.label('asked_by'), answerer.username.label('answered_by')).\
            join(asker, asker.id == Ques_ans.asked_by). \
            join(answerer, answerer.id == Ques_ans.answered_by).\
            filter(Ques_ans.answer == null()). \
            filter(Ques_ans.answered_by == session['user_id']).all()
        return render_template('ppp.html', result=result)
    else:
        flash("Please provide username and password", 'error')
        render_template(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username= request.form['username']
        password= request.form['password']
#        print("passweor", password)
        if username and password:
            user_pwd= User.query.filter_by(username=username).first()
            print('user_pwd', user_pwd, user_pwd.password, user_pwd.admin, type(user_pwd.admin), int(user_pwd.admin))
            if user_pwd:
                if check_password_hash(user_pwd.password, password):
                    if user_pwd.admin == 1:
                        session['role']= 'admin'
                    else:
                        session['role']= 'user'
                    session['user']= user_pwd.username
                    session['user_id']= user_pwd.id
                    session['logged_in']= True
                    print("session admin", session['role'])
                    flash("You have logged in successfully", 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Authentication failed', 'error')
                    return redirect(url_for('login'))
            else:
                flash('Username is incorrect', 'error')
                return redirect(url_for('login'))
        else:
            flash("Please provide username and password", "error")
            return render_template(redirect('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name= request.form['username']
        password= request.form['password']
        cnf_pwd= request.form['cnfpass']
        if int(request.form['expt']) == 0:
            is_admin=0
        else:
            is_admin=1
        if name and password and cnf_pwd:
            if password == cnf_pwd:
                pwd_hash= generate_password_hash(password, method='sha256')
                user= User(username=name, password=pwd_hash, admin=is_admin, dttime=datetime.datetime.now())
                db.session.add(user)
                db.session.commit()
                flash("user created successfully", "success")
                return redirect(url_for('login'))
            else:
                flash("password does not match", "error")
                return redirect(url_for('register'))
        else:
            flash("Please fill all details", "error")
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('role', None)
    session.pop('role_stat', None)
    session.pop('user', None)
    session['logged_in'] = False
    session.pop('user_id', None)
    flash("you have logged out successfully", 'success')
    return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True)