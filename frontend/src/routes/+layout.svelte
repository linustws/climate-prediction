<script>
    import "../app.css";
    import Navbar from "../components/Navbar.svelte";
</script>

<main>
    <Navbar/>

    <div class="slot"><slot/></div>
</main>

<style lang="postcss">
    main {
        height: 100vh;
        width: 100%;
        background-image: url("$lib/images/background.png");
        background-size: cover;
        background-position: center;
        //display: flex;
        //flex-direction: column;
        //align-items: center;
        font-size: 1.5rem;
        font-weight: 300;
        position: fixed;
        overflow: auto;
    }
    .slot {
        margin-top: 3.5rem;
    }
</style>
