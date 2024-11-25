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

    // Lifecycle: On component mount
    onMount(async () => {
        redirectToRegisterIfNotAuthenticated();
        // Parse query parameters
        const params = new URLSearchParams(window.location.search);
        movie_id = params.get("movie_id");
        if (!movie_id) {
            error = "No movie ID provided";
            return;
        }

        // Fetch movie details
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/movie_details?movie_id=${movie_id}`);
            if (!response.ok) throw new Error("Failed to fetch movie details");
            const data = await response.json();
            movie = data.movie;
        } catch (err) {
            error = err.message;
        }
    });

    // Open the rating modal
    const rateMovie = () => {
        isRatingOpen = true;
    };

    // Close the rating modal
    const closeRating = () => {
        isRatingOpen = false;
    };

    // Submit the rating
    const submitRating = ({ rating, feedback }) => {
        console.log(`Rating: ${rating}, Feedback: ${feedback}`);
        isRatingOpen = false;
    };
</script>

<!-- Modal for rating -->
<RatingModal bind:show={isRatingOpen} movie_id={movie_id} />

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
                style="background-image: url('https://image.tmdb.org/t/p/original{movie.backdrop_path}')">
            </div>
            <div class="backdrop-overlay"></div>
            <div class="movie-info">
                <img 
                    src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`} 
                    alt="{movie.title}" 
                    class="movie-poster" />
                <div class="movie-details-text">
                    <h1>{movie.title}</h1>
                    <p><strong>Release Date:</strong> {movie.release_date}</p>
                    <p><strong>Runtime:</strong> {movie.runtime} minutes</p>
                    <p><strong>Overview:</strong> {movie.overview}</p>
                    <p><strong>Rating:</strong> {movie.rating_avg} ({movie.rating_count} votes)</p>
                    <div class="action-buttons">
                        <button class="favourites-btn">Add to Favourites</button>
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
        z-index: 0; /* Ensure it's below the overlay and movie info */
    }

    .backdrop-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8); /* Darker background with opacity */
        z-index: 1; /* Ensure it sits on top of the backdrop */
    }

    .movie-info {
        display: flex;
        flex-direction: column;
        gap: 15px;
        z-index: 2; /* Ensure movie info is above both the backdrop and overlay */
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

    .favourites-btn:hover {
        background-color: #064E45;
    }

    .to-watch-btn {
        background-color: #064E45;
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
</style>
