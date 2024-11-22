<!-- <script>
  import MovieCard from "./components/MovieCard.svelte";
  let top7_latest=[]

  async function get(){
    const res= await fetch("http://127.0.0.1:5000/api/top7_latest");
    const data= await res.json();
    top7_latest=data
    console.log(top7_latest)
  }
</script>

<button on:click={get}>Get</button>
<div class="top_7_latest">
  <h2>Top 10 Latest Movies</h2>
  <div class="top-7-container">
{#each top7_latest as movie}
<MovieCard movie_name={movie.title} movie_runtime={movie.runtime} release_date={movie.release_date} />
{/each}
</div>
</div>

<style>
  .top-7-container{
      height:100px;
      width:100%;
      display:flex;
      flex-direction: row;
  }
</style> -->


