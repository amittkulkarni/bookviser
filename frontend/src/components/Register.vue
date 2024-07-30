<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <div class="card p-4">
          <div class="row g-0">
            <div class="col-md-6">
              <img src="https://plus.unsplash.com/premium_photo-1684953432025-2933206ca61b?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" class="img-fluid rounded-start" alt="Register Image">
            </div>
            <div class="col-md-6">
              <div class="card-body">
                <h2 class="card-title mb-4">Register</h2>
                <form @submit.prevent="register">
                  <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" class="form-control" id="username" v-model="username" required>
                  </div>
                  <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control" id="email" v-model="email" required>
                  </div>
                  <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" v-model="password" required>
                  </div>
                  <button type="submit" class="btn btn-dark">Register</button>
                </form>
              </div>
            </div>
          </div>
        </div>
        <div class="footer mt-4 text-center">
          <p>Already a registered user? <a href="/login">Login here</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: '',
    };
  },
  methods: {
    async register() {
      try {
        const response = await fetch('http://localhost:5000/api/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password,
          })
        });

        const data = await response.json();

        if (response.status === 201) {
          alert(data.message);
          this.$router.push({name: 'Login'});
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
