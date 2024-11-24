<script>
    import { onMount } from "svelte";

    export let show = false; // Controls the visibility of the modal
    export let movie_id;
    let user_id;
    let rating = 0; // State to hold the user's rating
    let feedback = ""; // State to hold the user's feedback
    let user;
    const closeModal = ()=>{
        show=false;
    }
    const submitRating = async () =>{
        const data = {
            user_id:user_id,
            movie_id:movie_id,
            rating:rating,
            review:feedback
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
        show= false;
    }
  onMount(() => {
    user =JSON.parse(localStorage.getItem('user'));
    user_id=user["userId"]
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
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000;
    }
  
    /* Modal container */
    .modal {
      background: #fff;
      padding: 20px;
      border-radius: 8px;
      text-align: center;
      width: 400px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
  
    /* Container for the rating stars */
    .rating-container {
      display: flex;
      justify-content: center;
      margin: 20px 0;
      gap: 5px;
    }
  
    /* Star buttons */
    .star {
      font-size: 2.5rem;
      cursor: pointer;
      color: #ccc;
      background: none;
      border: none;
      outline: none;
      user-select: none;
      transition: color 0.3s ease;
    }
  
    /* Selected (highlighted) stars */
    .star.selected {
      color: #ffcc00;
    }
  
    .rating-label {
      margin: 10px 0;
      font-size: 1.2rem;
      color: #333;
    }
  
    /* Feedback Text Area */
    textarea {
      width: 100%;
      padding: 10px;
      margin: 10px 0;
      border: 1px solid #ccc;
      border-radius: 5px;
      font-size: 1rem;
      resize: none;
    }
  
    textarea:focus {
      outline: none;
      border-color: #007bff;
    }
  
    /* Action buttons */
    .modal-actions {
      display: flex;
      justify-content: space-between;
      gap: 10px;
    }
  
    button {
      padding: 10px 15px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      background-color: #007bff;
      color: #fff;
      font-size: 1rem;
    }
  
    button:hover {
      background-color: #0056b3;
    }
  
    button:last-child {
      background-color: #ccc;
      color: #000;
    }
  
    button:last-child:hover {
      background-color: #999;
    }
  </style>
  