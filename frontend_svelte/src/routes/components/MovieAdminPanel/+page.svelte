<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import MovieCard from "../Slider/movie_card.svelte";

  const BASE_URL = "http://localhost:5000/api";

  // Admin actions form data
  let admin_id = "";
  let movie_id = "";
  let year_start = 2024;
  let year_end = 2024;
  let page_start = 1;
  let page_end = 1;

  // Search functionality form data
  let query = "";
  let movies = [];
  let searchError = "";

  let responseMessage = writable("");

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
  const addSingleMovie = () =>
      callApi("add_single_movie", "POST", { admin_id, movie_id });

  const updateSingleMovie = () =>
      callApi("update_single_movie", "PUT", { admin_id, movie_id });

  const deleteSingleMovie = () =>
      callApi("delete_single_movie", "DELETE", { admin_id, movie_id });

  const addBatchMovies = () =>
      callApi("add_batch_movies", "POST", {
          admin_id,
          year_start,
          year_end,
          page_start,
          page_end,
      });

  const updateBatchMovies = () =>
      callApi("update_batch_movies", "PUT", {
          admin_id,
          year_start,
          year_end,
          page_start,
          page_end,
      });

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
  body {
      font-family: Arial, sans-serif;
      background-color: #121212;
      color: #fff;
      padding: 20px;
  }

  input, button {
      margin: 5px 0;
      padding: 8px;
      border: none;
      border-radius: 5px;
      font-size: 1rem;
  }

  input {
      background-color: #1e1e1e;
      color: #fff;
      width: 100%;
  }

  button {
      background-color: #007BFF;
      color: white;
      cursor: pointer;
  }

  button:hover {
      background-color: #0056b3;
  }

  .response, .search-results {
      margin-top: 20px;
      padding: 10px;
      background-color: #1e1e1e;
      border-radius: 5px;
  }

  .movies-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem;
      margin-top: 20px;
  }
</style>

<main class = "body">
  <h1>Admin Panel</h1>

  <!-- Admin Actions -->
  <section>
      <h2>Single Movie Actions</h2>
      <input type="text" placeholder="Admin ID" bind:value={admin_id} />
      <input type="text" placeholder="Movie ID" bind:value={movie_id} />
      <button on:click={addSingleMovie}>Add Single Movie</button>
      <button on:click={updateSingleMovie}>Update Single Movie</button>
      <button on:click={deleteSingleMovie}>Delete Single Movie</button>
  </section>

  <section>
      <h2>Batch Movie Actions</h2>
      <input type="text" placeholder="Admin ID" bind:value={admin_id} />
      <input type="number" placeholder="Year Start" bind:value={year_start} />
      <input type="number" placeholder="Year End" bind:value={year_end} />
      <input type="number" placeholder="Page Start" bind:value={page_start} />
      <input type="number" placeholder="Page End" bind:value={page_end} />
      <button on:click={addBatchMovies}>Add Batch Movies</button>
      <button on:click={updateBatchMovies}>Update Batch Movies</button>
  </section>

  <div class="response">
      <h3>Admin Response:</h3>
      <p>{$responseMessage}</p>
  </div>

  <!-- Search Movies -->
  <section>
      <h2>Search Movies</h2>
      <input type="text" placeholder="Search Query" bind:value={query} />
      <button on:click={searchMovies}>Search</button>

      {#if searchError}
          <p class="error">{searchError}</p>
      {:else if movies.length === 0 && query}
          <p>No results found.</p>
      {:else}
          <div class="movies-grid">
              {#each movies as { poster_path, movie_id }}
                  <MovieCard poster_path={poster_path} movie_id={movie_id} />
              {/each}
          </div>
      {/if}
  </section>
</main>
