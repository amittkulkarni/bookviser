<template>
  <div class="librarian-dashboard">
    <!-- Navbar -->
    <Navbar :books-link="'/admin/books'" :dashboard-link="'/admin/dashboard'" :dashboard-text="'Librarian  Dashboard'" :show-search-bar="true" @search="searchRequests"/>
    <!-- Main Content -->
    <div class="container my-5">
      <h1 class="text-center mb-4">Manage Book Requests</h1>
      <div v-if="requests.length === 0" class="text-center">
        No book requests found.
      </div>
      <div v-else class="row">
        <div v-for="request in requests" :key="request.issue_id" class="col-md-6 mb-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ request.book.name }}</h5>
              <p class="card-text">
                <strong>User:</strong> {{ request.user.username }}<br>
                <strong>Email:</strong> {{ request.user.email }}<br>
                <strong>Author:</strong> {{ request.book.author }}<br>
                <strong>Status:</strong> {{ request.status }}<br>
                <strong>Date Issued:</strong> {{ formatDate(request.date_issued) }}<br>
                <strong>Return Date:</strong> {{ formatDate(request.return_date) }}
              </p>
              <div class="d-flex justify-content-between">
                <button v-if="request.status === 'requested'" @click="approveRequest(request.issue_id)" class="btn btn-success">Approve</button>
                <button v-if="request.status === 'requested'" @click="rejectRequest(request.issue_id)" class="btn btn-danger">Reject</button>
                <button v-if="request.status === 'issued'" @click="revokeRequest(request.issue_id)" class="btn btn-danger">Revoke</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";

export default {
  components: {Navbar},
  data() {
    return {
      requests: [],
      searchQuery: ''
    };
  },
  // computed: {
  //   filteredRequests() {
  //     return this.requests.filter(request =>
  //       request.book.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
  //       request.user.username.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
  //       request.user.email.toLowerCase().includes(this.searchQuery.toLowerCase())
  //     );
  //   }
  // },
  created() {
    this.fetchRequests();
  },
  methods: {
    async fetchRequests() {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch('http://localhost:5000/api/admin/requests', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      this.requests = data.requests;
    },
    formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  },
    async approveRequest(issue_id) {
      await this.updateRequestStatus(issue_id, 'approve');
    },
    async revokeRequest(issue_id) {
      await this.updateRequestStatus(issue_id, 'revoke');
    },
    async rejectRequest(issue_id) {
    await this.updateRequestStatus(issue_id, 'reject');
  },
    async updateRequestStatus(issue_id, action) {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch('http://localhost:5000/api/admin/requests', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ issue_id, action })
      });

      if (response.ok) {
        await this.fetchRequests();
      } else {
        console.error(`Failed to ${action} request`);
      }
    },
    async searchRequests(query) {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch(`http://localhost:5000/api/search/request?name=${encodeURIComponent(query)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        this.requests = data.requests;
      } else {
        console.error('Failed to search requests: ', response.statusText);
      }
    },
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push({ name: 'Login' });
    }
  }
};
</script>

<style scoped>
body, html, .librarian-dashboard {
  height: 100%;
  margin: 0;
}

.navbar {
  width: 100%;
  z-index: 1000;
}
</style>
