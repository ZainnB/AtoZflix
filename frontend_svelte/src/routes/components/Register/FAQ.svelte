<script>
    export let questions = [];

    let activeQuestion = null;

    function toggleQuestion(index) {
        activeQuestion = activeQuestion === index ? null : index;
    }
</script>

<section class="faq">
    <h2>Frequently Asked Questions</h2>
    {#each questions as question, index}
        <button
            class="faqbox"
            on:click={() => toggleQuestion(index)}
            aria-expanded={activeQuestion === index}
            type="button"
        >
            <svg
                class="icon"
                width="24"
                height="24"
                fill="none"
                stroke="currentColor"
                xmlns="http://www.w3.org/2000/svg"
            >
                <path d="M6 9l6 6 6-6" />
            </svg>
            <span>{question.title}</span>
        </button>
        {#if activeQuestion === index}
            <div class="faq-content">
                <p>{question.content}</p>
            </div>
        {/if}
    {/each}
</section>

<style>
    .faq {
        padding: 100px 150px;
        background-color: #111;
        color: white;
    }

    .faq h2 {
        font-size: 2rem;
        text-align: center;
        margin-bottom: 20px;
        font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    }

    .faqbox {
        display: flex;
        align-items: center;
        width: 100%;
        max-width: 800px;
        margin: 10px auto;
        padding: 15px;
        background: #111;
        cursor: pointer;
        border: none;
        color: white;
        font-size: 1rem;
        border-bottom: 1px solid #333;
        font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    }

    .faqbox:hover .icon {
        stroke: #098577;
    }

    .faqbox svg {
        margin-right: 15px; /* Space between icon and text */
        transition: stroke 0.2s;
        flex-shrink: 0; /* Prevent the icon from resizing */
    }

    .faqbox span {
        text-align: left;
        flex: 1; /* Allow the text to take remaining space */
    }

    .faq-content {
        padding: 15px;
        background: #222;
        margin-top: 5px;
        border-left: 3px solid #098577;
        font-family: Arial, sans-serif;
    }
</style>
