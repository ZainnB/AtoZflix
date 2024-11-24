<script>
  import RatingModal from "../RatingModal/RatingModal.svelte";

  let showModal = false;
  let movieRating = null;

  const handleOpenModal = () => {
    showModal = true;
  };

  const handleCloseModal = () => {
    showModal = false;
  };

  const handleSubmitRating = (rating) => {
    movieRating = rating; // Save the rating
    console.log(`Rating submitted: ${movieRating}`);
    handleCloseModal(); // Close the modal
  };
</script>

<main>
  <h1>Rate a Movie</h1>
  <button on:click={handleOpenModal}>Rate Now</button>

  <p>{movieRating !== null ? `Your Rating: ${movieRating} stars` : "No rating submitted yet."}</p>

  <RatingModal
    show={showModal}
    onClose={handleCloseModal}
    onSubmit={handleSubmitRating} />
</main>

<style>
  main {
    text-align: center;
    margin: 50px auto;
    max-width: 400px;
  }

  button {
    padding: 10px 15px;
    font-size: 1rem;
    border: none;
    background-color: #007bff;
    color: white;
    border-radius: 5px;
    cursor: pointer;
  }

  button:hover {
    background-color: #0056b3;
  }
</style>
