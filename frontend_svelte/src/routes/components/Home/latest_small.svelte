<script>
    import { onMount } from "svelte";

    let movies = [];

    onMount(async () => {
        try {
            const response = await fetch("http://127.0.0.1:5000/api/latest?limit=20"); // Adjust limit as needed
            if (!response.ok) {
                console.error("Failed to fetch latest movies:", response.status);
                return;
            }

            const data = await response.json();
            movies = data.movies;
            console.log("Movies fetched successfully:", movies);
        } catch (error) {
            console.error("Error fetching latest movies:", error);
        }
    });

    let currentIndex = 0;
    const maxIndex = () => movies.length - 7;

    function nextSlide() {
        if (currentIndex < maxIndex()) {
            currentIndex += 1;
        }
    }

    function prevSlide() {
        if (currentIndex > 0) {
            currentIndex -= 1;
        }
    }
</script>

<div class="latest-movies">
    <div class="slider-header">
        <h2>Latest Movies</h2>
        <button class="view-all-btn">View All</button>
    </div>

    <div class="slider-wrapper">
        <button class="slider-btn left" on:click={prevSlide}>&lt;</button>

        <div class="slider">
            {#each movies.slice(currentIndex, currentIndex + 7) as movie}
                <div class="movie-card">
                    <div
                        class="movie-poster"
                        style="background-image: url(https://image.tmdb.org/t/p/w500{movie.poster_path})"
                    >
                        {#if !movie.poster_path}
                            <p class="fallback-text">Poster not available</p>
                        {/if}
                    </div>
                    <script>
                      console.log("Poster Path:", movie.poster_path);
                    </script>
                </div>
            {/each}
        </div>

        <button class="slider-btn right" on:click={nextSlide}>&gt;</button>
    </div>
</div>

<style>
    .latest-movies {
        width: 100%;
        margin: 2rem 0;
        color: rgb(0, 0, 0);
    }

    .slider-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .slider-header h2 {
        font-size: 1.5rem;
        font-weight: bold;
    }

    .view-all-btn {
        background-color: transparent;
        color: #fff;
        border: none;
        font-size: 0.9rem;
        cursor: pointer;
        transition: color 0.3s ease;
    }

    .view-all-btn:hover {
        color: #098557;
    }

    .slider-wrapper {
        display: flex;
        align-items: center;
        position: relative;
    }

    .slider {
        display: flex;
        overflow: hidden;
        gap: 1rem;
        width: 100%;
    }

    .movie-card {
        flex: 0 0 13%; /* Adjust card size here */
        background: #121212;
        border-radius: 10px;
        overflow: hidden;
        transition: transform 0.3s ease;
    }

    .movie-card:hover {
        transform: scale(1.05);
    }

    .movie-poster {
        height: 100%;
        background-size: cover;
        background-position: center;
        position: relative;
        background-color: #121212;
    }

    .fallback-text {
        color: white;
        font-size: 0.9rem;
        text-align: center;
        padding: 1rem;
    }

    .slider-btn {
        background-color: transparent;
        color: white;
        border: none;
        font-size: 2rem;
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        cursor: pointer;
        z-index: 1;
    }

    .slider-btn.left {
        left: 0;
    }

    .slider-btn.right {
        right: 0;
    }
</style>
