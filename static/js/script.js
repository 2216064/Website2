document.addEventListener("DOMContentLoaded", function () {
    // The navigation bar creation code
    const navBar = document.createElement("nav");
    navBar.className = "navbar";

    const container = document.createElement("div");
    container.className = "container";

    const logo = document.createElement("div");
    logo.className = "logo";

    const logoLink = document.createElement("a");
    logoLink.href = "index.html";
    logoLink.textContent = "Job Platform";

    logo.appendChild(logoLink);

    const navLinks = document.createElement("div");
    navLinks.className = "nav-links";

    const platformLink = createNavLink("Platform", "platform.html");
    const loginLink = createNavLink("Login", "login.html");
    const registerLink = createDropdownNavLink("Register", [
        { text: "Employer", href: "registerEmployer.html" },
        { text: "Student", href: "registerStudent.html" }
    ]);

    document.body.insertBefore(navBar, document.body.firstChild);
    navBar.appendChild(container);
    container.appendChild(logo);
    container.appendChild(navLinks);
    navLinks.appendChild(platformLink);
    navLinks.appendChild(loginLink);
    navLinks.appendChild(registerLink);

    function createNavLink(text, href) {
        const link = document.createElement("a");
        link.href = href;
        link.textContent = text;
        link.style.color = "#ffffff";
        link.style.textDecoration = "none";
        link.style.padding = "10px 15px";
        link.style.transition = "background-color 0.3s";
        link.style.borderRadius = "5px";
        link.addEventListener("mouseover", function () {
            link.style.backgroundColor = "#2a9d8f";
        });
        link.addEventListener("mouseout", function () {
            link.style.backgroundColor = "transparent";
        });
        return link;
    }

    function createDropdownNavLink(text, dropdownItems) {
        const container = document.createElement("div");
        container.className = "dropdown";

        const button = document.createElement("a");
        button.href = "#";
        button.textContent = text;
        button.className = "dropbtn";
        container.appendChild(button);

        const dropdownContent = document.createElement("div");
        dropdownContent.className = "dropdown-content";
        dropdownItems.forEach(item => {
            const link = document.createElement("a");
            link.href = item.href;
            link.textContent = item.text;
            dropdownContent.appendChild(link);
        });

        container.appendChild(dropdownContent);
        return container;
    }

    // Inject CSS styles
    const style = document.createElement("style");
    style.textContent = `
        /* General Styles */
        body, html {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        /* Navbar Styles */
        .navbar {
            background-color: #264653;
            color: #ffffff;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 999;
            padding: 10px 0;
        }

        .navbar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .navbar .logo a {
            color: #ffffff;
            font-size: 1.5rem;
            font-weight: bold;
            text-decoration: none;
        }

        .navbar .nav-links {
            display: flex;
            align-items: center;
        }

        .navbar .nav-links .nav-link {
            color: #ffffff;
            text-decoration: none;
            padding: 10px 15px;
            transition: background-color 0.3s;
            border-radius: 5px;
        }

        .navbar .nav-links .nav-link:hover {
            background-color: #2a9d8f;
        }

        /* Dropdown Styles */
        .dropdown {
            position: relative;
            display: inline-block;
        }

        .dropbtn {
            color: #ffffff;
            text-decoration: none;
            padding: 10px 15px;
            transition: background-color 0.3s;
            border-radius: 5px;
        }

        .dropdown-content {
            display: none;
            position: absolute;
            background-color: #f9f9f9;
            min-width: 160px;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            z-index: 1;
        }

        .dropdown-content a {
            color: black;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
        }

        .dropdown-content a:hover {
            background-color: #f1f1f1;
        }

        .dropdown:hover .dropdown-content {
            display: block;
        }

        .dropdown:hover .dropbtn {
            background-color: #2a9d8f;
        }

        /* Section Styles */
        .section {
            padding: 100px 20px;
            text-align: center;
        }

        .about-section {
            background-image: url("/static/images/new-york-city-5oaa14h4mw6w3o71.jpg");
            background-size: cover;
            background-position: center;
            height: 100vh;
            color: #000;
        }

        .testimonials-section {
            background-image: url("/static/images/1000_F_536022929_rHVla2eMU4AiI95H75ykj6P47LCfEwQo.jpg");
            background-size: cover;
            background-position: center;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            margin-top: 20px;
            color: #000;
        }

        .testimonials-section .testimonial {
            margin: 20px 0;
        }

        /* Container Styles */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Footer Styles */
        footer {
            background-color: #264653;
            color: #ffffff;
            padding: 10px 0;
            text-align: center;
        }
    `;
    document.head.appendChild(style);
});