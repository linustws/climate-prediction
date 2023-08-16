<script>
    import Plot from 'svelte-plotly.js';
    import SparkleButton from '$lib/components/SparkleButton.svelte';
    import {onMount} from "svelte";

    let predictionValue = 1;
    let predictionType = 'month';
    let isLoading = false;
    let actualData = [];
    let predictionData = [];
    let data = [];

    const fetchActualData = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error);
            }

            data = await response.json();
            actualData = data['data'];
            actualData = {
                ...actualData,
                'mode': 'lines',
                'name': 'Actual',
                'hovertemplate': 'Datetime: %{x}<br>Mean Temperature: %{y}°C'
            }
            data = [actualData]
            console.log('Actual:', actualData);
        } catch (error) {
            console.error('Error:', error.message);
        }
    };

    onMount(() => {
        fetchActualData();
    });


    const handleSubmit = async (event) => {
        event.preventDefault();
        isLoading = true;
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

            data = await response.json();
            predictionData = data['prediction'];
            predictionData = {
                ...predictionData,
                'mode': 'lines',
                'name': 'Predicted',
                'hovertemplate': 'Datetime: %{x}<br>Mean Temperature: %{y}°C'
            }
            data = [actualData, predictionData]
            console.log('Prediction:', predictionData);
            console.log('Combined:', data);
        } catch (error) {
            console.error('Error:', error.message);
        } finally {
            isLoading = false;
        }
    };
</script>

<div class="content">
    {#if isLoading}
        <!-- Loading bar -->
        <div class="loading-bar">
            <div class="spinner"></div>
        </div>
    {:else}
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
    {/if}
    <div class="plotly-container">
        <Plot {data}
            layout={{
            margin: {t: 50, r: 150, l: 100},
            plot_bgcolor: 'rgba(255, 255, 255, 0)',
            paper_bgcolor: 'rgba(0, 0, 0, 0.75)',
            xaxis: {
                automargin: true,
                color: 'white',
                gridcolor: 'rgba(255, 255, 255, 0.1)',
                title: 'Datetime'
            },
            yaxis: {
                automargin: true,
                color: 'white',
                gridcolor: 'rgba(255, 255, 255, 0.1)',
                title: {
                    text: 'Mean Temperature (°C)',
                    standoff: 20
                },
            },
            modebar: {
                activecolor: 'rgba(255, 255, 255, 0.85)',
                bgcolor: 'rgba(0, 0, 0, 0)',
                color: 'rgba(255, 255, 255, 0.5)',
                orientation: 'v',
            },
            showlegend: true,
            legend: {
                orientation: 'v'
            },
            colorway: ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
        }} config={{scrollZoom: true}}
              fillParent={true}
              debounce={250}
        />
    </div>
</div>

<style lang="postcss">
    .content {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 20px;
    }

    .input-row {
        display: flex;
        align-items: center;
        gap: 10px;
        width: 376px;
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
        border: 3px solid rgba(0, 0, 0, 0.85);
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

    .plotly-container {
        display: flex;
        width: 1100px;
        height: 625px;
        margin: 20px auto 0;
        border-radius: 5px;
        box-shadow: 0 0 16px rgba(0, 0, 0, 0.75);
        overflow: hidden;
    }

    .loading-bar {
        width: 376px; /* Width of the form field */
        height: 46px; /* Height of the form field */
        background-color: rgba(26, 17, 16, 1);
        position: relative;
        border-radius: 100px;
        border: 3px solid rgba(0, 0, 0, 0.75);
        box-shadow: 0 0 calc(0.2em + 1px) rgba(0, 0, 0, 0.1), 0 0 calc(0.4em + 1px) rgba(0, 0, 0, 0.1);
        overflow: hidden; /* Hide overflowing parts */
    }

    .spinner {
        width: 100%;
        height: 100%;
        position: absolute;
        background: linear-gradient(90deg, transparent, rgba(99, 110, 250, 0.8), transparent);
        animation: loading 1.5s infinite;
    }

    @keyframes loading {
        0% {
            transform: translateX(-100%);
        }
        100% {
            transform: translateX(100%);
        }
    }
</style>
