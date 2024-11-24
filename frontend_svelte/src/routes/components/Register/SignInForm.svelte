<script>
    export let onClose; // Function to close the form
    let usernameOrEmail = ""; // Variable to hold username or email
    let password = "";
  
    const handleSignIn = async () => {
  console.log("Username or Email:", usernameOrEmail); // Debug input values
  console.log("Password:", password);

  const response = await fetch("http://127.0.0.1:5000/api/signin", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: usernameOrEmail, password }),
  });

  const data = await response.json();
  console.log("Response from Backend:", data); // Debug backend response

  if (data.success) {
    alert("Login successful!");

    // Save credentials to localStorage
    localStorage.setItem("user", JSON.stringify({
      username: usernameOrEmail,
      token: data.token, // Assuming the backend sends a token
    }));

    // Redirect to home
    window.location.href = "./Home";
  } else {
    alert(data.message || "Invalid credentials!");
  }
};

  </script>
  
  <div class="overlay">
    <div class="form-container">
      <button class="close-btn" on:click={onClose}>X</button>
      <h2>Sign In</h2>
      <form on:submit|preventDefault={handleSignIn}>
        <label for="usernameOrEmail">Username or Email:</label>
        <input
          type="text"
          id="usernameOrEmail"
          bind:value={usernameOrEmail}
          placeholder="Enter username or email"
          required
        />
  
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          bind:value={password}
          placeholder="Enter password"
          required
        />
  
        <button type="submit" >Sign In</button>
      </form>
    </div>
  </div>
  
  <style>
    .overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.8);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000;
    }
  
    .form-container {
      background: #098577;
      padding: 20px;
      border-radius: 8px;
      width: 300px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      text-align: center;
      border: 3px solid #ffffff;
    }
  
    .form-container h2 {
      margin-bottom: 20px;
      color: rgb(0, 0, 0);
    }
  
    .form-container label {
      display: block;
      margin-bottom: 8px;
      color: rgb(0, 0, 0);
      font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    }
  
    .form-container input {
      width: 100%;
      padding: 8px;
      margin-bottom: 16px;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
      border: 1px solid #333;
      background-color: #000;
      color: white;
      font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    }
  
    .form-container button {
      background-color: #000000;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 5px;
      cursor: pointer;
      font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    }
  
    .form-container button:hover {
      background-color: #064e45;
    }
  
    .close-btn {
      background-color: #098577;
      border: none;
      font-size: 18px;
      cursor: pointer;
      position: absolute;
      top: 10px;
      right: 10px;
    }
  </style>
  