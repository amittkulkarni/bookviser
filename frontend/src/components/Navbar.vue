<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
      <router-link class="navbar-brand" :to="dashboardLink">{{ dashboardText }}</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link :to="dashboardLink" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link :to="booksLink" class="nav-link">Books</router-link>
          </li>
          <li v-if="dashboardLink === '/admin/dashboard'" class="nav-item">
            <router-link to="/admin/sections" class="nav-link">Sections</router-link>
          </li>
          <li v-if="dashboardLink === '/admin/dashboard'" class="nav-item">
            <router-link to="/admin/users" class="nav-link">Users</router-link>
          </li>
          <li v-if="dashboardLink === '/admin/dashboard'" class="nav-item">
            <router-link to="/admin/requests" class="nav-link">Requests</router-link>
          </li>
        </ul>
        <div class="ms-auto d-flex align-items-center">
          <form v-if="showSearchBar" class="d-flex me-3" @submit.prevent="$emit('search', searchQuery)">
            <input class="form-control me-2" type="search" placeholder="Search" v-model="searchQuery" aria-label="Search">
            <button class="btn btn-outline-light" type="submit">Search</button>
          </form>
          <button class="btn btn-outline-light" @click="logout">Logout</button>
        </div>      </div>
    </div>
  </nav>
</template>

<script>
export default {
  props: {
    dashboardLink: {
      type: String,
      default: '/user/dashboard'
    },
    dashboardText: {
      type: String,
      default: 'Library Dashboard'
    },
    booksLink: {
      type: String,
      default: '/book/issued'
    },
    showSearchBar: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      searchQuery: '',
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push({ name: 'Login' });
    }
  }
};
</script>

<style scoped>
.navbar {
  width: 100%;
  z-index: 1000;
}
</style>

