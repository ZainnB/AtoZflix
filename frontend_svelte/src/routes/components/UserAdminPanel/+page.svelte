<script>
    import { onMount } from 'svelte';
    import { redirectToRegisterIfNotAuthenticated } from '../../../utils/auth.js';

    let selectedOption = 'users'; // Default to 'users'
    let data = null; // Holds fetched data
    let error = null;
    let updateUserData = { user_id: '', username: '', email: '', role: '' };

    const fetchData = async () => {
        error = null;
        try {
            const url = 'http://127.0.0.1:5000/api/get_all_users';
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const result = await response.json();
            data = result.users; // Assume API returns 'users' key
        } catch (err) {
            error = err.message;
        }
    };

    const deleteUser = async (user_id) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/delete_user?user_id=${user_id}&admin_id=1`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Failed to delete user');
            }

            fetchData();
            alert('User deleted successfully');
        } catch (err) {
            alert(err.message);
        }
    };

    const updateUser = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/update_user', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...updateUserData, admin_id: 1 }),
            });

            if (!response.ok) {
                throw new Error('Failed to update user');
            }

            fetchData();
            alert('User updated successfully');
            updateUserData = { user_id: '', username: '', email: '', role: '' };
        } catch (err) {
            alert(err.message);
        }
    };

    $: fetchData();

    onMount(() => {
        redirectToRegisterIfNotAuthenticated();
        fetchData();
    });
</script>

<div class="admin-wrapper">

    <div class="admin-panel">
        <h1 class="panel-title">User Admin Panel</h1>

        {#if error}
            <p class="error-message">{error}</p>
        {:else if data}
            <div class="data-table">
                <h2 class="table-title">Users</h2>
                <table>
                    <thead>
                        <tr>
                            <th>User ID</th>
                            <th>Username</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each data as user}
                            <tr>
                                <td>{user.user_id}</td>
                                <td>{user.username}</td>
                                <td>{user.email}</td>
                                <td>{user.role}</td>
                                <td class="action-buttons">
                                    <button class="btn delete-btn" on:click={() => deleteUser(user.user_id)}>Delete</button>
                                    <button class="btn update-btn" on:click={() => updateUserData = { user_id: user.user_id, username: user.username, email: user.email, role: user.role }}>Update</button>
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>

            {#if updateUserData.user_id}
                <div class="update-form">
                    <h3>Update User</h3>
                    <form on:submit|preventDefault={updateUser}>
                        <div class="form-group">
                            <label for="username">Username:</label>
                            <input id="username" type="text" bind:value={updateUserData.username} placeholder="Enter username" />
                        </div>
                        
                        <div class="form-group">
                            <label for="email">Email:</label>
                            <input id="email" type="email" bind:value={updateUserData.email} placeholder="Enter email" />
                        </div>
                        
                        <div class="form-group">
                            <label for="role">Role:</label>
                            <input id="role" type="text" bind:value={updateUserData.role} placeholder="Enter role" />
                        </div>
                        
                        <button class="btn submit-btn" type="submit">Update</button>
                    </form>
                </div>
            {/if}
        {:else}
            <p class="loading">Loading...</p>
        {/if}
    </div>
</div>

<style>
    .admin-wrapper {
        display: flex;
        height: 100vh;
        color: #f0f0f0;
        background-color: #121212;
    }

    .admin-panel {
        flex-grow: 1;
        padding: 20px;
        background-color: #1e1e1e;
    }

    .panel-title {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        color: #ffffff;
    }

    .data-table {
        margin-top: 1rem;
        border-radius: 8px;
        overflow: hidden;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        color: #ffffff;
        background-color: #1e1e1e;
    }

    th, td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #444;
    }

    th {
        background-color: #333;
    }

    .action-buttons {
        display: flex;
        gap: 10px;
    }

    .btn {
        padding: 8px 12px;
        font-size: 0.9rem;
        font-weight: bold;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .delete-btn {
        background-color: #d9534f;
        color: #fff;
    }

    .delete-btn:hover {
        background-color: #c9302c;
    }

    .update-btn {
        background-color: #5bc0de;
        color: #fff;
    }

    .update-btn:hover {
        background-color: #31b0d5;
    }

    .update-form {
        margin-top: 2rem;
        padding: 1rem;
        border-radius: 8px;
        background-color: #2c2c2c;
    }

    .form-group {
        margin-bottom: 1rem;
    }

    label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }

    input {
        width: 100%;
        padding: 10px;
        font-size: 0.9rem;
        color: #000;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    .submit-btn {
        background-color: #5cb85c;
        color: #fff;
    }

    .submit-btn:hover {
        background-color: #4cae4c;
    }

    .error-message {
        color: #d9534f;
        font-weight: bold;
        text-align: center;
    }

    .loading {
        text-align: center;
        font-weight: bold;
        color: #888;
    }
</style>
