<script>
    import { onMount } from "svelte";

    let movies = [];
    let currentIndex = 0;

    onMount(async () => {
        try {
            const response = await fetch("http://127.0.0.1:5000/api/trending?limit=20");
            if (!response.ok) {
                console.error("Failed to fetch trending movies:", response.status);
                return;
            }

            const data = await response.json();
            movies = data.movies.slice(5);
            console.log("Movies fetched successfully:", movies);

            // Start the slider functionality
            startAutoSlide();
        } catch (error) {
            console.error("Error fetching trending movies:", error);
        }
    });

    function slideNext() {
        currentIndex = (currentIndex + 1) % Math.ceil(movies.length / 4); // Move to the next set of 4 movies
    }

    function slidePrev() {
        currentIndex = (currentIndex - 1 + Math.ceil(movies.length / 4)) % Math.ceil(movies.length / 4); // Move to the previous set
    }

    function startAutoSlide() {
        setInterval(() => {
            slideNext();
        }, 5000); // Slide every 5 seconds
    }
</script>

<div class="top15-medium">
    <!-- Slider Container -->
    <div class="slider" style="transform: translateX(-{currentIndex * 100}%);">
        {#each Array(Math.ceil(movies.length / 4)) as _, slideIndex}
            <div class="slide">
                {#each movies.slice(slideIndex * 4, slideIndex * 4 + 4) as movie}
                    <div class="movie-card">
                        <div
                            class="movie-poster"
                            style="background-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.8)), url(https://image.tmdb.org/t/p/w500{movie.backdrop_path})"
                        >
                            <div class="movie-info">
                                <h3>{movie.title}</h3>
                                <div class="genres">
                                    {#each movie.genres as genre}
                                        <span>{genre}</span>
                                    {/each}
                                </div>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        {/each}
    </div>

    <!-- Slider Navigation Buttons -->
    <div class="slider-buttons">
        <button class="prev-button" on:click={slidePrev}>❮</button>
        <button class="next-button" on:click={slideNext}>❯</button>
    </div>
</div>

<style>
    /* Main Container */
    .top15-medium {
        position: relative;
        overflow: hidden;
        background-color: #121212;
        padding: 2rem;
        width: 100%;
        height: 100%;
        box-sizing: border-box;
    }

    /* Slider */
    .slider {
        display: flex;
        transition: transform 0.5s ease-in-out;
        gap: 1rem;
    }

    .slide {
        display: flex;
        flex: 0 0 100%;
        gap: 1rem; /* Spacing between movie cards */
    }

    /* Movie Card Styling */
    .movie-card {
        flex: 0 0 24%; 
        border-radius: 10px;
        overflow: hidden;
        background: transparent;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 200px;
    }

    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.515);
    }

    /* Poster with Gradient Overlay */
    .movie-poster {
        height: 100%; /* Adjust poster height relative to card */
        background-size: cover;
        background-position: center;
        position: relative;
    }

    /* Transparent Movie Info */
    .movie-info {
        padding: 1rem;
        padding-top: 41%;
        color: rgb(255, 255, 255);
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
        background: linear-gradient(to bottom, rgba(0, 0, 0, 0.155), rgba(0, 0, 0, 0.681));
    }

    .movie-info h3 {
        font-size: 1.4rem;
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
    }

    .movie-info .genres {
        display: flex;
        flex-wrap: nowrap;
        gap: 0.1rem;
    }

    .movie-info .genres span {
        font-size: 0.9rem;
        color: #098577;
    }

    /* Slider Navigation Buttons */
    .slider-buttons {
        position: absolute;
        top: 50%;
        right: 1rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        transform: translateY(-50%);
    }

    .slider-buttons button {
        background: rgba(0, 0, 0, 0.7);
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: background 0.3s ease;
    }

    .slider-buttons button:hover {
        background: rgba(255, 255, 255, 0.7);
        color: black;
    }
</style>
