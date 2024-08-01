<template>
  <div class="admin-books">
    <!-- Navbar and Book List Section -->
    <Navbar :books-link="'/admin/books'" :dashboard-link="'/admin/dashboard'" :dashboard-text="'Librarian  Dashboard'" :show-search-bar="true" @search="searchBooks"/>

    <div class="container my-4">
      <h1 class="text-center mb-4">Library Books</h1>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">Books List</h2>
        <button class="btn btn-dark" @click="openAddBookModal">Add Book</button>
      </div>
      <div class="row">
        <div v-if="books.length === 0" class="col-12">
          <p class="text-center">No books available. Please add a new book.</p>
        </div>
        <div v-for="book in books" :key="book.book_id" class="col-md-4">
          <div class="card mb-4">
            <img src="https://boxshot.com/3d-book-cover/how-to-make-a-3d-book-cover-in-photoshop/sample.jpg" class="card-img-top" alt="Book Cover">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <h5 class="card-title mb-0">{{ book.name }}</h5>
                <button @click="viewDetails(book)" class="btn btn-dark">See Details</button>
              </div>
              <div class="d-flex justify-content-end">
                <button @click="editBook(book)" class="btn btn-secondary me-2">Edit</button>
                <button @click="deleteBook(book.book_id)" class="btn btn-danger">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Book Details Modal -->
    <!-- Book Details Modal -->
<div class="modal fade" id="bookDetailsModal" tabindex="-1" aria-labelledby="bookDetailsLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="bookDetailsLabel">{{ selectedBook.name }}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <p><strong>Author:</strong> {{ selectedBook.author }}</p>
        <p><strong>Section:</strong> {{ selectedBook.section }}</p>
        <p><strong>Content:</strong> {{ selectedBook.content }}</p>
        <p><strong>Available Copies:</strong> {{ selectedBook.available_copies }}</p>
        <hr>
        <h5>Issued To:</h5>
        <div v-if="selectedBook.issues.length === 0">
          <p>No issues found for this book.</p>
        </div>
        <div v-else>
          <div v-for="issue in selectedBook.issues" :key="issue.user_id">
            <p><strong>User:</strong> {{ issue.username }} ({{ issue.email }})</p>
            <p><strong>Date Issued:</strong> {{ formatDate(issue.date_issued) }}</p>
            <p><strong>Return Date:</strong> {{ formatDate(issue.return_date) }}</p>
            <p><strong>Status:</strong> {{ issue.status }}</p>
            <hr>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>


    <!-- Add/Edit Book Modal -->
    <div class="modal fade" id="addBookModal" tabindex="-1" aria-labelledby="addBookLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addBookLabel">{{ editMode ? 'Edit Book' : 'Add New Book' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editMode ? updateBook() : addBook()">
              <div class="mb-3">
                <label for="bookName" class="form-label">Book Name</label>
                <input type="text" class="form-control" id="bookName" v-model="newBook.name" required>
              </div>
              <div class="mb-3">
                <label for="bookAuthor" class="form-label">Author</label>
                <input type="text" class="form-control" id="bookAuthor" v-model="newBook.author" required>
              </div>
              <div class="mb-3">
                <label for="bookLanguage" class="form-label">Language</label>
                <input type="text" class="form-control" id="bookLanguage" v-model="newBook.language" value="English"
                       required>
              </div>
              <div class="mb-3">
                <label for="bookContent" class="form-label">Content</label>
                <textarea class="form-control" id="bookContent" v-model="newBook.content" required></textarea>
              </div>
              <div class="mb-3">
                <label for="bookSection" class="form-label">Section</label>
                <input type="text" class="form-control" id="bookSection" v-model="newBook.section" required>
              </div>
              <div class="mb-3">
                <label for="bookCopies" class="form-label">Available Copies (Optional)</label>
                <input type="number" class="form-control" id="bookCopies" v-model="newBook.available_copies">
              </div>
              <button type="submit" class="btn btn-primary">{{ editMode ? 'Update Book' : 'Add Book' }}</button>
            </form>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { Modal } from "bootstrap/js/index.esm.js";
import Navbar from "@/components/Navbar.vue";

export default {
  components: {Navbar},
  data() {
    return {
      books: [],
      selectedBook: {
        issues: []
      },
      newBook: {
        name: '',
        author: '',
        language: 'English',
        content: '',
        section: '',
        available_copies: 1,
      },
      editMode: false,
      searchQuery: ''
    };
  },
  created() {
    this.fetchBooks();
  },
  methods: {
    async fetchBooks() {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch('http://localhost:5000/api/admin/books', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      this.books = data.books;
    },
    viewDetails(book) {
      this.selectedBook = book;
      const modal = new Modal(document.getElementById('bookDetailsModal'));
      modal.show();
    },
    openAddBookModal() {
      this.newBook = {
        name: '',
        author: '',
        language: 'English',
        content: '',
        section: '',
        available_copies: 1,
      };
      this.editMode = false;
      const modal = new Modal(document.getElementById('addBookModal'));
      modal.show();
    },
    async addBook() {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch('http://localhost:5000/api/admin/books', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(this.newBook)
      });
      if (response.ok) {
        await this.fetchBooks();
        const modal = Modal.getInstance(document.getElementById('addBookModal'));
        modal.hide();
      } else {
        console.error('Failed to add book');
      }
    },
    editBook(book) {
      this.newBook = { ...book };
      this.editMode = true;
      const modal = new Modal(document.getElementById('addBookModal'));
      modal.show();
    },
    async updateBook() {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch(`http://localhost:5000/api/admin/book/${this.newBook.book_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(this.newBook)
      });
      if (response.ok) {
        await this.fetchBooks();
        const modal = Modal.getInstance(document.getElementById('addBookModal'));
        modal.hide();
      } else {
        console.error('Failed to update book');
      }
    },
    async searchBooks(query) {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch(`http://localhost:5000/api/search/book?name=${encodeURIComponent(query)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        this.books = data.books;
      } else {
        console.error('Failed to search books: ', response.statusText);
      }
    },
    async deleteBook(book_id) {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch(`http://localhost:5000/api/admin/book/${book_id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        await this.fetchBooks();
      } else {
        console.error('Failed to delete book');
      }
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push({ name: 'Login' });
    }
  }
};
</script>

<style scoped>
body, html, .admin-books {
  height: 100%;
  margin: 0;
}

.navbar {
  width: 100%;
  z-index: 1000;
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}
</style>
