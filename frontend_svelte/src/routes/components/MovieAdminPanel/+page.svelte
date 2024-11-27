<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import MovieCard from "../Slider/movie_card.svelte";

  const BASE_URL = "http://localhost:5000/api";

  // Admin actions form data
  let user_id = "";
  let movie_id = "";
  let year_start = 2024;
  let year_end = 2024;
  let page_start = 1;
  let page_end = 1;
  let batchFormVisible = false;

  // Search functionality form data
  let query = "";
  let movies = [];
  let searchError = "";

  let responseMessage = writable("");

  // Fetch Admin ID from localStorage
  onMount(() => {
    const user = JSON.parse(localStorage.getItem("user"));
    user_id = user?.userId || "";
    if (!user_id) {
      console.log("No user ID found in localStorage");
    }
  });

  // API request handler
  const callApi = async (endpoint, method, body) => {
    try {
      const res = await fetch(`${BASE_URL}/${endpoint}`, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      responseMessage.set(data.message || data.error || "Action completed");
    } catch (error) {
      responseMessage.set(`Error: ${error.message}`);
    }
  };

  // Admin panel actions
  const addSingleMovie = () => callApi("add_single_movie", "POST", { user_id, movie_id });
  const updateSingleMovie = () => callApi("update_single_movie", "PUT", { user_id, movie_id });
  const deleteSingleMovie = () => callApi("delete_single_movie", "DELETE", { user_id, movie_id });
  const addBatchMovies = () => callApi("add_batch_movies", "POST", { user_id, year_start, year_end, page_start, page_end });
  const updateBatchMovies = () => callApi("update_batch_movies", "PUT", { user_id, year_start, year_end, page_start, page_end });

  // Search functionality
  const searchMovies = async () => {
    try {
      const res = await fetch(`${BASE_URL}/search_movie?query=${encodeURIComponent(query)}&limit=10`);
      const data = await res.json();
      if (res.ok) {
        movies = data.movies;
        searchError = "";
      } else {
        searchError = data.error || "Failed to fetch movies.";
      }
    } catch (err) {
      searchError = "An error occurred while searching movies.";
      console.error(err);
    }
  };
</script>

<style>
  main {
    font-family: Arial, sans-serif;
    background-color: #121212;
    color: #fff;
    margin: 0;
    padding: 20px;
  }

  .search-bar {
    text-align: center;
    margin-bottom: 20px;
  }

  input, button {
    margin: 5px;
    padding: 10px;
    border: none;
    border-radius: 5px;
    font-size: 1rem;
  }

  input {
    background-color: #1e1e1e;
    color: #fff;
    width: 300px;
  }

  button {
    background-color: #098577;
    color: white;
    cursor: pointer;
  }

  button:hover {
    background-color: #064E45;
  }

  .response {
    margin-top: 20px;
    padding: 15px;
    background-color: #1e1e1e;
    border-radius: 5px;
  }

  .movies-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 20px;
  }

  .movie-id {
    margin-top: 10px;
    font-size: 0.9rem;
    text-align: center;
  }

  .batch-actions {
    text-align: center;
    margin-top: 20px;
  }

  .batch-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 10px;
    background-color: #1e1e1e;
    padding: 15px;
    border-radius: 5px;
  }
  .back-button {
  margin-top: 20px;
  text-align: center;
}

.back-button button {
  background-color: #555;
  color: #fff;
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.back-button button:hover {
  background-color: #333;
}

</style>

<main>
  <!-- Back Button -->
<div class="back-button">
  <button on:click={() => window.history.back()}>Back</button>
</div>

  <!-- Search Bar -->
  <div class="search-bar">
    <h1>Search Movies</h1>
    <input type="text" placeholder="Search Query" bind:value={query} />
    <button on:click={searchMovies}>Search</button>
  </div>

  <!-- Movie Grid -->
  {#if searchError}
    <p class="error">{searchError}</p>
  {:else if movies.length === 0 && query}
    <p class="response">No results found.</p>
  {:else}
    <div class="movies-grid">
      {#each movies as { poster_path, movie_id }}
        <div>
          <MovieCard poster_path={poster_path} movie_id={movie_id} />
          <p class="movie-id">Movie ID: {movie_id}</p>
        </div>
      {/each}
    </div>
  {/if}

  <!-- Single Movie Actions -->
  <section>
    <h2>Single Movie Actions</h2>
    <input type="text" placeholder="Movie ID" bind:value={movie_id} />
    <button on:click={addSingleMovie}>Add Single Movie</button>
    <button on:click={updateSingleMovie}>Update Single Movie</button>
    <button on:click={deleteSingleMovie}>Delete Single Movie</button>
  </section>

  <!-- Batch Movie Actions -->
  <div class="batch-actions">
    <button on:click={() => (batchFormVisible = !batchFormVisible)}>
      {batchFormVisible ? "Hide Batch Actions" : "Show Batch Actions"}
    </button>

    {#if batchFormVisible}
      <div class="batch-form">
        <input type="number" placeholder="Year Start" bind:value={year_start} />
        <input type="number" placeholder="Year End" bind:value={year_end} />
        <input type="number" placeholder="Page Start" bind:value={page_start} />
        <input type="number" placeholder="Page End" bind:value={page_end} />
        <button on:click={addBatchMovies}>Add Batch Movies</button>
        <button on:click={updateBatchMovies}>Update Batch Movies</button>
      </div>
    {/if}
  </div>

  <!-- Response Message -->
  <div class="response">
    <h3>Admin Response:</h3>
    <p>{$responseMessage}</p>
  </div>
</main>
