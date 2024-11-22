<script>
    import { onMount } from "svelte";

    let movies = [];
    let currentIndex = 0;
    let interval;

    onMount(async () => {
        try {
            const response = await fetch("http://127.0.0.1:5000/api/trending?limit=5");
            if (!response.ok) {
                console.error("Failed to fetch trending movies:", response.status);
                return;
            }

            const data = await response.json();
            movies = data.movies;
            console.log("Movies fetched successfully:", movies);

        } catch (error) {
            console.error("Error fetching trending movies:", error);
        }
        startAutoSlide();
    });

    const startAutoSlide = () => {
        interval = setInterval(() => {
            currentIndex = (currentIndex + 1) % movies.length;
        }, 7000);
    };

    const stopAutoSlide = () => clearInterval(interval);

    const handleNext = () => (currentIndex = (currentIndex + 1) % movies.length);

    const handlePrev = () => (currentIndex = (currentIndex - 1 + movies.length) % movies.length);

    const addToWatchLater = (movie) => alert(`${movie.title} added to Watch Later!`);
    const markAsFavorite = (movie) => alert(`${movie.title} marked as Favorite!`);
</script>

<div class="slider">
    {#if movies.length > 0}
        <div
            class="slider-bg"
            style="background-image: url(https://image.tmdb.org/t/p/original{movies[currentIndex].backdrop_path})"
        >
            <!-- Gradient Overlay -->
            <div class="slider-overlay"></div>

            <div class="movie-details">
                <h1>{movies[currentIndex].title}</h1>
                <div class="movie-meta">
                    <span>{movies[currentIndex].release_date.split("-")[0]}</span>
                    <span>{movies[currentIndex].rating} ⭐</span>
                    <span>{movies[currentIndex].duration} min</span>
                    <span>{movies[currentIndex].genres}</span>
                </div>
                <p>{movies[currentIndex].overview}</p>
                <div class="buttons">
                    <button class="action-btn" on:click={() => addToWatchLater(movies[currentIndex])}>+ Watch Later</button>
                    <button class="action-btn" on:click={() => markAsFavorite(movies[currentIndex])}>❤ Favorite</button>
                </div>
            </div>
            <div class="trending-label">
                <span>🔥 Top Trending 🔥</span>
            </div>
        </div>
        <button
            class="nav-btn prev-btn"
            on:click={handlePrev}
            on:mouseenter={stopAutoSlide}
            on:mouseleave={startAutoSlide}
        >◀</button>
        <button
            class="nav-btn next-btn"
            on:click={handleNext}
            on:mouseenter={stopAutoSlide}
            on:mouseleave={startAutoSlide}
        >▶</button>
    {:else}
        <p>Loading movies...</p>
    {/if}
</div>

<style>
    .slider {
        position: relative;
        width: 100%;
        height: 100vh;
        overflow: hidden;
        font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
        color: white;
    }

    .slider-bg {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 2rem;
    }

    .slider-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.8));
        z-index: 1; /* Keep it above the background image */
    }

    .movie-details {
        position: relative; /* Ensure it sits above the gradient */
        z-index: 2; /* Keep it above the gradient overlay */
        background: rgba(0, 0, 0, 0.237);
        padding: 2rem;
        border-radius: 1rem;
        max-width: 50%;
        font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
        margin-bottom: 7%;
    }

    .movie-details h1 {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .movie-details p {
        font-size: 1rem;
        margin-bottom: 1rem;
    }

    .movie-meta {
        display: flex;
        justify-content: space-around;
        font-size: 0.rem;
        margin-bottom: 1rem;
    }

    .nav-btn {
        position: absolute;
        top: 80%; /* Slightly above the middle of the slider */
        right: 0.4rem; /* Align both buttons to the right */
        background: #0985774a;
        color: white;
        border: none;
        font-size: 1rem;
        padding: 1rem;
        cursor: pointer;
        transition: background 0.3s;
        z-index: 3;
    }

    .nav-btn:hover {
        background: #098558b6;
    }

    .prev-btn {
        top: 72.5%; /* Slightly below the next button */
    }

    .action-btn {
        background: #098577a8;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 0.5rem;
        margin-right: 1rem;
        cursor: pointer;
        transition: background 0.3s;
    }

    .action-btn:hover {
        background: #098577;
    }

    .trending-label {
    position: absolute;
    bottom: 5rem; /* Keep it near the bottom */
    left: 50%; /* Center it horizontally */
    transform: translateX(-50%); /* Adjust centering */
    background: rgba(0, 0, 0, 0.6); /* Semi-transparent background */
    color: white;
    font-size: 1.2rem;
    padding: 0.5rem 1rem;
    border-radius: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem; /* Space between fire icon and text */
    z-index: 3;
    }

    .trending-label span {
        display: inline-block;
        filter: grayscale(1);
    }
</style>
