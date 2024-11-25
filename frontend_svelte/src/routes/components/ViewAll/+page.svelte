<script>
    import { onMount } from "svelte";
    import MovieCard from "./movie_card.svelte";
    import { page } from "$app/stores";
  
    let movies = [];
    let type = ""; // API type, e.g., "latest" or "top_rated"
    let heading = ""; // Page heading
    let pageNumber = 1; // Current page
    const limit = 80; // Number of movies per page
    let totalMovies = 0; // Total number of movies fetched from the backend
    let totalPages = 0; // Total number of pages for pagination
    let error = ""; // To store error messages
  
    // Extract query parameters from the URL using URLSearchParams
    onMount(async () => {
      try {
        // Fetch query parameters from URL
        const urlParams = new URLSearchParams(window.location.search);
        type = urlParams.get("type") || "";  // API type (e.g., latest, top_rated)
        heading = urlParams.get("heading") || "";  // Page heading (e.g., "Latest Movies")
  
        // Fetch movies based on current params
        await fetchMovies();
      } catch (err) {
        error = "Failed to fetch movies.";
        console.error("Error fetching movies:", err);
      }
    });
  
    // Fetch movies from the backend API
    async function fetchMovies() {
      try {
        const offset = (pageNumber - 1) * limit;
        const response = await fetch(`http://127.0.0.1:5000/api/${type}?limit=${limit}&offset=${offset}`);
        if (!response.ok) {
          console.error(`Failed to fetch movies: ${response.status}`);
          error = "Failed to fetch movies.";
          return;
        }
        const data = await response.json();
        movies = data.movies || [];
        totalMovies = data.total_movies || 0;  // Total movies from the backend
        totalPages = Math.ceil(totalMovies / limit);  // Calculate total pages
      } catch (error) {
        console.error("Error fetching movies:", error);
        error = "Error fetching movies.";
      }
    }
  
    function nextPage() {
      if (pageNumber < totalPages) {
        pageNumber += 1;
        fetchMovies();
      }
    }
  
    function prevPage() {
      if (pageNumber > 1) {
        pageNumber -= 1;
        fetchMovies();
      }
    }
  </script>
  
  <div class="view-all-page">
    <h1>{heading}</h1>
    {#if error}
      <p class="error">{error}</p>
    {/if}
    <div class="movie-grid">
      {#each movies as movie}
        <MovieCard poster_path={movie.poster_path} movie_id={movie.movie_id} />
      {/each}
    </div>
  
    <div class="pagination">
      <button on:click={prevPage} disabled={pageNumber === 1}>Previous</button>
      <span>Page {pageNumber} of {totalPages}</span>
      <button on:click={nextPage} disabled={pageNumber === totalPages}>Next</button>
    </div>
  </div>
  
  <style>
    .view-all-page {
      padding: 1rem;
      color: #fff;
      background-color: #121212;
    }
  
    h1 {
      text-align: center;
      margin-bottom: 1rem;
    }
  
    .movie-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap: 1rem;
      margin: 1rem 0;
    }
  
    .pagination {
      display: flex;
      justify-content: center;
      gap: 1rem;
      margin-top: 1rem;
    }
  
    .pagination button {
      padding: 0.5rem 1rem;
      background-color: #098577;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s;
    }
  
    .pagination button:disabled {
      background-color: #444;
      cursor: not-allowed;
    }
  
    .pagination button:hover:not(:disabled) {
      background-color: #064e45;
    }
  
    .error {
      color: red;
      text-align: center;
      margin-top: 1rem;
    }
  </style>
  