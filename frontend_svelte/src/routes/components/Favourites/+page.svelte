<script>
    import { onMount } from 'svelte';
  
    let favourites = []; // List of favourites fetched from the backend
    let user_id = null; // User ID fetched from local storage
  
    // Fetch favourites on mount
    onMount(async () => {
      const user = JSON.parse(localStorage.getItem('user'));
      user_id = user?.userId;
  
      if (user_id) {
        await fetchFavourites();
      } else {
        alert('No user found. Please log in.');
      }
    });
  
    const fetchFavourites = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/get_favourites?user_id=${user_id}`);
        const result = await response.json();
  
        if (response.ok) {
          favourites = result.favourites;
        } else {
          console.error(result.message);
          alert('Failed to fetch favourites');
        }
      } catch (error) {
        console.error('Request failed:', error);
        alert('An error occurred while fetching favourites.');
      }
    };
  
    const removeFavourite = async (movie_id) => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/remove_favourite', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ user_id, movie_id }),
        });
  
        const result = await response.json();
  
        if (response.ok) {
          alert('Favourite removed successfully!');
          favourites = favourites.filter((fav) => fav.movie_id !== movie_id);
        } else {
          console.error(result.message);
          alert('Failed to remove favourite');
        }
      } catch (error) {
        console.error('Request failed:', error);
        alert('An error occurred while removing favourite.');
      }
    };
  </script>
  
  <div>
    <h1>Your Favourites</h1>
    {#if favourites.length > 0}
      {#each favourites as fav}
        <div class="favourite-block">
          <img src={fav.poster_path} alt="Movie Poster" />
          <div class="details">
            <h2>Rating: {fav.rating} / 10</h2>
            <p>{fav.review}</p>
            <p>Rated At: {fav.rated_at}</p>
            <p>Added At: {fav.added_at}</p>
            <button on:click={() => removeFavourite(fav.movie_id)}>Remove</button>
          </div>
        </div>
      {/each}
    {:else}
      <p>No favourites to display.</p>
    {/if}
  </div>
  
  <style>
    .favourite-block {
      display: flex;
      align-items: center;
      margin: 20px 0;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 8px;
      background-color: #121212;
      color: white;
    }
  
    .favourite-block img {
      width: 100px;
      height: 150px;
      margin-right: 20px;
    }
  
    .details {
      flex: 1;
    }
  
    button {
      padding: 8px 16px;
      background-color: #098577;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
  
    button:hover {
      background-color: #064E45;
    }
  </style>
  