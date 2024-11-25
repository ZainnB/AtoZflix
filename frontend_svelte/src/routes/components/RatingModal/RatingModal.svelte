<script>
  import { onMount } from "svelte";

  export let show = false; // Controls the visibility of the modal
  export let movie_id;
  let user_id;
  let rating = 0; // State to hold the user's rating
  let feedback = ""; // State to hold the user's feedback
  let user;
  
  const closeModal = () => {
      show = false;
  }

  const submitRating = async () => {
      const data = {
          user_id: user_id,
          movie_id: movie_id,
          rating: rating,
          review: feedback
      }

      try {
          const response = await fetch('http://127.0.0.1:5000/api/rate_movie', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify(data),
          });

          const result = await response.json();

          if (response.ok) {
              console.log('Success:', result.message);
              alert('Rating submitted successfully!');
          } else {
              console.log('Error:', result.message);
              alert('Error: ' + result.message);
          }
      } catch (error) {
          console.error('Request failed', error);
          alert('An error occurred. Please try again.');
      }
      show = false;
  }

  onMount(() => {
      user = JSON.parse(localStorage.getItem('user'));
      user_id = user["userId"];
      if (user_id) {
          console.log('User ID from localStorage:', user_id);
      } else {
          console.log('No user ID found in localStorage');
      }
  });
</script>

{#if show}
  <div class="modal-overlay">
      <div class="modal">
          <h2>Rate the Movie</h2>

          <!-- Star Rating Section -->
          <div class="rating-container">
              {#each Array(10).fill() as _, index}
                  <button
                      type="button"
                      class="star"
                      aria-label={`Rate ${index + 1} stars`}
                      class:selected={index + 1 <= rating}
                      on:click={() => (rating = index + 1)}>
                      ★
                  </button>
              {/each}
          </div>
          <p class="rating-label">{rating > 0 ? `You rated ${rating} stars` : "Select your rating"}</p>

          <!-- Feedback Text Section -->
          <textarea
              rows="4"
              placeholder="Write your review here..."
              bind:value={feedback}></textarea>

          <!-- Action Buttons -->
          <div class="modal-actions">
              <button on:click={submitRating}>Submit</button>
              <button on:click={closeModal}>Cancel</button>
          </div>
      </div>
  </div>
{/if}

<style>
  /* Overlay to darken the background */
  .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.7);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000;
  }

  /* Modal container */
  .modal {
      background: #121212;
      padding: 20px;
      border-radius: 10px;
      text-align: center;
      width: 450px;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
      color: #fff;
  }

  /* Title */
  h2 {
      font-size: 1.5rem;
      margin-bottom: 20px;
      color: #fff;
  }

  /* Container for the rating stars */
  .rating-container {
      display: flex;
      justify-content: space-between;
      gap: 4px;
      margin: 20px 0;
      padding: 10 10px;
  }

  /* Star buttons */
  .star {
      font-size: 1.5rem;
      cursor: pointer;
      color: #ccc;
      background: none;
      border: none;
      outline: none;
      user-select: none;
      transition: color 0.3s ease;
      padding: 0;
      margin: 10px 0;
  }

  /* Selected (highlighted) stars */
  .star.selected {
      color: #ffcc00;
  }

  .rating-label {
      margin: 10px 0;
      font-size: 1rem;
      color: #ccc;
  }

  /* Feedback Text Area */
  textarea {
      width: 100%;
      padding: 12px;
      margin: 10px 0;
      border: 1px solid #098577;
      border-radius: 8px;
      font-size: 1rem;
      background-color: #121212;
      color: #fff;
      resize: none;
      transition: border-color 0.3s ease;
  }

  textarea:focus {
      outline: none;
      border-color: #064e45;
  }

  /* Action buttons */
  .modal-actions {
      display: flex;
      justify-content: space-between;
      gap: 10px;
  }

  button {
      padding: 12px 20px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      background-color: #098577;
      color: white;
      font-size: 1.1rem;
      transition: background-color 0.3s ease;
  }

  button:hover {
      background-color: #064e45;
  }

  button:last-child {
      background-color: #ccc;
      color: #000;
  }

  button:last-child:hover {
      background-color: #999;
  }
</style>
