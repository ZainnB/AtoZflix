<script>
    export let poster_path;
  </script>
  <a href="#">
  <div class="movie-card">
    <img src={`https://image.tmdb.org/t/p/w500${poster_path}`} alt="Movie Poster" class="movie-image" />
  </div></a>
  <style>
    .movie-card {
      flex: 0 0 calc(12.5% - 10px);
      margin: 4px;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
      background: #fff;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      height: 250px;
      width: 150px;
    }
  
    .movie-card:hover {
      transform: scale(1.05);
      box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
    }
  
    .movie-image {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  </style>
  