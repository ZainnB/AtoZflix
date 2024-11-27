<script>
    import { onMount } from 'svelte';
    import { redirectToRegisterIfNotAuthenticated } from "/src/utils/auth.js";
    import Navbar from "../Home/Navbar2.svelte";
    import SideBar from "../Home/SideBar.svelte";
    import Footer from "../Register/Footer1.svelte";
    import Line from "../Register/Line.svelte";
    import MovieCard from '../Slider/movie_card.svelte';

    let user_id = null;
    let favourites = [];
    let isLoading = true;
    let error = '';
    let sidebar = false;

    // Check if the user is authenticated and redirect if not
    onMount(async () => {
        redirectToRegisterIfNotAuthenticated();
        user_id = JSON.parse(localStorage.getItem("user")).userId;

        // Fetch movie details
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/get_favourites?user_id=${user_id}`);
            if (!response.ok) throw new Error("Failed to fetch favourites");
            const data = await response.json();
            favourites = data.favourites || [];
        } catch (err) {
            error = err.message;
        } finally {
            isLoading = false;
        }
    });

    async function fetchFavourites() {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/get_favourites?user_id=${user_id}`);
            if (!response.ok) throw new Error("Failed to fetch favourites");
            const data = await response.json();
            favourites = data.favourites || [];
        } catch (err) {
            error = err.message;
        } finally {
            isLoading = false;
        }
    }

    // Remove a favourite movie
    async function removeFavourite(movieId) {
        try {
            const url = `http://127.0.0.1:5000/api/remove_favourite`;
            console.log(user_id,movieId)
            const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_id, movie_id: movieId  }),
            });
            if (!response.ok) throw new Error("Failed to remove the movie");
            await fetchFavourites();
            } catch (e) {
            alert(e.message || 'An error occurred while removing the movie.');
            }
    }

</script>


<div class="wrapper">
    <div class="navbar-wrapper">
        <Navbar />
    </div>
    <div class="sidebar-wrapper">
        <SideBar bind:open={sidebar} />
    </div>
    
    <div class="favourites-wrapper">
        {#if isLoading}
            <p>Loading your favourites...</p>
        {:else if error}
            <p>{error}</p>
        {:else if favourites.length === 0}
            <p>You have no favourites yet.</p>
        {:else}
            {#each favourites as movie}
                <div class="movie-card">
                    <MovieCard poster_path={movie.poster_path} movie_id={movie.movie_id} />
                    <p class="added-at">Added on: {new Date(movie.added_at).toLocaleDateString()}</p>
                    <button class="remove-button" on:click={() => removeFavourite(movie.movie_id)}>
                        Remove from Favourites
                    </button>
                </div>
            {/each}
        {/if}
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
    .favourites-wrapper {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1rem;
        padding: 1rem;
        margin-top: 80px;
    }

    .favourites-wrapper p {
        margin-top: 1rem;
        color: #ffffff;
        text-align: center;
    }

    .movie-card {
        margin-bottom: 1rem;
        width: 100%;
        max-width: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .added-at {
        font-size: 0.8rem;
        color: #888;
    }

    .remove-button {
        margin-top: 0.5rem;
        padding: 0.5rem 1rem;
        background-color: #ff4d4f;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }

    .remove-button:hover {
        background-color: #ff1a1d;
    }
</style>
