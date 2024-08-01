<template>
  <div class="user-dashboard">
    <!-- Navbar -->
    <Navbar :show-search-bar="true"/>

    <!-- Books Section -->
    <div class="container my-4 pt-5">
      <h2 class="text-center mb-4">Books</h2>
      <div class="row">
        <div v-if="books.length === 0" class="col-12">
          <p class="text-center">No books available.</p>
        </div>
        <div v-for="book in paginatedBooks" :key="book.book_id" class="col-md-3 mb-4">
          <div class="card">
            <img src="https://boxshot.com/3d-book-cover/how-to-make-a-3d-book-cover-in-photoshop/sample.jpg" class="card-img-top" alt="Book Cover">
            <div class="card-body">
              <h5 class="card-title">{{ book.name }}</h5>
              <p class="card-text"><strong>Author:</strong> {{ book.author }}</p>
              <p class="card-text"><strong>Section:</strong> {{ book.section }}</p>
              <div class="d-flex justify-content-between align-items-center">
                <button v-if="book.status === 'returned'" @click="requestBook(book)" class="btn btn-dark">Request</button>
                <button v-if="book.status === 'requested'" class="btn btn-dark" disabled>Requested</button>
                <button v-if="book.status === 'issued'" class="btn btn-dark" disabled>In Shelf</button>
                <button @click="viewDetails(book)" class="btn btn-warning">See Details</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="text-center">
        <button class="btn btn-dark me-2" @click="prevPage" :disabled="currentPage === 1">Previous</button>
        <button class="btn btn-dark" @click="nextPage" :disabled="!hasMoreBooks">Next</button>
      </div>
    </div>

    <!-- Sections Section -->
    <div class="container my-4">
      <h2 class="text-center mb-4">Sections</h2>
      <div class="row">
        <div v-for="section in sections" :key="section.section_id" class="col-md-3 mb-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ section.name }}</h5>
              <p class="card-text">{{ section.description }}</p>
              <button @click="viewSectionBooks(section)" class="btn btn-dark">View Books</button>
            </div>
          </div>
        </div>
      </div>
    </div>

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
            <p><strong>Available Copies:</strong> {{ selectedBook.available_copies }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
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
      sections: [],
      selectedBook: {},
      currentPage: 1,
      pageSize: 4,
    };
  },
  computed: {
    paginatedBooks() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = this.currentPage * this.pageSize;
      return this.books.slice(start, end);
    },
    hasMoreBooks() {
      return this.books.length > this.currentPage * this.pageSize;
    }
  },
  created() {
    this.fetchBooks();
    this.fetchSections();
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
      this.books = data.books.map(book => {
      let status = 'returned';
      if (book.issues && book.issues.length > 0) {
        const latestIssue = book.issues[book.issues.length - 1];
        if (latestIssue.status === 'requested') {
          status = 'requested';
        } else if (latestIssue.status === 'issued') {
          status = 'issued';
        }
      }
      return { ...book, status };
    });
    },
    async fetchSections() {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch('http://localhost:5000/api/admin/sections', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      this.sections = data.sections;
    },
    nextPage() {
      if (this.hasMoreBooks) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    async requestBook(book) {
    const token = localStorage.getItem('access_token');
    if (!token) {
      this.logout();
      return;
    }
    try {
      const response = await fetch(`http://localhost:5000/api/book/issue/${book.book_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ book_id: book.book_id })
      });

      if (response.ok) {
        book.status = 'requested';
        alert(`Book requested successfully: ${book.name}`);
      } else {
        const errorData = await response.json();
        alert(`Failed to request book: ${errorData.message}`);
      }
    } catch (error) {
      alert(`Error requesting book: ${error.message}`);
    }
  },

    viewDetails(book) {
      this.selectedBook = book;
      const modal = new Modal(document.getElementById('bookDetailsModal'));
      modal.show();
    },
    viewSectionBooks(section) {
      this.books = this.books.filter(book => book.section_id === section.section_id);
      this.currentPage = 1;
    },
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push({ name: 'Login' });
    }
  }
};
</script>
<style scoped>
body, html, .user-dashboard {
  height: 100%;
  margin: 0;
}

.navbar {
  width: 100%;
  z-index: 1000;
}

.card-img-top {
  height: 150px;
  object-fit: cover;
}
</style>
