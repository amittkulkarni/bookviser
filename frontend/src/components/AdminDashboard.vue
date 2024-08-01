<template>
  <div class="admin-dashboard">
    <Navbar :books-link="'/admin/books'" :dashboard-link="'/admin/dashboard'" :dashboard-text="'Librarian Dashboard'"></Navbar>

    <div class="container-fluid mt-5 pt-4 full-height">
      <div class="row full-height">
        <div class="col-12 col-md-3 mb-4">
          <div class="card shadow-lg full-height">
            <div class="card-body">
              <h3 class="card-title">Ad Requests</h3>
              <p class="card-text">{{ adRequests }}</p>
            </div>
          </div>
        </div>
        <div class="col-12 col-md-3 mb-4">
          <div class="card shadow-lg full-height">
            <div class="card-body">
              <h3 class="card-title">Campaigns</h3>
              <p class="card-text">{{ campaigns }}</p>
            </div>
          </div>
        </div>
        <div class="col-12 col-md-3 mb-4">
          <div class="card shadow-lg full-height">
            <div class="card-body">
              <h3 class="card-title">Influencers</h3>
              <p class="card-text">{{ influencers }}</p>
            </div>
          </div>
        </div>
        <div class="col-12 col-md-3 mb-4">
          <div class="card shadow-lg full-height">
            <div class="card-body">
              <h3 class="card-title">Sponsors</h3>
              <p class="card-text">{{ sponsors }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="row full-height">
        <div class="col-12 col-md-4 mb-4">
          <div class="card shadow-lg full-height">
            <div class="card-body">
              <h5 class="card-title">Graph 1</h5>
              <GraphComponent :data="graphData1" />
            </div>
          </div>
        </div>
        <div class="col-12 col-md-4 mb-4">
          <div class="card shadow-lg full-height">
            <div class="card-body">
              <h3 class="card-title">Graph 2</h3>
              <GraphComponent :data="graphData2" />
            </div>
          </div>
        </div>
        <div class="col-12 col-md-4 mb-4">
          <div class="card shadow-lg full-height">
            <div class="card-body">
              <h5 class="card-title">Graph 3</h5>
              <GraphComponent :data="graphData3" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import GraphComponent from './Graph.vue';
import Navbar from "@/components/Navbar.vue";

export default {
  components: {
    Navbar,
    GraphComponent
  },
  data() {
    return {
      adRequests: 0,
      campaigns: 0,
      influencers: 0,
      sponsors: 0,
      graphData1: {
        labels: ['January', 'February', 'March', 'April', 'May'],
        datasets: [{
          label: 'Ad Requests',
          backgroundColor: '#42A5F5',
          data: [65, 59, 80, 81, 56]
        }]
      },
      graphData2: {
        labels: ['January', 'February', 'March', 'April', 'May'],
        datasets: [{
          label: 'Campaigns',
          backgroundColor: '#66BB6A',
          data: [28, 48, 40, 19, 86]
        }]
      },
      graphData3: {
        labels: ['January', 'February', 'March', 'April', 'May'],
        datasets: [{
          label: 'Users',
          backgroundColor: '#FFA726',
          data: [18, 48, 77, 9, 100]
        }]
      }
    };
  },
  mounted() {
    this.fetchDashboardData();
  },
  methods: {
    async fetchDashboardData() {
       const token = localStorage.getItem('access_token');
      try {
        const response = await fetch('http://localhost:5000/api/admin/dashboard', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        this.adRequests = data.adRequests;
        this.campaigns = data.campaigns;
        this.influencers = data.influencers;
        this.sponsors = data.sponsors;
      } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
      }
    },
    logout() {
      localStorage.removeItem('access_token')
      this.$router.push({name: 'Login'});
    }
  }
};
</script>

<style scoped>
body, html, .admin-dashboard {
  height: 100%;
  margin: 0;
}

.navbar {
  width: 100%;
  z-index: 1000;
}


.full-height {
  height: 100%;
}

.card {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.5rem;
  font-weight: bold;
}
</style>
