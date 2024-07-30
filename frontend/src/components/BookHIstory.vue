<template>
  <div class="book-history">
    <h2>Issue History for {{ book.name }}</h2>
    <div v-for="issue in book.issues" :key="issue.user_id">
      <p><strong>User:</strong> {{ issue.username }} ({{ issue.email }})</p>
      <p><strong>Date Issued:</strong> {{ formatDate(issue.date_issued) }}</p>
      <p><strong>Return Date:</strong> {{ formatDate(issue.return_date) }}</p>
      <p><strong>Status:</strong> {{ issue.status }}</p>
      <hr>
    </div>
    <button @click="goBack" class="btn btn-secondary">Back to Book List</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      book: {}
    };
  },
  created() {
    this.fetchBookHistory();
  },
  methods: {
    async fetchBookHistory() {
      const bookId = this.$route.params.bookId;
      const response = await fetch(`http://localhost:5000/api/admin/books/${bookId}/history`);
      const data = await response.json();
      this.book = data.book;
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    goBack() {
      this.$router.push({ name: 'Books' });
    }
  }
};
</script>
