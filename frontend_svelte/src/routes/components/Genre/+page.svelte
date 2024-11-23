<script>
    import MovieCard from "../Slider/movie_card.svelte";
    import { onMount } from "svelte";
    
    let genre_list;
    let movies = [];
    
    // Fetch genre list on component mount
    onMount(async () => {
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
      <p>Selected Genre: {selectedGenre}</p>
      <!-- Render MovieCards based on selected genre -->
      {#if movies.length > 0}
        <div class="movies-grid">
          {#each movies as movie}
            <MovieCard poster_path={movie.poster_path} />
          {/each}
        </div>
      {:else}
        <p>No movies available for the selected genre.</p>
      {/if}
    </div>
  </div>
  
  <style>
    .genre_container {
      width: 100%;
      height: 100vh;
      display: grid;
      grid-template-columns: 20% 80%;
      grid-template-rows: 100%;
    }
  
    .genre_buttons {
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      padding: 1rem;
      background-color: #141414;
      color: #fff;
      overflow-y: auto;
    }
  
    button {
      padding: 10px 20px;
      background-color: #f0f0f0;
      border: 1px solid #ccc;
      border-radius: 5px;
      cursor: pointer;
      margin-bottom: 10px;
      transition: background-color 0.3s ease, color 0.3s ease;
    }
  
    button:hover {
      background-color: #e50914;
      color: #fff;
    }
  
    button.selected {
      background-color: #e50914;
      color: #fff;
      border-color: #e50914;
    }
  
    .movie_container {
      padding: 1rem;
      background-color: #141414;
      color: #fff;
      overflow-y: auto;
    }
  
    .movies-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); /* Dynamic grid with responsive columns */
      gap: 1rem;
    }
  
    @media (max-width: 768px) {
      .genre_container {
        grid-template-columns: 1fr;
        grid-template-rows: auto 1fr;
      }
    }
  </style>
  