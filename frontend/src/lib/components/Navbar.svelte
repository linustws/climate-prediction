<script>
    import { ChartLineSolid, CubesSolid, GithubBrand } from 'svelte-awesome-icons';
    import {onMount} from "svelte";

    let currentPath = '/';

    onMount(() => {
        currentPath = window.location.pathname;
    });

    const handlePredictClick = () => {
        if (currentPath === '/') {
            window.location.reload();
        } else {
            window.location.href = '/';
        }
    };

    const handleModelClick = () => {
        if (currentPath === '/model') {
            window.location.reload();
        } else {
            window.location.href = '/model';
        }
    };
</script>


<header>
    <div class="title">
        Singapore Weather Prediction
    </div>
    <nav class="navbar">
        <ul>
            <li><a href="/" on:click={handlePredictClick}><i><ChartLineSolid class="outline-none"/></i>Predict</a></li>
            <li><a href="/model" on:click={handleModelClick}><i><CubesSolid class="outline-none"/></i>Model</a></li>
        </ul>
    </nav>
    <div class="github"><a href="https://github.com/linustws/singapore-weather-prediction"><i><GithubBrand class="outline-none"/></i></a></div>
</header>

<style lang="postcss">
    header {
        position: fixed;
        display: grid;
        gap: 0.5rem;
        width: 100%;
        min-width: 750px;
        background: var(--background-color);
        opacity: 0.75;
        box-shadow: 3px 3px 8px 0 var(--background-color);
        --color: #008aff;
        grid-template-columns: max-content auto min-content;
        grid-template-areas: "title nav github";
        z-index: 2;
    }

    header > * {
        align-self: center;
    }

    .title{
        display: flex;
        align-items: center;
        padding: 0.5rem 1rem;
        text-decoration: none;
        color: var(--foreground-color);
        overflow: hidden;
    }

    header nav > ul {
        justify-content: end;
    }

    header a {
        display: flex;
        align-items: center;
        padding: 0 1rem;
        border-radius: 0.5rem;
        text-decoration: none;
        color: var(--foreground-color);
        overflow: hidden;
        position: relative;
        z-index: 1;
        --slantness: 4rem;
    }

    header a::after {
        content: "";
        position: absolute;
        z-index: -1;
        left: calc( (100% + var(--slantness)) * -1);
        top: 0%;
        bottom: 0%;
        width: calc(100% + var(--slantness));
        clip-path: polygon(0% 0%, 100% 0%, calc(100% - var(--slantness)) 100%, 0% 100%);
        background: var(--color);
        opacity: 0;
        transition: all var(--transition);
    }

    header a:hover > i {
        color: var(--background-color);
    }

    header a:hover::after {
        left: 0%;
        opacity: 1;
    }

    .github {
        grid-area: github;
        color: var(--color);
        font-size: 27.5px;
        transition: all var(--transition);
    }

    .github a {
        display: flex;
        align-items: center;
        padding: 6px 1rem;
        border-radius: 0.5rem;
        text-decoration: none;
        color: var(--foreground-color);
        overflow: hidden;
        position: relative;
        z-index: 1;
        --slantness: 4rem;
        margin-right: 1rem;
    }

    nav > ul {
        grid-area: nav;
        place-self: center;
        display: grid;
        grid-auto-flow: column;
        grid-auto-columns: max-content;
        gap: 0.5rem;
        list-style: none;
    }

    nav a > i {
        margin-right: 0.5em;
        color: var(--color);
        font-size: 0.7em;
        transition: all var(--transition);
    }
</style>