<script>
    import SignInForm from "./SignInForm.svelte";
    export let logo = "/assets/img/logo.png";
    let showSignInForm = false;

    const toggleSignInForm = () => {
        showSignInForm = !showSignInForm;
    };
</script>

<nav>
    <div class="nav-container">
        <img src={logo} alt="Netflix Logo" class="logo" />
        <div class="signin">
            <button on:click={toggleSignInForm}>Sign In</button>
        </div>
    </div>
</nav>

{#if showSignInForm}
    <SignInForm onClose={toggleSignInForm} />
{/if}

<style>
    nav {
        width: 100%;
        height: auto;
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px 0;
        position: relative;
    }

    .nav-container {
        max-width: 60vw;
        margin: auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 20px;
    }
    .logo {
        width: 140px;
        height: auto;
    }

    .signin {
        margin-left: auto;
    }

    .signin button {
        background-color: #098577;
        color: #fff;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }

    .signin button:hover {
        background-color: #064e45;
    }
</style>
