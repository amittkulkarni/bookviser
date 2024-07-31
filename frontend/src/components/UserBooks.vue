<template>
  <div class="user-books">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/user/dashboard">Library Dashboard</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/user/dashboard" class="nav-link">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/book/issued" class="nav-link">Books</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/sections" class="nav-link">Sections</router-link>
            </li>
          </ul>
          <button class="btn btn-outline-light ms-auto" @click="logout">Logout</button>
        </div>
      </div>
    </nav>
    <h2 class="text-center my-4">Books Issued to You</h2>
    <div v-if="books.length === 0" class="text-center">
      <p>No books have been issued to you.</p>
    </div>
    <div v-else class="container">
      <div class="row">
        <div v-for="book in books" :key="book.book_id" class="col-md-3 mb-4">
          <div class="card">
            <img src="https://boxshot.com/3d-book-cover/how-to-make-a-3d-book-cover-in-photoshop/sample.jpg" class="card-img-top" alt="Book Cover">
            <div class="card-body">
              <h5 class="card-title">{{ book.name }}</h5>
              <p class="card-text"><strong>Author:</strong> {{ book.author }}</p>
              <p class="card-text"><strong>Section:</strong> {{ book.section }}</p>
              <p><strong>Date Issued:</strong> {{ formatDate(book.date_issued) }}</p>
              <p><strong>Return Date:</strong> {{ formatDate(book.return_date) }}</p>
              <div class="d-flex justify-content-between align-items-center">
                <button class="btn btn-primary" @click="readBook(book)">Read</button>
                <button class="btn btn-danger" @click="returnBook(book)">Return</button>
            </div>
            </div>
          </div>
        </div>
        <div class="modal fade" id="readBookModal" tabindex="-1" aria-labelledby="readBookModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="readBookModalLabel">{{ selectedBook.name }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>{{ selectedBook.content }}</p>
          </div>
        </div>
      </div>
    </div>
      </div>
    </div>
  </div>
</template>

<script>
import {Modal} from "bootstrap/js/index.esm.js";

export default {
  data() {
    return {
      books: [],
      selectedBook: {}
    };
  },
  created() {
    this.fetchIssuedBooks();
  },
  methods: {
    async fetchIssuedBooks() {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      try {
        const response = await fetch('http://localhost:5000/api/book/issued', {
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
          console.error('Failed to fetch issued books:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching issued books:', error);
      }
    },
    async returnBook(book) {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      try {
        const response = await fetch(`http://localhost:5000/api/book/issue/${book.book_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });
        if (response.ok) {
          alert(`Book returned successfully: ${book.name}`);
          await this.fetchIssuedBooks(); // Refresh the list
        } else {
          const errorData = await response.json();
          alert(`Failed to return book: ${errorData.message}`);
        }
      } catch (error) {
        alert(`Error returning book: ${error.message}`);
      }
    },
    async readBook(book) {
      this.selectedBook = book;
      console.log(book);
      const modal = new Modal(document.getElementById('readBookModal'));
      modal.show();
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
.user-books {
  padding-top: 70px; /* Adjust based on your navbar height */
}

.card-img-top {
  height: 150px;
  object-fit: cover;
}
</style>
