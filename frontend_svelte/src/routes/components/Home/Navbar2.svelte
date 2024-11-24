<script>
  import { onMount } from 'svelte';
  export let logo = "/assets/img/logo.png";

  let searchQuery = "";

  const handleSearch = async () => {
    console.log("Search query:", searchQuery);
    if (searchQuery.trim()) {
      window.location.href = `/components/movieSearchResult?query=${encodeURIComponent(searchQuery)}`;
    }
  };

  // Handle Enter key press
  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleSearch();
    }
  };

  const handleLogout = () => {
<<<<<<< Updated upstream
  console.log("User logged out");

  // Clear all localStorage data
  localStorage.clear();

  // Optionally clear sessionStorage if you're using it
  sessionStorage.clear();

  // Redirect to homepage or login page
  window.location.href = "/";
};

=======
    console.log("User logged out");
    window.location.href = "/";
  };
>>>>>>> Stashed changes

</script>

<nav>
  <div class="nav-container">
    <button class="hamburger">&#9776;</button>
    <img src={logo} alt="Logo" class="logo" />
    <div class="navbar-links">
      <input
        type="text"
        class="navbar-search"
        bind:value={searchQuery}
        placeholder="Search movies..."
        on:keydown={handleKeyDown}
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
    z-index: 10;
  }

  .nav-container {
    max-width: 80vw;
    margin: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    z-index: 10;
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

  .hamburger {
    font-size: 30px;
    color: transparent;
    background: transparent;
    border: none;
  }

</style>
