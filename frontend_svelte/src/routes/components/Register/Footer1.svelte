<footer class="footer">
    <div class="footer-content">
        <div class="creators">
            <div class="creator">
                <img src="/assets/img/ZainB.png" alt="Zain Baig" class="creator-pic" />
                <div class="creator-info">
                    <p>Zain Baig</p>
                    <a href="https://www.linkedin.com/in/zain-baig-04790b260/" target="_blank">LinkedIn</a>
                </div>
            </div>
            <div class="creator">
                <img src="/assets/asad-pic.jpg" alt="Asad Irfan" class="creator-pic" />
                <div class="creator-info">
                    <p>Asad Irfan</p>
                    <a href="https://www.linkedin.com/in/asad-irfan" target="_blank">LinkedIn</a>
                </div>
            </div>
        </div>
    </div>
    <div class="footer-country">
        <select name="country" id="country" title="Select Language">
            <option value="en">English</option>
            <option value="ur">Urdu</option>
        </select>
        <p>AtoZFlix Pakistan</p>
    </div>
    <div class="footer-bottom">
        <p>&copy; 2024 Smart Movie Recommendation System. All rights reserved.</p>
        <p><a href="mailto:contact@project.com" class="contact-link">Contact Us</a></p>
    </div>
</footer>

<style>
    .footer {
        background: #111;
        color: white;
        padding: 40px 20px;
        font-family: Arial, sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .footer-content {
        width: 100%;
        max-width: 1200px;
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 30px;
        margin-bottom: 20px;
    }

    .creators {
        display: flex;
        justify-content: space-around;
        gap: 30px;
    }

    .creator {
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .creator-pic {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 10px;
        border: 2px solid #098577;
    }

    .creator-info p {
        font-weight: bold;
        margin-bottom: 5px;
        font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    }

    .creator-info a {
        color: #098577;
        text-decoration: none;
        font-size: 0.9rem;
    }

    .creator-info a:hover {
        text-decoration: underline;
    }

    .footer-country {
        margin-top: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        max-width: 1200px;
    }

    select {
        padding: 8px;
        border-radius: 4px;
        background-color: #222;
        color: white;
        border: none;
        font-size: 0.9rem;
        cursor: pointer;
        font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    }

    .footer-bottom {
        margin-top: 20px;
        text-align: center;
        font-size: 0.9rem;
    }

    .footer-bottom a {
        color: #098577;
        text-decoration: none;
        font-family: 'Netflix Sans', 'Helvetica Neue', 'Segoe UI', 'Roboto', 'Ubuntu', sans-serif;
    }

    .footer-bottom a:hover {
        text-decoration: underline;
    }
</style>
