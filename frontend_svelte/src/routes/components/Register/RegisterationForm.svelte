<script>
  let email = "";
  let username = "";
  let password = "";
  let errorMessage = "";
  let successMessage = "";

  const submitForm = async () => {
    errorMessage = "";
    successMessage = "";

    try {
      const response = await fetch("http://127.0.0.1:5000/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, username, password }),
      });

      if (response.ok) {
        const result = await response.json();
        successMessage = result.message;
      } else {
        const error = await response.json();
        errorMessage = error.message || "Registration failed.";
      }
    } catch (error) {
      errorMessage = "An error occurred: " + error.message;
    }
  };
</script>

<div class="main">
  <!-- Heading Section -->
  <h1>Endless Recommendations, Tailored just for You.</h1>
  <h2>
    Explore movies that match your taste. Ready to discover your next favorite?
  </h2>
  <h2>Enter your email to get personalized recommendations.</h2>

  <!-- Registration Form -->
  <form on:submit|preventDefault={submitForm}>
    <label for="email">Email:</label>
    <input
      id="email"
      type="email"
      bind:value={email}
      placeholder="Enter your email"
      required
    />

    <label for="username">Username:</label>
    <input
      id="username"
      type="text"
      bind:value={username}
      placeholder="Enter your username"
      required
    />

    <label for="password">Password:</label>
    <input
      id="password"
      type="password"
      bind:value={password}
      placeholder="Enter your password"
      required
    />

    <button type="submit">Get Started ></button>

    {#if errorMessage}
      <p style="color: red;">{errorMessage}</p>
    {/if}

    {#if successMessage}
      <p style="color: green;">{successMessage}</p>
    {/if}
  </form>
</div>

<style>
  .main {
    background-size: cover;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    flex-direction: column;
    background-color: rgba(0, 0, 0, 0.7);
    text-align: center;
  }

  h1,
  h2 {
    color: white;
    font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    font-weight: 600;
    margin: 10px;
  }

  h1 {
    font-size: 30px;
    font-weight: 700;
    margin-top: 00px;
  }

  h2 {
    font-size: 17px;
    font-weight: 400;
    margin-top: 20px;
  }

  form {
    display: flex;
    flex-direction: column;
    width: 300px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 8px;
    justify-content: centre;
    align-items: centre;
  }

  label {
    margin-top: 12px;
    font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    font-size: 16px;
    color: white;
  }

  input {
    margin-top: 5px;
    padding: 10px;
    font-size: 16px;
    font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    border-radius: 5px;
    border: 1px solid #333;
    background-color: #000;
    color: white;
  }

  button {
    width: 180px;
    margin-top: 40px;
    padding: 12px;
    font-size: 16px;
    background-color: #098577;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
    align-self: center;
  }

  button:hover {
    background-color: #064e45;
  }
</style>
