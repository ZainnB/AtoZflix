<script>
  import Navbar from "./Navbar1.svelte";
  import Main from "./RegisterationForm.svelte";
  import FAQ from "./FAQ.svelte";
  import Footer from "./Footer1.svelte";
  import Line from "./Line.svelte";
  import { redirectToRegisterIfNotAuthenticated } from "/src/utils/auth.js";
  import { onMount } from "svelte";

  onMount(async ()=>{
    redirectToHomeIfAuthenticated();
  })
  const faqQuestions = [
    {
      title: "How does the recommendation system understand my preferences?",
      content:
        "Our system uses advanced machine learning algorithms to analyze your viewing history, ratings, and preferences. It learns what you like and suggests movies and shows that match your unique taste.",
    },
    {
      title: "What is a hybrid recommendation system?",
      content:
        "It combines content-based filtering (analyzing the attributes of movies you like) and collaborative filtering (finding patterns in what similar users enjoy) to provide smarter, more accurate recommendations.",
    },
    {
      title: "Will I only see popular or trending movies?",
      content:
        "No! Our recommendations focus on what you personally enjoy, even if the movies are less known. This ensures every suggestion feels tailored and relevant to you.",
    },
    {
      title: "How does the system evolve as I use it?",
      content:
        "As you interact with the platform—rating, adding to your watchlist, or skipping suggestions—the system refines its understanding of your preferences to deliver even better recommendations over time.",
    },
  ];
</script>

<div class="background-section">
  <div class="navbar-main-container">
    <Navbar logo="/assets/img/logo.png" />
    <Main />
  </div>

  <Line />
  <FAQ questions={faqQuestions} />
  <Line />
  <Footer />
</div>

<style>
  div {
    font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box; 
    width: 100%; 
    height: 100%;
    background: none;
  }

  .navbar-main-container {
    background-image: url("/assets/img/bg.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
</style>
