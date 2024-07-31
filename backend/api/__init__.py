from .resources import (UserRegister, UserLogin, LibrarianDashboard, UserActions, BookResource, SectionResource,
                        LibrarianUser, IssueBook, SearchBooks, BookRequests)
from backend import api


def initialize_api():
    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(LibrarianDashboard, '/admin/dashboard')
    api.add_resource(LibrarianUser, '/admin/users')
    api.add_resource(UserActions, '/admin/update-user')
    api.add_resource(BookResource, '/admin/books', '/admin/book/<int:book_id>')
    api.add_resource(SectionResource, '/admin/sections', '/admin/section/<int:section_id>')
    api.add_resource(IssueBook, '/book/issued', '/book/issue/<int:book_id>')
    api.add_resource(SearchBooks, '/search/book')
    api.add_resource(BookRequests, '/admin/requests')
