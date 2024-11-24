<script>
    import { onMount } from "svelte";
    import { redirectToRegisterIfNotAuthenticated } from "../../../utils/auth.js";
    import Navbar from "./Navbar2.svelte";
    import SideBar from "./SideBar.svelte";
    import TrendingMovies from "./Top5big.svelte";
    import Top15Medium from "./Top15medium.svelte";
    import Slider from "../Slider/+page.svelte";
    import GenreSlider from "../GenralSlider/+page.svelte"
    import Footer from "../Register/Footer1.svelte";
    import Line from "../Register/Line.svelte";


    let sidebar = false;

    onMount(async () => {
        redirectToRegisterIfNotAuthenticated();
        console.log("Page loaded successfully");
    });
</script>


    <div class="wrapper">
        <div class="navbar-wrapper">
            <Navbar/>
        </div>
        <div class = "sidebar-wrapper">
            <SideBar bind:open={sidebar} />
        </div>
        <!-- Movies Section -->
        <div class="movies-wrapper">
            <TrendingMovies />
        </div>
        <div class="top15-wrapper">
            <Top15Medium />
        </div>
        <div class="latest-movies-wrapper">
            <Slider heading={"Latest Movies"} api={"latest"} limit={30}/>
        </div>
        <div class="latest-movies-wrapper">
            <Slider heading={"Top Rated Movies"} api={"top_rated"} limit={20}/>
        </div>
        <div class="latest-movies-wrapper">
            <GenreSlider type="genre" value={"Comedy"} limit={10} heading={"Laugh out Loud"} />
        </div>

    </div>
    <Line />
    <Footer />


<style>

    .wrapper {
        position: relative;
        min-height: 100vh;
        overflow: hidden;
        background-color: #121212
    }

    .navbar-wrapper {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 10;
    }

    .sidebar-wrapper {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
    }
    
    .movies-wrapper {
        position: relative;
        z-index: 1;
    }

    .top15-wrapper {
        z-index: 1;
    }

    .latest-movies-wrapper {
        z-index: 1;
        margin-top: 1rem;
    }
    *{
        padding:0px;
    }
</style>
