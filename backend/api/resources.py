from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from backend.models import User, Book, Section, BookIssue
from backend import db


class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'], password=data['password'], role=data['role'])
        try:
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User registered successfully.'}, 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Username or Email already exists. Please choose a different username or email.'}, 400
        finally:
            db.session.remove()


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username'], role=data['role']).first()
        if user and user.password == data['password']:
            access_token = create_access_token(identity={'username': user.username, 'id': user.user_id, 'role': user.role})
            return {'message': 'Login Successful', 'access_token': access_token, 'role': user.role}, 200
        return {'message': 'Invalid credentials'}, 401


class LibrarianDashboard(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Librarian access required'}, 403

        users = User.query.filter_by(role='user')
        books = Book.query.all()
        sections = Section.query.all()
        return {
            'users': len(users),
            'books': len(books),
            'sections': len(sections)
        }


class LibrarianUser(Resource):
    @jwt_required()
    def get(self):
        whitelisted_users = User.query.filter_by(role='user', flag=True).all()
        blacklisted_users = User.query.filter_by(role='user', flag=False).all()
        return {
            'whitelistedUsers': [user.as_dict() for user in whitelisted_users],
            'blacklistedUsers': [user.as_dict() for user in blacklisted_users]
        }, 200


class UserActions(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = data['user_id']
        action = data['action']
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        if action == 'whitelist':
            user.flag = True
            db.session.commit()
            return {'message': 'User is whitelisted successfully'}, 200
        elif action == 'flag':
            user.flag = False
            db.session.commit()
            return {'message': 'User is blacklisted successfully'}, 200
        else:
            return {'message': 'invalid action'}, 400


class BookResource(Resource):
    @jwt_required()
    def get(self):
        books = Book.query.all()
        books_list = [{
            'book_id': book.book_id,
            'section': book.section.name,
            'name': book.name,
            'content': book.content,
            'author': book.author,
            'language':  book.language,
            'date_added': book.date_added.isoformat(),
            'available_copies': book.available_copies,
            'issues': [{
                'user_id': issue.user_id,
                'username': issue.user.username,
                'email': issue.user.email,
                'date_issued': issue.date_issued.isoformat(),
                'return_date': issue.return_date.isoformat(),
                'status': issue.status
            } for issue in book.issues]
        } for book in books]
        return {'books': books_list}, 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        name = data.get('name')
        content = data.get('content')
        author = data.get('author')
        language = data.get('language', 'English')
        available_copies = data.get('available_copies', 1)
        section_name = data.get('section')
        section = Section.query.filter_by(name=section_name).first()
        if not all([name, content, author, section]):
            return {'message': 'Missing required fields'}, 400

        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Librarian access required'}, 403
        new_book = Book(name=name, content=content, author=author, language=language, available_copies=available_copies, section_id=section.section_id)
        db.session.add(new_book)
        db.session.commit()
        return {'message': 'Book added successfully.'}, 201

    @jwt_required()
    def put(self, book_id):
        data = request.get_json()
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404
        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Librarian access required'}, 403
        book.name = data.get('name')
        book.content = data.get('content')
        book.author = data.get('author')
        book.language = data.get('language')
        book.available_copies = data.get('available_copies')
        book.section_id = Section.query.filter_by(name=data.get('section')).first().section_id
        db.session.commit()
        return {'message': 'Book updated successfully.'}, 200

    @jwt_required()
    def delete(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404

        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Unauthorized'}, 403

        db.session.delete(book)
        db.session.commit()
        db.session.close()
        return {'message': 'Book deleted successfully.'}, 200


class SectionResource(Resource):
    @jwt_required()
    def get(self):
        sections = Section.query.all()
        sections_list = [{
            'section_id': section.section_id,
            'name': section.name,
            'description': section.description
        } for section in sections]
        return {'sections': sections_list}, 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Librarian access required'}, 403

        new_section = Section(name=name, description=description)
        db.session.add(new_section)
        db.session.commit()
        return {'message': 'Section created successfully.'}, 201

    @jwt_required()
    def put(self, section_id):
        data = request.get_json()
        section = Section.query.get(section_id)
        if not section:
            return {'message': 'Section not found'}, 404

        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Unauthorized'}, 403

        section.name = data.get('name')
        section.description = data.get('description')
        db.session.commit()
        return {'message': 'Section updated successfully.'}, 200

    @jwt_required()
    def delete(self, section_id):
        section = Section.query.get(section_id)
        if not section:
            return {'message': 'Section not found'}, 404

        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Unauthorized'}, 403

        db.session.delete(section)
        db.session.commit()
        return {'message': 'Section deleted successfully.'}, 200


class IssueBook(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        issued_books = BookIssue.query.filter_by(user_id=current_user['id'], status='issued').all()
        return {'books': [{
            'book_id': issue.book_id,
            'name': issue.book.name,
            'author': issue.book.author,
            'date_issued': issue.date_issued.isoformat(),
            'return_date': issue.return_date.isoformat() if issue.return_date else None,
            'content': issue.book.content,
            'section': issue.book.section.name,
            'status': issue.status
        }
            for issue in issued_books]}, 200

    @jwt_required()
    def post(self, book_id):
        book = Book.query.get(book_id)
        current_books = (BookIssue.query.filter_by(user_id=get_jwt_identity()['id'])
                         .filter(BookIssue.status.in_(['issued', 'requested'])).count())
        if current_books >= 5:
            return {'message': 'Maximum number of book request reached'}, 400
        if not book:
            return {'message': 'Book not found'}, 404
        if book.available_copies <= 0:
            return {'message': 'Book out of stock'}, 400
        current_user = get_jwt_identity()
        existing_issue = BookIssue.query.filter_by(book_id=book_id, user_id=current_user['id'], status='requested').first()
        if existing_issue:
            return {'message': 'Book already requested'}, 400
        book_issue = BookIssue(book_id=book.book_id, user_id=current_user['id'], status='requested')
        book_issue.set_return_date(14)
        book.available_copies -= 1
        db.session.add(book_issue)
        db.session.commit()
        return {'message': 'Book issued successfully.'}, 200

    @jwt_required()
    def put(self, book_id):
        req = BookIssue.query.filter_by(book_id=book_id, user_id=get_jwt_identity()['id'], status='issued').first()
        if not req:
            return {'message': 'Request not found'}, 404
        req.status = 'returned'
        book = Book.query.get(req.book_id)
        if book:
            book.available_copies += 1
        db.session.commit()
        return {'message': 'Book returned successfully.'}, 200


class SearchBooks(Resource):
    @jwt_required()
    def get(self):
        args = request.args
        books = Book.query.filter(Book.name.ilike(f"%{args.get('name', '')}%")).all()
        return {'books': [book.as_dict() for book in books]}, 200


class SearchRequests(Resource):
    @jwt_required()
    def get(self):
        query = request.args.get('name', '').strip()
        requests = BookIssue.query.join(User).join(Book).filter(
            (User.username.ilike(f"%{query}%")) |
            (Book.name.ilike(f"%{query}%"))
        ).all()
        return {'requests': [req.as_dict() for req in requests]}, 200


class BookRequests(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user['role'] != 'librarian':
            return {'message': 'Librarian access required'}, 403
        book_requests = BookIssue.query.order_by(BookIssue.date_issued.desc()).all()
        result = []
        for req in book_requests:
            user = User.query.get(req.user_id)
            book = Book.query.get(req.book_id)
            result.append({
                'issue_id': req.issue_id,
                'user': {
                    'user_id': user.user_id,
                    'username': user.username,
                    'email': user.email
                },
                'book': {
                    'book_id': book.book_id,
                    'name': book.name,
                    'author': book.author
                },
                'date_issued': req.date_issued.isoformat(),
                'return_date': req.return_date.isoformat() if req.return_date else None,
                'status': req.status
            })

        return {'requests': result}, 200

    @jwt_required()
    def put(self):
        data = request.get_json()
        issue_id = data.get('issue_id')
        action = data.get('action')
        req = BookIssue.query.get(issue_id)
        if not req:
            return {'message': 'Request not found'}, 404
        if action == 'approve':
            req.status = 'issued'
        elif action == 'revoke':
            req.status = 'returned'
            book = Book.query.get(req.book_id)
            if book:
                book.available_copies += 1
        elif action == 'reject':
            db.session.delete(req)
            db.session.commit()
            return {'message': 'Request rejected successfully.'}, 200
        db.session.commit()
        return {'message': 'Request updated successfully.'}, 200
