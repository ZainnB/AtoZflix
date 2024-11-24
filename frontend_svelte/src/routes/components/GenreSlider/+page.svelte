<script>
    import { onMount } from "svelte";
    import MovieCard from "../Slider/movie_card.svelte";
    export let limit;
    export let genre;
    export let heading;
    let movies = [];
    let currentIndex = 0;
    onMount(async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/genre?genre=${genre}&limit=${limit}`);
        if (!response.ok) {
          console.error("Failed to fetch latest movies:", response.status);
          return;
        }
        const data = await response.json();
        movies = data.movies || [];
      } catch (error) {
        console.error("Error fetching latest movies:", error);
      }
    });
  
    // Max index to slide within range
    const maxIndex = () => Math.max(0, movies.length - 8);
  
    // Handlers for navigation
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
      <h2>{heading}</h2>
      <button class="view-all-btn">View All</button>
    </div>
  
    <div class="slider-wrapper">
      <button class="slider-btn left" on:click={prevSlide}>&lt;</button>
  
      <div class="slider">
        {#each movies.slice(currentIndex, currentIndex + 8) as movie}
          <MovieCard poster_path={movie.poster_path} movie_id={movie.movie_id} />
        {/each}
      </div>
  
      <button class="slider-btn right" on:click={nextSlide}>&gt;</button>
    </div>
  </div>
  
  <style>
    .latest-movies {
      width: 100%;
      max-width: 1400px;
      margin: 0.2rem auto;
      color: #ffffff;
      background-color: #121212;
      padding: 0.2rem;
      border-radius: 7px;
    }
  
    .slider-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem; /* Reduced gap between header and slider */
    }
  
    .slider-header h2 {
      font-size: 1.5rem;
      font-weight: bold;
      margin: 0;
    }
  
    .view-all-btn {
      background-color: transparent;
      color: #098577;
      border: none;
      font-size: 0.9rem;
      cursor: pointer;
      transition: color 0.3s ease;
    }
  
    .view-all-btn:hover {
      color: #06eE45; /* Brighter red on hover */
    }
  
    .slider-wrapper {
      display: flex;
      align-items: center;
      position: relative;
    }
  
    .slider {
      display: flex;
      overflow: hidden;
      gap: 0.5rem; /* Reduced gap between movies */
      width: 100%;
    }
  
    .slider-btn {
      position: absolute;
      top: 0;
      bottom: 0;
      width: 3rem; /* Thin horizontal buttons */
      background-color: transparent;
      color: #fff;
      border: none;
      cursor: pointer;
      z-index: 1;
      transition: background-color 0.3s ease;
    }
  
    .slider-btn.left {
      left: 0;
    }
  
    .slider-btn.right {
      right: 0;
    }
  
    .slider-btn:hover {
      background-color: rgba(0, 0, 0, 0.6); /* Darker on hover */
    }
  
    .slider-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  </style>
  