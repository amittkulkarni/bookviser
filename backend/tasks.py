from celery import shared_task
from flask import render_template
from flask_mail import Message
from backend import mail
from backend.models import User, BookIssue, Feedback
import pdfkit
from datetime import datetime, timedelta


@shared_task(ignore_result=False)
def generate_monthly_report():
    users = User.query.all()
    now = datetime.utcnow()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(seconds=1)

    for user in users:
        issued_books = BookIssue.query.filter(BookIssue.user_id == user.user_id,
                                              BookIssue.date_issued >= start_of_month,
                                              BookIssue.date_issued <= end_of_month).all()
        feedbacks = Feedback.query.filter(Feedback.user_id == user.user_id,
                                          Feedback.created_at >= start_of_month,
                                          Feedback.created_at <= end_of_month).all()
        report_html = render_template('report.html', user=user, issued_books=issued_books, feedbacks=feedbacks)
        pdf = pdfkit.from_string(report_html, False)

        msg = Message('Monthly Activity Report', sender='your-email@example.com', recipients=[user.email])
        msg.attach('report.pdf', 'application/pdf', pdf)
        mail.send(msg)


# @shared_task(name='celery.hello_world')
# def hello_world():
#     return 'hello world'


