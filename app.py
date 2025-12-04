import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, User, Category, Budget, Expense
from sqlalchemy import func
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()


def createApp():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'sqlite:///expenses.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv('FLASK_SECRET', 'dev-secret')
    db.init_app(app)
    return app


app = createApp()


def sendEmailAlert(subject, body, to_addr=None):
    to_addr = to_addr or os.getenv('ALERT_EMAIL')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587)
                    ) if os.getenv('SMTP_PORT') else 587
    smtp_user = os.getenv('SMTP_USER')
    smtp_pass = os.getenv('SMTP_PASSWORD')
    if not smtp_server or not smtp_user or not smtp_pass or not to_addr:
        print('Email alert skipped: SMTP not fully configured or no recipient.')
        return
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = smtp_user
        msg['To'] = to_addr
        msg.set_content(body)
        with smtplib.SMTP(smtp_server, smtp_port) as s:
            s.starttls()
            s.login(smtp_user, smtp_pass)
            s.send_message(msg)
        print('Email sent to', to_addr)
    except Exception as e:
        print('Failed to send email:', e)


def checkBudgetsForCategory(category_id, year, month, added_amount=0):

    month_start = f"{year}-{month:02d}"
    total_q = db.session.query(func.sum(Expense.amount)).filter(
        Expense.category_id == category_id,
        func.strftime('%Y-%m', Expense.date) == month_start).scalar() or 0.0
    total = float(total_q) + float(added_amount)

    month_budget = Budget.query.filter_by(
        category_id=category_id, month_year=month_start).first()
    if month_budget:
        budget_amount = month_budget.amount
    else:
        general = Budget.query.filter_by(
            category_id=category_id, month_year=None).first()
        budget_amount = general.amount if general else None

    cat = Category.query.get(category_id)
    if budget_amount is not None:
        if total > budget_amount:
            subject = f"Budget Exceeded: {cat.name}"
            body = f"You have exceeded your budget for {month_start}.\nSpent: {total:.2f}\nBudget: {budget_amount:.2f}"
            print('ALERT:', body)
            sendEmailAlert(subject, body)
        else:
            remaining = budget_amount - total
            if remaining <= 0.1 * budget_amount:
                subject = f"Low Budget Remaining: {cat.name}"
                body = f"Only {remaining:.2f} left from budget {budget_amount:.2f} for {month_start}."
                print('ALERT low:', body)
                sendEmailAlert(subject, body)


@app.route('/')
def index():
    categories = Category.query.order_by(Category.name).all()
    recent = Expense.query.order_by(Expense.date.desc()).limit(10).all()
    cur_month = datetime.today().strftime('%Y-%m')
    month_total = db.session.query(func.sum(Expense.amount)).filter(
        func.strftime('%Y-%m', Expense.date) == cur_month).scalar() or 0.0
    return render_template('index.html', categories=categories, recent=recent, month_total=float(month_total), cur_month=cur_month)


@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    categories = Category.query.order_by(Category.name).all()
    if request.method == 'POST':
        user_name = request.form.get('user') or 'Default'
        user = User.query.filter_by(name=user_name).first()
        if not user:
            user = User(name=user_name, email=None)
            db.session.add(user)
            db.session.commit()
        try:
            category_id = int(request.form['category'])
            amount = float(request.form['amount'])
            if amount <= 0:
                flash('Amount must be positive', 'danger')
                return redirect(url_for('add_expense'))
        except Exception:
            flash('Invalid input', 'danger')
            return redirect(url_for('add_expense'))
        note = request.form.get('note')
        date_str = request.form.get(
            'date') or datetime.today().strftime('%Y-%m-%d')
        d = datetime.strptime(date_str, '%Y-%m-%d').date()
        shared = request.form.get('shared') or None
        exp = Expense(user_id=user.id, category_id=category_id,
                      amount=amount, note=note, date=d, shared_group=shared)
        db.session.add(exp)
        db.session.commit()

        checkBudgetsForCategory(
            category_id, d.year, d.month, added_amount=0)

        flash('Expense added', 'success')
        return redirect(url_for('index'))
    return render_template('add_expense.html', categories=categories)


@app.route('/budgets', methods=['GET', 'POST'])
def budgets():
    categories = Category.query.order_by(Category.name).all()
    if request.method == 'POST':
        try:
            cid = int(request.form['category'])
            amount = float(request.form['amount'])
            if amount <= 0:
                flash('Budget must be positive', 'danger')
                return redirect(url_for('budgets'))
        except Exception:
            flash('Invalid input', 'danger')
            return redirect(url_for('budgets'))
        month = request.form.get('month') or None
        b = Budget.query.filter_by(category_id=cid, month_year=month).first()
        if not b:
            b = Budget(category_id=cid, amount=amount, month_year=month)
            db.session.add(b)
        else:
            b.amount = amount
        db.session.commit()
        flash('Budget set', 'success')
        return redirect(url_for('budgets'))
    budgets = Budget.query.order_by(Budget.category_id).all()
    return render_template('budgets.html', categories=categories, budgets=budgets)


@app.route('/reports')
def reports():
    q = db.session.query(func.strftime('%Y-%m', Expense.date).label('m'),
                         func.sum(Expense.amount)).group_by('m').order_by('m')
    totals = [{'month': r[0], 'total': float(r[1])} for r in q]

    cur_month = datetime.today().strftime('%Y-%m')
    cat_data = []
    cats = Category.query.order_by(Category.name).all()
    for c in cats:
        spent = db.session.query(func.sum(Expense.amount)).filter(
            Expense.category_id == c.id,
            func.strftime('%Y-%m', Expense.date) == cur_month).scalar() or 0.0
        budget = Budget.query.filter_by(
            category_id=c.id, month_year=cur_month).first()
        if not budget:
            budget = Budget.query.filter_by(
                category_id=c.id, month_year=None).first()
        cat_data.append({'category': c.name, 'spent': float(
            spent), 'budget': budget.amount if budget else None})
    return render_template('reports.html', totals=totals, cat_data=cat_data, cur_month=cur_month)


@app.route('/api/add', methods=['POST'])
def api_add():
    data = request.json or {}
    required = ['user', 'category', 'amount']
    for r in required:
        if r not in data:
            return jsonify({'error': f'missing {r}'}), 400
    cat = Category.query.filter_by(name=data['category']).first()
    if not cat:
        return jsonify({'error': 'category not found'}), 404
    user = User.query.filter_by(name=data['user']).first()
    if not user:
        user = User(name=data['user'], email=None)
        db.session.add(user)
        db.session.commit()
    try:
        amount = float(data['amount'])
    except Exception:
        return jsonify({'error': 'invalid amount'}), 400
    exp = Expense(user_id=user.id, category_id=cat.id,
                  amount=amount, note=data.get('note'))
    db.session.add(exp)
    db.session.commit()
    checkBudgetsForCategory(cat.id, exp.date.year,
                            exp.date.month, added_amount=0)
    return jsonify({'status': 'ok'}), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)),
            debug=os.getenv('FLASK_ENV') == 'development')
