<script>
  export let open = false;
  let items = [
    "Home",
    "Genre",
    "Actors",
    "Crew",
    "Country",
    "Favourites",
    "To Watch Later"
  ];
  let itemlink = [
    "Home",
    "Genre",
    "Actors",
    "Crew",
    "Country",
    "Favourites",
    "ToWatchLater"
  ];
  let pairedArray = items.map((item, index) => ({
    dropdownElement: item,
    link: itemlink[index],
  }));

  const toggleDropdown = () => {
    open = !open;
  };
</script>

<div class="dropdown">
  <button on:click={toggleDropdown} class="dropdown-toggle">&#9776;</button>
  {#if open}
    <div class="dropdown-content">
      {#each pairedArray as { dropdownElement, link }}
        <a href={`../components/${link}`}>{dropdownElement}</a>
      {/each}
    </div>
  {/if}
</div>

<style>
  .dropdown {
    position: relative;
    display: inline-block;
    z-index: 15;
    left: 8%;
    top: 0px;
  }

  .dropdown-toggle {
    padding: 10px 20px;
    border: none;
    cursor: pointer;
    margin-top: 3px;
    font-size: 30px;
    color: white;
    background: transparent;
    transition: color 0.3s;
  }

  .dropdown-content {
    position: absolute;
    top: 100%;
    background-color: #098577a9;
    border-radius: 8px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 8;
    display: flex;
    flex-direction: column;
    min-width: 200px;
  }

  .dropdown-toggle:hover {
    color: #1abc9c;
  }

  .dropdown-content a {
    text-decoration: none;
    padding: 8px 20px;
    color: black;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .dropdown-content a:last-child {
    border-bottom: none; /* Remove the border for the last item */
  }

  .dropdown-content a:hover {
    background-color: #121212;
    color: white;
  }
</style>
