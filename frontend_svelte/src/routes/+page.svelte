<script>
  import RegistrationPage from "./components/Register/+page.svelte";
  import Home from "./components/Home/+page.svelte";
  import {onMount} from 'svelte';
  onMount(async () => {
    window.location.href="./components/Register";
  });
</script>