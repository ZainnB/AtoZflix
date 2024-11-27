<script>
    import { onMount } from "svelte";
    import { redirectToRegisterIfNotAuthenticated } from "/src/utils/auth.js";
    import GeneralSlider2 from "../GenralSlider2/+page.svelte";
    import Navbar from "../Home/Navbar2.svelte";
    import SideBar from "../Home/SideBar.svelte";
    import Footer from "../Register/Footer1.svelte";
    import Line from "../Register/Line.svelte";

    // State variables
    let topCrew = [];
    const limit = 10;
    let sidebar = false;
    let searchQuery = "";

    onMount(async () => {
      redirectToRegisterIfNotAuthenticated();
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/top-crew?limit=${limit}`);
        if (!response.ok) {
          console.error("Failed to fetch top crew:", response.status);
          return;
        }

        const data = await response.json();
        if (data.status === "success") {
          topCrew = data.data || [];
        } else {
          console.error("Error in fetching crew:", data.message);
        }
      } catch (error) {
        console.error("Error fetching top crew:", error);
      }
    });

    const handleSearch = async () => {
        console.log("Search query:", searchQuery);
        if (searchQuery.trim()) {
            const type = "crew";
            window.location.href = `/components/searchActorOrCrew?type=${encodeURIComponent(type)}&query=${encodeURIComponent(searchQuery)}`;
        }
    };
  
    // Handle Enter key press
    const handleKeyDown = (event) => {
      if (event.key === "Enter") {
        handleSearch();
      }
    };
</script>

<div class="wrapper">
  <div class="navbar-wrapper">
      <Navbar />
  </div>
  <div class="sidebar-wrapper">
      <SideBar bind:open={sidebar} />
  </div>

  <div class="content">
    <!-- Search Bar Section -->
    <div class="search-section">
      <h2 class="search-heading">Search for Your Favorite Directors or Producers or Writers</h2>
      <div class="navbar-links">
        <input
          type="text"
          class="navbar-search"
          bind:value={searchQuery}
          placeholder="Search Directors/Producers/Writers..."
          on:keydown={handleKeyDown}
        />
      </div>
    </div>

    <h1>Top Directors/Producers/Writers</h1>

    {#each topCrew as { crew_id, crew_name, job_title }}
      <div class="crew-slider">
        <h2>{crew_name} - {job_title}</h2>
        <GeneralSlider2 
          api_name="crew-movies"
          type="crew" 
          value={crew_id} 
          limit={5} />
      </div>
    {/each}
  </div>

  <Line />
  <Footer />
</div>

<style>
  .wrapper {
    position: relative;
    min-height: 100vh;
    background-color: #121212;
    font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    overflow: hidden;
  }

  .navbar-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 10;
  }

  .sidebar-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
  }

  .search-section {
    text-align: center;
    margin: 20px 0;
  }

  .search-heading {
    color: #fff;
    font-size: 1.5rem;
    margin-bottom: 15px;
    font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
  }

  .navbar-links {
    display: flex;
    justify-content: center;
    margin: 0 auto;
  }

  .navbar-search {
    padding: 12px 20px;
    border-radius: 25px;
    border: 1px solid rgba(255, 255, 255, 0.5);
    background-color: rgba(15, 16, 20, 0.6);
    color: white;
    outline: none;
    width: 300px;
    transition: width 0.3s, background-color 0.3s;
    font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    font-size: 1rem;
  }

  .navbar-search:focus {
    width: 400px;
    background-color: rgba(15, 16, 20, 0.8);
  }

  .content {
    padding: 2rem 1rem;
    margin-top: 70px;
    color: #fff;
  }

  h1 {
    font-size: 2rem;
    text-align: left;
    margin: 20px 0;
  }

  .crew-slider {
    margin-bottom: 2rem;
    padding: 1rem;
    background-color: #1e1e1e;
    border-radius: 8px;
  }

  h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }

  @media (max-width: 768px) {
    .content {
      padding: 1rem;
    }

    .navbar-search {
      width: 250px;
    }

    .navbar-search:focus {
      width: 300px;
    }
  }
</style>
