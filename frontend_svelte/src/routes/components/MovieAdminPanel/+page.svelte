<script>
  import { onMount } from "svelte";
  import MovieCard from "../Slider/movie_card.svelte";
  import { redirectToRegisterIfNotAuthenticated } from "../../../utils/auth.js";

  let query = "";
  let movies = [];
  let error = "";
  let movieIdInput = "";
  let batchStartYear = "";
  let batchEndYear = "";
  let batchStartPage = "";
  let batchEndPage = "";
  let testResponse = "";

  // Admin ID (assuming stored in localStorage)
  let adminId = JSON.parse(localStorage.getItem("user"))?.userId || null;

  // Fetch movies on query change
  async function fetchMovies() {
    if (!query) return;

    try {
      const response = await fetch(`http://localhost:5000/api/search_movie?query=${encodeURIComponent(query)}&limit=10`);
      const data = await response.json();

      if (response.ok) {
        movies = data.movies;
      } else {
        error = data.error || "Failed to fetch movies.";
      }
    } catch (err) {
      error = "Error occurred while fetching movies.";
    }
  }

  // Single Movie Action (Add, Update, Delete)
  async function handleSingleMovieAction(action) {
    if (!movieIdInput) {
      alert("Enter a Movie ID");
      return;
    }

    const url = `/api/${action}_single_movie`;
    try {
      const response = await fetch(`http://localhost:5000${url}`, {
        method: action === "delete" ? "DELETE" : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ admin_id: adminId, movie_id: movieIdInput }),
      });
      const result = await response.json();
      alert(response.ok ? result.message : result.error || "Action failed");
      fetchMovies();
    } catch {
      alert("Request failed.");
    }
  }


  onMount(() => {
    redirectToRegisterIfNotAuthenticated();
  });
</script>
<div class="wrapper">
  <div class="content">
    <!-- Search Bar -->
    <input
      type="text"
      placeholder="Search for a movie..."
      bind:value={query}
      on:change={fetchMovies}
    />

    <!-- Search Results -->
    {#if error}
      <p class="error">{error}</p>
    {:else if movies.length === 0}
      <p>No movies found.</p>
    {:else}
      <div class="movies-grid">
        {#each movies.slice(0, 8) as { poster_path, movie_id }}
          <MovieCard poster_path={poster_path} movie_id={movie_id} />
        {/each}
      </div>
    {/if}

    <!-- Single Movie Actions -->
    <h3>Single Movie Actions</h3>
    <input
      type="text"
      placeholder="Movie ID"
      bind:value={movieIdInput}
    />
    <button on:click={() => handleSingleMovieAction("add")}>Add Movie</button>
    <button on:click={() => handleSingleMovieAction("update")}>Update Movie</button>
    <button on:click={() => handleSingleMovieAction("delete")}>Delete Movie</button>
  </div>
</div>
  

<style>
  .error {
    color: red;
  }

  .movies-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
  }
</style>