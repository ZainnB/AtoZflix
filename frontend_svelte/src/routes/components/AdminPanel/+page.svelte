<script>
    import { goto } from '$app/navigation';
</script>

<div class="admin-home-wrapper">
    <Navbar />
    <SideBar />

    <div class="content">
        <h1>Admin Dashboard</h1>
        <div class="navigation">
            <button on:click={() => goto('/AdminPanel/MovieAdminPanel')}>Go to Movie Admin Panel</button>
            <button on:click={() => goto('/AdminPanel/UserAdminPanel')}>Go to User Admin Panel</button>
        </div>
    </div>
</div>

<style>
    .admin-home-wrapper {
        background-color: #121212;
        color: #fff;
        min-height: 100vh;
        padding: 20px;
    }

    .content {
        text-align: center;
    }

    .navigation button {
        background-color: #098577;
        color: #fff;
        padding: 10px 20px;
        margin: 10px;
        border: none;
        cursor: pointer;
    }

    .navigation button:hover {
        background-color: #064E45;
    }
</style>
