<template>
  <div class="admin-sections">
    <!-- Navbar and Section List Section -->
    <Navbar :books-link="'/admin/books'" :dashboard-link="'/admin/dashboard'" :dashboard-text="'Librarian  Dashboard'"/>
    <div class="container my-4">
      <h1 class="text-center mb-4">Library Sections</h1>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">Sections List</h2>
        <button class="btn btn-dark" @click="openAddSectionModal">Add Section</button>
      </div>
      <div class="row">
        <div v-if="sections.length === 0" class="col-12">
          <p class="text-center">No sections available. Please add a new section.</p>
        </div>
        <div v-for="section in sections" :key="section.section_id" class="col-md-4">
          <div class="card mb-4">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <h5 class="card-title mb-0">{{ section.name }}</h5>
                <button @click="viewDetails(section)" class="btn btn-dark">See Details</button>
              </div>
              <p class="card-text">{{ section.description }}</p>
              <div class="d-flex justify-content-end">
                <button @click="editSection(section)" class="btn btn-secondary me-2">Edit</button>
                <button @click="deleteSection(section.section_id)" class="btn btn-danger">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Section Details Modal -->
    <div class="modal fade" id="sectionDetailsModal" tabindex="-1" aria-labelledby="sectionDetailsLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="sectionDetailsLabel">{{ selectedSection.name }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p><strong>Description:</strong> {{ selectedSection.description }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Section Modal -->
    <div class="modal fade" id="addSectionModal" tabindex="-1" aria-labelledby="addSectionLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addSectionLabel">{{ editMode ? 'Edit Section' : 'Add New Section' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editMode ? updateSection() : addSection()">
              <div class="mb-3">
                <label for="sectionName" class="form-label">Section Name</label>
                <input type="text" class="form-control" id="sectionName" v-model="newSection.name" required>
              </div>
              <div class="mb-3">
                <label for="sectionDescription" class="form-label">Description</label>
                <textarea class="form-control" id="sectionDescription" v-model="newSection.description" required></textarea>
              </div>
              <button type="submit" class="btn btn-primary">{{ editMode ? 'Update Section' : 'Add Section' }}</button>
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
      sections: [],
      selectedSection: {},
      newSection: {
        name: '',
        description: '',
      },
      editMode: false,
    };
  },
  created() {
    this.fetchSections();
  },
  methods: {
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
    viewDetails(section) {
      this.selectedSection = section;
      const modal = new Modal(document.getElementById('sectionDetailsModal'));
      modal.show();
    },
    openAddSectionModal() {
      this.newSection = {
        name: '',
        description: '',
      };
      this.editMode = false;
      const modal = new Modal(document.getElementById('addSectionModal'));
      modal.show();
    },
    async addSection() {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch('http://localhost:5000/api/admin/sections', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(this.newSection)
      });
      if (response.ok) {
        await this.fetchSections();
        const modal = Modal.getInstance(document.getElementById('addSectionModal'));
        modal.hide();
      } else {
        console.error('Failed to add section');
      }
    },
    editSection(section) {
      this.newSection = { ...section };
      this.editMode = true;
      const modal = new Modal(document.getElementById('addSectionModal'));
      modal.show();
    },
    async updateSection() {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch(`http://localhost:5000/api/admin/section/${this.newSection.section_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(this.newSection)
      });
      if (response.ok) {
        await this.fetchSections();
        const modal = Modal.getInstance(document.getElementById('addSectionModal'));
        modal.hide();
      } else {
        console.error('Failed to update section');
      }
    },
    async deleteSection(section_id) {
      const token = localStorage.getItem('access_token');
      if (!token) {
        this.logout();
        return;
      }
      const response = await fetch(`http://localhost:5000/api/admin/section/${section_id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        await this.fetchSections();
      } else {
        console.error('Failed to delete section');
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
body, html, .admin-sections {
  height: 100%;
  margin: 0;
}

.navbar {
  width: 100%;
  z-index: 1000;
}

.card {
  margin-bottom: 20px;
}
</style>
