<script>
    import { onMount } from "svelte";
    import { redirectToRegisterIfNotAuthenticated } from "../../../utils/auth.js";
    import Navbar from "../Home/Navbar2.svelte";
    import SideBar from "../Home/SideBar.svelte";
    import Footer from "../Register/Footer1.svelte";
    import Line from "../Register/Line.svelte";
    import RatingModal from "../RatingModal/RatingModal.svelte";

    let isRatingOpen = false; // Controls modal visibility
    let movie_id;
    let movie = null;
    let error = null;
    let sidebar = false;
    let isFavourite = false; // Tracks if movie is in favourites
    let user_id;

    // Lifecycle: On component mount
    onMount(async () => {
        redirectToRegisterIfNotAuthenticated();
        user_id = JSON.parse(localStorage.getItem("user")).userId;
        const params = new URLSearchParams(window.location.search);
        console.log(user_id)
        movie_id = params.get("movie_id");
        console.log(movie_id)
        if (!movie_id) {
            error = "No movie ID provided";
            return;
        }

        // Fetch movie details
        try {
            const response = await fetch(
                `http://127.0.0.1:5000/api/movie_details?movie_id=${movie_id}`,
            );
            if (!response.ok) throw new Error("Failed to fetch movie details");
            const data = await response.json();
            movie = data.movie;

            // Check if movie is already in user's favourites
            console.log(user_id,movie_id)
            const favResponse = await fetch(
                
                `http://127.0.0.1:5000/api/check_favourite?user_id=${user_id}&movie_id=${movie_id}`,
            );
            if (favResponse.ok) {
                const favData = await favResponse.json();
                console.log(favData)
                isFavourite = favData.is_favourite;
                console.log(isFavourite)
            }
        } catch (err) {
            error = err.message;
        }
    });
    const rateMovie = () => {
        isRatingOpen = true;
    };
    const toggleFavourite = async () => {
        const url = isFavourite
            ? `http://127.0.0.1:5000/api/remove_favorite`
            : `http://127.0.0.1:5000/api/add_favourite`;
            console.log(user_id,movie_id)
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_id, movie_id }),
        });

        if (response.ok) {
            isFavourite = !isFavourite; // Toggle the favourite status
        } else {
            console.error("Failed to update favourite status");
        }
    };
</script>

<!-- Modal for rating -->
<RatingModal bind:show={isRatingOpen} {movie_id} />
<div class="movie-details">
    <div class="navbar-wrapper">
        <Navbar />
    </div>
    <div class="sidebar-wrapper">
        <SideBar bind:open={sidebar} />
    </div>
    {#if error}
        <p class="error">{error}</p>
    {:else if movie}
        <div class="movie-header">
            <div
                class="backdrop"
                style="background-image: url('https://image.tmdb.org/t/p/original{movie.backdrop_path}')"
            ></div>
            <div class="backdrop-overlay"></div>
            <div class="movie-info">
                <img
                    src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                    alt={movie.title}
                    class="movie-poster"
                />
                <div class="movie-details-text">
                    <h1>{movie.title}</h1>
                    <p><strong>Release Date:</strong> {movie.release_date}</p>
                    <p><strong>Runtime:</strong> {movie.runtime} minutes</p>
                    <p><strong>Overview:</strong> {movie.overview}</p>
                    <p>
                        <strong>Rating:</strong>
                        {movie.rating_avg} ({movie.rating_count} votes)
                    </p>
                    <div class="action-buttons">
                        <button
                            class="favourites-btn"
                            class:is-favourite={isFavourite}
                            on:click={toggleFavourite}
                        >
                            {isFavourite ? "Remove from Favourites" : "Add to Favourites"}
                        </button>
                        <button class="to-watch-btn">Add to Watch Later</button>
                        <button class="rate-btn" on:click={rateMovie}>Give Rating</button>
                    </div>
                </div>
            </div>
        </div>
    {:else}
        <p>Loading...</p>
    {/if}
    <Line />
    <Footer />
</div>

<style>
    .movie-details {
        padding: 20px;
        color: white;
        background-color: #121212;
        min-height: 100vh;
        position: relative;
        overflow: hidden;
        font-family: "Netflix Sans", "Helvetica Neue", "Segoe UI", "Roboto",
            "Ubuntu", sans-serif;
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

    .movie-header {
        position: relative;
        display: flex;
        gap: 30px;
        padding: 20px;
    }

    .backdrop {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-size: cover;
        background-position: center;
        z-index: 0;
    }

    .backdrop-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        z-index: 1;
    }

    .movie-info {
        display: flex;
        flex-direction: column;
        gap: 15px;
        z-index: 2;
        position: relative;
        margin-top: 3%;
    }

    .movie-poster {
        max-width: 250px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
    }

    .movie-details-text h1 {
        font-size: 2.5rem;
        margin: 0;
    }

    .movie-details-text p {
        margin: 5px 0;
    }

    .action-buttons {
        margin-top: 20px;
    }

    .action-buttons button {
        padding: 12px 20px;
        border-radius: 5px;
        font-size: 1rem;
        margin-right: 10px;
        cursor: pointer;
        border: none;
        transition: all 0.3s ease;
    }

    .favourites-btn {
        background-color: #098577;
        color: white;
    }

    .favourites-btn:disabled {
        background-color: #555;
        cursor: not-allowed;
    }

    .favourites-btn:hover {
        background-color: #064e45;
    }

    .to-watch-btn {
        background-color: #064e45;
        color: white;
    }

    .to-watch-btn:hover {
        background-color: #098577;
    }

    .rate-btn {
        background-color: #333;
        color: white;
    }

    .rate-btn:hover {
        background-color: #555;
    }
    .action-buttons button {
        padding: 12px 20px;
        border-radius: 5px;
        font-size: 1rem;
        margin-right: 10px;
        cursor: pointer;
        border: none;
        transition: all 0.3s ease;
    }

    /* Default button styles */
    .favourites-btn {
        background-color: #333;
        color: white;
        border: 2px solid transparent;
    }

    /* Add-to-Favourites style */
    .favourites-btn:not(.is-favourite) {
        background-color: #098577; /* Green for adding */
    }

    /* Remove-from-Favourites style */
    .favourites-btn.is-favourite {
        background-color: #e50914; /* Netflix red for removing */
        border-color: #b71c1c; /* Red border for distinction */
    }

    /* Hover effects */
    .favourites-btn:hover:not(.is-favourite) {
        background-color: #064e45; /* Darker green */
    }

    .favourites-btn:hover.is-favourite {
        background-color: #b71c1c; /* Darker red */
    }

    .to-watch-btn {
        background-color: #098577;
        color: white;
    }

    .to-watch-btn:hover {
        background-color: #064e45;
    }

    .rate-btn {
        background-color: #333;
        color: white;
    }

    .rate-btn:hover {
        background-color: #555;
    }
</style>
