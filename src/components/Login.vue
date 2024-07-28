<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-center mb-4">
      <button @click="setRole('user')" :class="{'btn-dark': role === 'user', 'btn-outline-dark': role !== 'user'}" class="btn mx-2">User</button>
      <button @click="setRole('librarian')" :class="{'btn-dark': role === 'librarian', 'btn-outline-dark': role !== 'librarian'}" class="btn mx-2">Librarian</button>
    </div>
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <div class="card p-4">
          <div class="row g-0">
            <div class="col-md-6">
              <img src="https://plus.unsplash.com/premium_photo-1684953432025-2933206ca61b?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" class="img-fluid rounded-start" alt="Register Image">
            </div>
            <div class="col-md-6">
              <div class="card-body">
                <h2 class="card-title mb-4">{{ cardTitle }}</h2>
                <form @submit.prevent="login">
                  <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" class="form-control" id="username" v-model="username" required>
                  </div>
                  <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" v-model="password" required>
                  </div>
                  <button type="submit" class="btn btn-dark">Login</button>
                </form>
              </div>
            </div>
          </div>
        </div>
        <div class="footer mt-4 text-center">
          <p>Not a registered user? <a href="/register">Register here</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      role: ''
    };
  },
  computed: {
    cardTitle() {
      return this.role ? `${this.role.charAt(0).toUpperCase() + this.role.slice(1)} Login` : 'Login';
    }
  },
  methods: {
    setRole(selectedRole) {
      this.role = selectedRole;
    },
    async login() {
      if (!this.role) {
        alert('Please select a role.');
        return;
      }
      try {
        const response = await fetch('http://localhost:5000/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
            role: this.role
          })
        });

        const data = await response.json();

        if (response.ok) {
          alert(data.message);
          localStorage.setItem('access_token', data.access_token);
          const userRole = data.role;
          if (userRole === 'librarian') {
            this.$router.push({ name: 'AdminDashboard' });
          } else if (userRole === 'user') {
            this.$router.push({ name: 'UserDashboard' });
          }
        } else {
          alert(data.message);
        }
      } catch (error) {
        alert('An error occurred.');
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1200px;
}

.card {
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.img-fluid {
  border-radius: 10px 0 0 10px;
  height: 100%;
  object-fit: cover;
}

.card-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card-title {
  font-size: 2.5rem;
  font-weight: bold;
}
</style>


