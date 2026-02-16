<template>

    <div class = "container">
      <div class = "d-flex gap-3 flex-column">
        <div>
          <button>HI</button>
        </div>
        <div>
          <button>Hello</button>
        </div>
      </div>
    </div>
    <h3>I am working</h3>
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
    Launch demo modal
    </button>

    <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Modal Title</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                <div class="modal-body">
                    This is the modal body content.
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary">Save changes</button>
                    <button><RouterLink to = '/'>Go Home</RouterLink></button>
                </div>
            </div>
        </div>
    </div>


  <div class="container mt-4">
    <h2>User List with Collapsible Rows</h2>
    
    <table class="table table-hover">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        <template v-for="(user, index) in users" :key="user.id">
          <!-- Main row -->
          <tr>
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>
              <button 
                class="btn btn-sm" 
                :class="expandedRows[index] ? 'btn-secondary' : 'btn-info'"
                @click="toggleRow(index)"
              >
                {{ expandedRows[index] ? '▲ Hide' : '▼ More Info' }}
              </button>
            </td>
          </tr>
          
          <!-- Collapsible detail row - using v-show -->
          <tr v-show="expandedRows[index]" class="detail-row">
            <td colspan="4">
              <div class="details-content p-3">
                <div class="row">
                  <div class="col-md-6">
                    <p><strong>Phone:</strong> {{ user.phone }}</p>
                    <p><strong>Company:</strong> {{ user.company }}</p>
                  </div>
                  <div class="col-md-6">
                    <p><strong>Address:</strong> {{ user.address }}</p>
                    <p><strong>Website:</strong> 
                      <a :href="'http://' + user.website" target="_blank" class="text-decoration-none">
                        {{ user.website }}
                      </a>
                    </p>
                  </div>
                </div>
              </div>
            </td>
          </tr>
          
        </template>
      </tbody>
    </table>

    <div class="mt-3">
      <button class="btn btn-sm btn-outline-success me-2" @click="expandAll">
        Expand All
      </button>
      <button class="btn btn-sm btn-outline-warning" @click="collapseAll">
        Collapse All
      </button>
    </div>
  </div>

</template>

<script setup>
    import { ref, reactive } from 'vue'

    // Using an object for better performance with v-show
    const expandedRows = ref({})

    // Toggle row expansion
    const toggleRow = (index) => {
    expandedRows.value[index] = !expandedRows.value[index]
    }

    // Expand all rows
    const expandAll = () => {
    users.forEach((_, index) => {
        expandedRows.value[index] = true
    })
    }

    // Collapse all rows
    const collapseAll = () => {
    users.forEach((_, index) => {
        expandedRows.value[index] = false
    })
    }

    // Sample data
    const users = reactive([
    {
        id: 1,
        name: 'John Doe',
        email: 'john@example.com',
        phone: '+1 234 567 890',
        company: 'ABC Corp',
        address: '123 Main St, New York',
        website: 'johndoe.com'
    },
    {
        id: 2,
        name: 'Jane Smith',
        email: 'jane@example.com',
        phone: '+1 987 654 321',
        company: 'XYZ Ltd',
        address: '456 Oak Ave, London',
        website: 'janesmith.com'
    },
    {
        id: 3,
        name: 'Bob Johnson',
        email: 'bob@example.com',
        phone: '+1 555 123 456',
        company: 'Tech Solutions',
        address: '789 Pine Rd, Tokyo',
        website: 'bobjohnson.com'
    }
    ])
</script>

<style scoped>
    .detail-row {
    background-color: #f8f9fa;
    border-left: 4px solid #17a2b8;
    }

    .details-content {
    background-color: #f8f9fa;
    animation: slideDown 0.3s ease-out;
    }

    @keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
    }

    .btn {
    transition: all 0.2s ease;
    }
</style>
