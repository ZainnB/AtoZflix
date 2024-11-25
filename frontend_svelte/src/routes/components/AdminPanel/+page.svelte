<script>
    import { onMount } from 'svelte';

    let selectedOption = 'movies'; // Default to 'movies'
    let data = null; // Holds fetched data
    let error = null;
    let updateUserData = { user_id: '', username: '', email: '' }; // Data for updating user

    // Fetch data for the selected option
    const fetchData = async () => {
        error = null;  // Reset error before each fetch
        try {
            let url = '';
            if (selectedOption === 'movies') {
                url = 'http://127.0.0.1:5000/api/get_all_movies';
            } else if (selectedOption === 'users') {
                url = 'http://127.0.0.1:5000/api/get_all_users';
            }

            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const result = await response.json();
            data = result[selectedOption];  // Store fetched data based on selected option
        } catch (err) {
            error = err.message;
        }
    };

    // Delete user function
    const deleteUser = async (user_id) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/delete_user?user_id=${user_id}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Failed to delete user');
            }

            // Re-fetch data to reflect changes
            fetchData();
            alert('User deleted successfully');
        } catch (err) {
            alert(err.message);
        }
    };

    // Update user function
    const updateUser = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/update_user', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updateUserData)
            });

            if (!response.ok) {
                throw new Error('Failed to update user');
            }

            // Re-fetch data to reflect changes
            fetchData();
            alert('User updated successfully');
            updateUserData = { user_id: '', username: '', email: '' }; // Reset form
        } catch (err) {
            alert(err.message);
        }
    };

    // Watch for changes in selectedOption to fetch data when it changes
    $: selectedOption, fetchData();
    
    // Lifecycle: On component mount, fetch movies initially
    onMount(fetchData);
</script>

<!-- Admin Panel UI -->
<div class="admin-panel">
    <h1>Admin Panel</h1>
    
    <!-- Dropdown for selecting data type -->
    <select bind:value={selectedOption} class="data-select">
        <option value="movies">Movies</option>
        <option value="users">Users</option>
    </select>

    <!-- Displaying fetched data -->
    {#if error}
        <p class="error">{error}</p>
    {:else if data}
        <div class="data-table">
            {#if selectedOption === 'movies'}
                <h2>Movies</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Movie ID</th>
                            <th>Title</th>
                            <th>Release Date</th>
                            <th>Overview</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each data as movie}
                            <tr>
                                <td>{movie.movie_id}</td>
                                <td>{movie.title}</td>
                                <td>{movie.release_date}</td>
                                <td>{movie.overview}</td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            {:else if selectedOption === 'users'}
                <h2>Users</h2>
                <table>
                    <thead>
                        <tr>
                            <th>User ID</th>
                            <th>Username</th>
                            <th>Email</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each data as user}
                            <tr>
                                <td>{user.user_id}</td>
                                <td>{user.username}</td>
                                <td>{user.email}</td>
                                <td>
                                    <button on:click={() => deleteUser(user.user_id)}>Delete</button>
                                    <button on:click={() => updateUserData = { user_id: user.user_id, username: user.username, email: user.email }}>Update</button>
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>

                <!-- Update User Form -->
                {#if updateUserData.user_id}
                    <h3>Update User</h3>
                    <form on:submit|preventDefault={updateUser}>
                        <label>Username:</label>
                        <input type="text" bind:value={updateUserData.username} />
                        <label>Email:</label>
                        <input type="email" bind:value={updateUserData.email} />
                        <button type="submit">Update</button>
                    </form>
                {/if}
            {/if}
        </div>
    {:else}
        <p>Loading...</p>
    {/if}
</div>

<style>
    .admin-panel {
        padding: 20px;
        color: #fff;
        background-color: #121212;
        min-height: 100vh;
    }

    h1 {
        font-size: 2rem;
        margin-bottom: 20px;
    }

    .data-select {
        padding: 10px;
        font-size: 1rem;
        margin-bottom: 20px;
    }

    .data-table {
        overflow-x: auto;
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    th, td {
        padding: 12px;
        border: 1px solid #444;
        text-align: left;
    }

    th {
        background-color: #333;
    }

    .error {
        color: red;
    }

    button {
        padding: 5px 10px;
        margin-right: 10px;
        cursor: pointer;
    }

    button:hover {
        background-color: #444;
    }

    input[type="text"], input[type="email"] {
        padding: 8px;
        margin-bottom: 10px;
        width: 100%;
    }
</style>
