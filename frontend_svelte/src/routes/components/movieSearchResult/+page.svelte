<script>
    import { onMount } from "svelte";
  
    let query = "";
    let movies = [];
    let error = "";
  
    // Extract query parameter
    onMount(async () => {
      const urlParams = new URLSearchParams(window.location.search);
      query = urlParams.get("query");
  
      if (query) {
        try {
            const response = await fetch(`http://localhost:5000/api/search_movie?query=${encodeURIComponent(query)}&limit=10`);
            const data = await response.json();
  
          if (response.ok) {
            movies = data.movies;
          } else {
            error = data.error || "Failed to fetch movies.";
          }
        } catch (err) {
          error = "An error occurred while fetching movies.";
          console.error(err);
        }
      }
    });
  </script>
  
  <main>
    <h1>Search Results for "{query}"</h1>
  
    {#if error}
      <p class="error">{error}</p>
    {:else if movies.length === 0}
      <p>No results found.</p>
    {:else}
      <ul>
        {#each movies as movie}
          <li>
            <img src={movie.poster_path} alt="Movie Poster" width="100" />
            <p>Movie ID: {movie.movie_id}</p>
          </li>
        {/each}
      </ul>
    {/if}
  </main>
  
  <style>
    .error {
      color: red;
    }
  </style>
  