<script>
    import SparkleButton from '$lib/components/SparkleButton.svelte';
    let predictionValue = 1;
    let predictionType = 'month';
</script>

<div class="content">
    <div class="input-row">
        <div class="input-container">
            <label for="prediction-value" class="label">Predict for:</label>
            <div class="input-fields">
                <input type="number" id="prediction-value" bind:value={predictionValue} min="1" max="100" />
                <select id="prediction-type" bind:value={predictionType}>
                    <option value="month">months</option>
                    <option value="year">years</option>
                </select>
            </div>
        </div>
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

    .label {
        font-size: 16px;
        font-weight: bold;
        padding: 4px 8px; /* Add some padding to the label */
        border-radius: 5px;
        color: #333; /* Adjust font color for better readability */
    }

    .input-container {
        display: flex;
        align-items: center;
        gap: 10px;
        border-radius: 5px;
        overflow: hidden;
        border: 1px solid #ccc;
        background-color: rgba(255, 255, 255, 0.8); /* Add background color to the input container */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Add a subtle box-shadow */
    }

    .input-fields {
        display: flex;
        align-items: center;
    }

    input[type="number"],
    select {
        font-size: 16px;
        padding: 8px 12px;
        border: none;
        background-color: transparent;
        outline: none;
        appearance: none;
        width: 80px;
        color: #333; /* Adjust font color for better readability */
    }

    select {
        -webkit-appearance: none;
        -moz-appearance: none;
    }

    .input-fields select {
        padding-right: 8px;
    }
</style>
