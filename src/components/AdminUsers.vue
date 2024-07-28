<template>
  <div class="admin-users">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Admin Dashboard</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link to="/admin/dashboard" class="nav-link">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/admin/books">Books</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/admin/sections">Sections</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/admin/users">Users</a>
            </li>
          </ul>
          <form class="d-flex" @submit.prevent="searchUsers">
            <input class="form-control me-2" type="search" placeholder="Search Users" v-model="searchQuery" aria-label="Search">
            <button class="btn btn-outline-light" type="submit">Search</button>
          </form>
        </div>
        <button class="btn btn-outline-light ms-3" @click="logout">Logout</button>
      </div>
    </nav>

    <div class="container-fluid mt-5 pt-4">
      <div class="row">
        <div class="col-12">
          <h2>Blacklisted Users</h2>
          <div v-if="blacklistedUsers.length === 0" class="alert alert-info">
            No Blacklisted Users.
          </div>
          <table v-else class="table table-hover">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in blacklistedUsers" :key="user.id">
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.role }}</td>
                <td>
                  <button class="btn btn-success" @click="whitelistUser(user.user_id)">Whitelist</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="row mt-5">
        <div class="col-12">
          <h2>Users</h2>
          <div v-if="whitelistedUsers.length === 0" class="alert alert-info">
            No Users Found.
          </div>
          <table v-else class="table table-hover">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in whitelistedUsers" :key="user.id">
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.role }}</td>
                <td>
                  <button class="btn btn-danger" @click="blacklistUser(user.user_id)">Flag</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminUsers',
  data() {
    return {
      whitelistedUsers: [],
      blacklistedUsers: [],
      searchQuery: '',
      isSearchActive: false // Flag to indicate if search is active
    };
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch('http://localhost:5000/api/admin/users', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      this.blacklistedUsers = data.blacklistedUsers;
      this.whitelistedUsers = data.whitelistedUsers;
    },
    async searchUsers() {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch(`http://localhost:5000/api/search/user?name=${this.searchQuery}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      this.whitelistedUsers = data.whitelistedUsers;
      this.blacklistedUsers = data.blacklistedUsers;
      this.isSearchActive = true;
    },
    async updateUser(userId, action) {
      const token = localStorage.getItem('access_token');
      await fetch('http://localhost:5000/api/admin/update-user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ user_id: userId, action })
      });
      await this.fetchUsers();
    },
    whitelistUser(userId) {
      this.updateUser(userId, 'whitelist');
    },
    blacklistUser(userId) {
      this.updateUser(userId, 'flag');
    },
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push({ name: 'Login' });
    }
  }
};
</script>

<style scoped>
body, html, .admin-users {
  height: 100%;
  margin: 0;
}

.navbar {
  width: 100%;
  z-index: 1000;
}

.table-hover tbody tr:hover {
  background-color: #f5f5f5;
}

.btn {
  margin-right: 5px;
}
</style>
