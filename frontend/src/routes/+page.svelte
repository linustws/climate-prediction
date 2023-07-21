<script>
    import SparkleButton from '$lib/components/SparkleButton.svelte';
    let predictionValue = 1;
    let predictionType = 'month';
</script>

<div class="content">
    <div class="input-row">
        <label for="prediction-value">Predict for:</label>
        <input type="number" id="prediction-value" bind:value={predictionValue} min="1" max="100" />
        <select id="prediction-type" bind:value={predictionType}>
            <option value="month">months</option>
            <option value="year">years</option>
        </select>
        <SparkleButton buttonText="Predict" />
    </div>
</div>

<style lang="postcss">
    .sparkle-button {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }

    .content {
        display: flex;
        margin-top: 25px; /* Space below the navbar */
        justify-content: center;
    }

    .input-row {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    label {
        font-size: 16px;
        font-weight: bold;
    }

    input[type="number"],
    select {
        font-size: 16px;
        padding: 5px;
    }
</style>
