<script>
    import { redirectToRegisterIfNotAuthenticated } from "../../../utils/auth.js";
  import MovieCard from "../Slider/movie_card.svelte";
  import GenreSlider from "../GenreSlider/+page.svelte";
  import Navbar from "../Home/Navbar2.svelte";
  import SideBar from "../Home/SideBar.svelte";
  import Footer from "../Register/Footer1.svelte";
  import Line from "../Register/Line.svelte";
  import { onMount } from "svelte";

  let genre_list;
  let movies = [];
  let sidebar = false;

  // Fetch genre list on component mount
  onMount(async () => {
    redirectToRegisterIfNotAuthenticated();
      const response = await fetch("http://127.0.0.1:5000/api/get_genre_names");
      if (!response.ok) {
          console.error("Failed to fetch genre list");
          return;
      }
      const data = await response.json();
      genre_list = data.genres;
  });

  let selectedGenre = null;

  // Function to handle genre selection
  function selectGenre(genre) {
      selectedGenre = genre;
      getMovieByGenre(genre); // Fetch movies when genre is selected
  }

  // Fetch movies based on selected genre
  const getMovieByGenre = async (genre) => {
      const response = await fetch(`http://127.0.0.1:5000/api/genre?genre=${genre}`);
      if (!response.ok) {
          console.error("Failed to fetch genre movies");
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
  <div class="genre_container">
      <!-- Genre List Section -->
      <div class="genre_buttons">
          {#each genre_list as genre}
              <button on:click={() => selectGenre(genre)} class:selected={selectedGenre === genre}>
                  {genre}
              </button>
          {/each}
      </div>

      <!-- Movie Section -->
      <div class="movie_container">
        <h1> {selectedGenre} </h1>
          {#if movies.length > 0}
              <div class="movies-grid">
                {#each movies as { poster_path, movie_id }}
                  <MovieCard poster_path={poster_path} movie_id={movie_id} />
                {/each}
              </div>
          {:else}
              {#each genre_list as genre}
                  <GenreSlider genre={genre} limit={10} heading={genre} />
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

  .genre_container {
      display: grid;
      grid-template-columns: 15% 85%; /* Make the genre column thinner */
      height: calc(100vh - 70px); /* Adjust height to exclude navbar height */
      margin-top: 70px;
  }

  .genre_buttons {
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

  .genre_buttons::-webkit-scrollbar {
      width: 8px;
  }

  .genre_buttons::-webkit-scrollbar-thumb {
      background-color: #064E45;
      border-radius: 10px;
  }

  .genre_buttons::-webkit-scrollbar-track {
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
      .genre_container {
          grid-template-columns: 1fr;
          grid-template-rows: auto 1fr;
      }
  }
</style>
