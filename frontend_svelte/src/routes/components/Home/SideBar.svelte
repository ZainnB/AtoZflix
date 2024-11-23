<script>
    export let open = false;
    let items = ["Home", "Genre", "Country", "Movies", "TV Series", "Top IMDB", "Favorites"];
    let itemlink = ["#", "#", "#", "#", "#", "#", "#"];
    let pairedArray = items.map((item, index) => ({ sidebarElement: item, link: itemlink[index] }));
  
    const closeSideBar = () => {
      open = false;
    };
  </script>
  
  <aside class:open={open}>
    <button on:click={closeSideBar}>Close</button>
    {#each pairedArray as {sidebarElement, link}}
      <a href={link}>{sidebarElement}</a>
    {/each}
  </aside>
  
  <style>
    aside {
      position: absolute;
      width: 300px;
      height: 100%;
      background-color: grey;
      border-radius: 8px;
      left: -100%; /* Initially hidden off-screen */
      transition: left 0.3s ease-in-out;
      display: flex;
      flex-direction: column;
      align-items: center;
      z-index: 10; /* Sidebar should be above the navbar */
    }
  
    aside a {
      text-decoration: none;
      padding: 15px;
      border-bottom: 1px solid #444;
      color: black;
      font-size: 20px;
      font-weight: 500;
      text-align: center;
      cursor: pointer;
      transition: background-color 0.3s;
    }
  
    .open {
      left: 0; /* When open, bring the sidebar into view */
    }
  </style>
  