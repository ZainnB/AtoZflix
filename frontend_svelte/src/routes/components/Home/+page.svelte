<script>
    import { onMount } from "svelte";
    import Navbar from "./Navbar2.svelte";
    import TrendingMovies from "./Top5big.svelte";
    import Top15Medium from "./Top15medium.svelte";
    import LatestMovies from "./latest_small.svelte";

    onMount(async () => {
        console.log("Page loaded successfully");
    });
</script>


    <div class="wrapper">
        <div class="navbar-wrapper">
            <Navbar />
        </div>

        <!-- Movies Section -->
        <div class="movies-wrapper">
            <TrendingMovies />
            <div class="top15-wrapper">
                <Top15Medium />
            </div>
            <div class="latest-movies-wrapper">
                <LatestMovies />
            </div>
    </div>

    </div>


<style>

    .wrapper {
        position: relative;
        min-height: 100vh;
        overflow: hidden;
    }

    .navbar-wrapper {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 10;
    }

    .movies-wrapper {
        position: relative;
        z-index: 1;
    }

    .top15-wrapper {
        padding: 0 1rem;
        z-index: 1;
    }

    .latest-movies-wrapper {
        padding: 2rem 1rem;
        z-index: 1;
        margin-top: 2rem;
    }
</style>
