<script>
    import "../app.css";
    import Navbar from "$lib/Navbar.svelte";
</script>

<main>
    <Navbar/>

    <slot/>
</main>

<style lang="postcss">
    main {
        margin: 0;
        height: 100%;
        overflow: auto;
        //overflow: hidden;
        background-image: url("$lib/images/background.png");
        background-size: cover;
        background-position: center;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        font-size: 1.5rem;
        font-weight: 300;
        position: fixed;
        width: 100%;
    }
</style>
