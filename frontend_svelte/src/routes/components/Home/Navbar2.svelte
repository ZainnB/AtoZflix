<script>
  // import { onMount } from 'svelte';
  export let logo = "/assets/img/logo.png";

  let searchQuery = "";
  export let isSidebarOpen = false;

  const handleSearch = () => {
    console.log("Searching for:", searchQuery);
  };

  const toggleSidebar = () => {
    isSidebarOpen = !isSidebarOpen;
  };

  const handleLogout = () => {
    console.log("User logged out");
    window.location.href = "/"; // Redirect to homepage or login
  };

</script>

<nav>
  <div class="nav-container">
    <button class="hamburger" on:click={toggleSidebar}>&#9776;</button>
    <img src={logo} alt="Logo" class="logo" />
    <div class="navbar-links">
      <input
        type="text"
        class="navbar-search"
        bind:value={searchQuery}
        placeholder="Search movies..."
      />
    </div>
    <button class="logout-btn" on:click={handleLogout}>Logout</button>
  </div>
</nav>


<style>
  /* Navbar */
  nav {
    width: 100%;
    height: auto;
    background: linear-gradient(to bottom, rgba(0, 0, 0, 0.842), rgba(0, 0, 0, 0.064)); /* Transparent gradient */
    padding: 10px 0;
    position: relative;
  }

  .nav-container {
    max-width: 80vw;
    margin: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
  }

  .logo {
    width: 140px;
    height: auto;
    margin-right: 20px; /* Space between logo and sidebar button */
  }

  .navbar-links {
    flex-grow: 1;
    display: flex;
    justify-content: center;
  }

  .navbar-search {
    padding: 8px 15px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.5);
    background-color: rgba(15, 16, 20, 0.5);
    color: white;
    outline: none;
    width: 200px;
    transition: width 0.3s, background-color 0.3s;
    font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
  }

  .navbar-search:focus {
    width: 300px;
    background-color: rgba(15, 16, 20, 0.7);
  }

  .logout-btn {
    background-color: #098577;
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s, transform 0.2s;
    font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
  }

  .logout-btn:hover {
    background-color: #064e45;
    transform: scale(1.05);
  }

  /* Hamburger Icon */
  .hamburger {
    font-size: 30px;
    color: white;
    background: transparent;
    border: none;
    cursor: pointer;
    transition: color 0.3s;
  }

  .hamburger:hover {
    color: #1abc9c; /* Hover effect for the hamburger icon */
  }

  /* Sidebar
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 250px;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.9);
    display: flex;
    flex-direction: column;
    padding-top: 60px;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease-out;
  }

  .sidebar ul {
    list-style: none;
    padding: 0;
  }

  .sidebar ul li {
    padding: 15px;
    border-bottom: 1px solid #444;
  }

  .sidebar ul li:last-child {
    border-bottom: none;
  }

  .sidebar ul li p {
    color: white;
    font-size: 20px;
    font-weight: 500;
    text-align: center;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .sidebar ul li p:hover {
    background-color: rgba(26, 188, 156, 0.5); /* Hover effect for list items */
  /* } */

  /* Sidebar Transition */
  /* .sidebar {
    transform: translateX(-100%);
  }

  .sidebar-active {
    transform: translateX(0); /* Move sidebar into view */
  /* } */
</style>
