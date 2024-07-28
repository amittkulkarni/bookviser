from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from backend.models import User, Book, Section
from backend import db
from .parsers import user_parse


class UserRegister(Resource):
    def post(self):
        data = user_parse()
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
        data = user_parse()
        user = User.query.filter_by(username=data['username'], role=data['role']).first()
        if user and user.password == data['password']:
            access_token = create_access_token(identity={'username': user.username, 'role': user.role})
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
            'available_copies': book.available_copies
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

class InfluencerAdRequestActions(Resource):
    @jwt_required()
    def put(self, ad_request_id):
        args = ad_request_parser.parse_args()
        ad_request = AdRequest.query.get(ad_request_id)
        if not ad_request:
            return {'message': 'Ad request not found'}, 404

        current_user = get_jwt_identity()
        if current_user['role'] != 'Influencer' or ad_request.influencer_id != current_user['id']:
            return {'message': 'Influencer access required'}, 403

        ad_request.status = args['status']
        ad_request.payment_amount = args['payment_amount']
        db.session.commit()
        return {'message': 'Ad request updated successfully.'}, 200


class SearchBooks(Resource):
    @jwt_required()
    def get(self):
        args = request.args
        books = Book.query.filter(Book.name.like(f"%{args.get('name', '')}%")).all()
        return {'books': [ book.as_dict() for book in books]}, 200


class SearchUsers(Resource):
    @jwt_required()
    def get(self):
        args = request.args
        blacklisted_users = User.query.filter_by(role='user', flag=False).filter(
            User.username.like(f"%{args.get('name', '')}%")).all()

        whitelisted_users = User.query.filter_by(role='user', flag=True).filter(
            User.username.like(f"%{args.get('name', '')}%")).all()
        return {'whitelistedUsers': [user.as_dict() for user in whitelisted_users],
                'blacklistedUsers': [user.as_dict() for user in blacklisted_users]}, 200