<script>
    import SparkleButton from '$lib/components/SparkleButton.svelte';

    let predictionValue = 1;
    let predictionType = 'month';

    const handleSubmit = async (event) => {
        event.preventDefault();
        // Make an API call to your backend here with the form data
        const formData = {
            value: predictionValue,
            type: predictionType,
        };
        console.log('Form data:', formData);
        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error);
            }

            const data = await response.json();
            console.log('Prediction:', data.prediction);
            // Process the prediction data as needed.
        } catch (error) {
            console.error('Error:', error.message);
            // Handle any errors that occur during the API call.
        }
    };
</script>

<div class="content">
    <form on:submit={handleSubmit}>
        <div class="input-row">
            <div class="input-container">
                <label for="prediction-value" class="label">Predict for:</label>
                <div class="input-fields">
                    <input type="number" id="prediction-value" bind:value={predictionValue} min="1" max="100"/>
                    <select id="prediction-type" bind:value={predictionType}>
                        <option value="month">months</option>
                        <option value="year">years</option>
                    </select>
                </div>
            </div>
            <SparkleButton type="submit" buttonText="Predict"/>
        </div>
    </form>
</div>

<style lang="postcss">
    .content {
        display: flex;
        margin-top: 25px;
        justify-content: center;
    }

    .input-row {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .label {
        font-size: 1rem;
        font-weight: 500;
        padding: 4px 8px;
        border-radius: 5px;
        color: #333;
    }

    .input-container {
        display: flex;
        align-items: center;
        gap: 10px;
        overflow: hidden;
        border: 1px solid #ccc;
        background-color: rgba(255, 255, 255, 1);
        margin-right: 20px;
        box-shadow: 0 0 calc(0.2em + 1px) rgba(0, 0, 0, 0.1), 0 0 calc(0.4em + 1px) rgba(0, 0, 0, 0.1);
        border-radius: 100px;
    }

    .input-fields {
        display: flex;
        align-items: center;
    }

    input[type="number"],
    select {
        font-size: 1rem;
        font-weight: 500;
        border: none;
        background-color: transparent;
        outline: none;
        appearance: none;
        color: #333;
    }

    select {
        width: 80px;
        padding: 8px 12px;
    }

    input[type="number"] {
        width: 50px;
        padding: 8px 0;
    }

    select {
        -webkit-appearance: none;
        -moz-appearance: none;
    }

    .input-fields select {
        padding-right: 8px;
    }
</style>
