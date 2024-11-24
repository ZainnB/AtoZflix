<!-- <script>
    import MovieCard from "../Slider/movie_card.svelte";
    import CountrySlider from "../GenreSlider/+page.svelte";
    import Navbar from "../Home/Navbar2.svelte";
    import SideBar from "../Home/SideBar.svelte";
    import Footer from "../Register/Footer1.svelte";
    import Line from "../Register/Line.svelte";
    import { onMount } from "svelte";
  
    let country_list;
    let movies = [];
    let sidebar = false;
  
    // Fetch country list on component mount
    onMount(async () => {
        const response = await fetch("http://127.0.0.1:5000/api/get_country_names");
        if (!response.ok) {
            console.error("Failed to fetch country list");
            return;
        }
        const data = await response.json();
        country_list = data.countries;
    });
  
    let selectedcountry = null;
  
    // Function to handle country selection
    function selectcountry(country) {
        selectedcountry = country;
        getMovieBycountry(country); // Fetch movies when country is selected
    }
  
    // Fetch movies based on selected country
    const getMovieBycountry = async (country) => {
        const response = await fetch(`http://127.0.0.1:5000/api/country?country=${country}`);
        if (!response.ok) {
            console.error("Failed to fetch country movies");
            return;
        }
        const data = await response.json();
        movies = data.movies;
    };
  </script>
  
  <div class="wrapper">
    <div class="navbar-wrapper">
        <Navbar />
    </div>
    <div class="sidebar-wrapper">
        <SideBar bind:open={sidebar} />
    </div>
    <div class="country_container">
        country List Section -->
        <!-- <div class="country_buttons">
            {#each country_list as country}
                <button on:click={() => selectcountry(country)} class:selected={selectedcountry === country}>
                    {country}
                </button>
            {/each}
        </div>
   -->
        <!-- Movie Section -->
        <!-- <div class="movie_container">
          <h1> {selectedcountry} </h1>
            {#if movies.length > 0}
                <div class="movies-grid">
                  {#each movies as { poster_path, movie_id }}
                    <MovieCard poster_path={poster_path} movie_id={movie_id} />
                  {/each}
                </div>
            {:else}
              {#each country_list as country}
                <CountrySlider type="country" value={country} limit={10} heading={country} />
              {/each}
            {/if}
        </div>
    </div>
    <Line />
    <Footer />
  </div>
  
  <style>
    .wrapper {
        position: relative;
        min-height: 100vh;
        overflow: hidden;
        background-color: #121212;
        font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
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
  
    .country_container {
        display: grid;
        grid-template-columns: 15% 85%; /* Make the country column thinner */
        height: calc(100vh - 70px); /* Adjust height to exclude navbar height */
        margin-top: 70px;
    }
  
    .country_buttons {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        padding: 1rem 0.5rem;
        background-color: #141414;
        color: #fff;
        overflow-y: auto;
        scrollbar-width: thin; /* For Firefox */
        scrollbar-color: #064E45 #121212;
    }
  
    .country_buttons::-webkit-scrollbar {
        width: 8px;
    }
  
    .country_buttons::-webkit-scrollbar-thumb {
        background-color: #064E45;
        border-radius: 10px;
    }
  
    .country_buttons::-webkit-scrollbar-track {
        background-color: #121212;
    }
  
    button {
        padding: 10px;
        background-color: transparent; /* Transparent by default */
        border: 1px solid transparent;
        border-radius: 5px;
        cursor: pointer;
        margin-bottom: 10px;
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
        color: #fff;
        font-size: 1rem;
        text-align: left;
    }
  
    button:hover {
        background-color: #064E45;
        border-color: #064E45;
    }
  
    button.selected {
        background-color: #098577;
        border-color: #098577;
        color: #fff;
    }
  
    .movie_container {
        padding: 1rem;
        background-color: #141414;
        color: #fff;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: #064E45 #121212;
    }
  
    .movies-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); /* Responsive grid */
        gap: 0.5rem;
        justify-content: center;
    }
  
    .movies-grid::-webkit-scrollbar {
        width: 8px;
    }
  
    .movies-grid::-webkit-scrollbar-thumb {
        background-color: #064E45;
        border-radius: 10px;
    }
  
    .movies-grid::-webkit-scrollbar-track {
        background-color: #121212;
    }
  
    @media (max-width: 768px) {
        .country_container {
            grid-template-columns: 1fr;
            grid-template-rows: auto 1fr;
        }
    } -->
  <!-- </style>-->