document.addEventListener("DOMContentLoaded", function() {
    // Initialize AOS
    AOS.init();

    // Fetch and display job listings
    fetchJobs();

    function fetchJobs(query = "") {
        fetch("/api/search_jobs" + query) 
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Fetched job listings:", data);  // Log fetched data
                const jobNoticeboard = document.getElementById("jobNoticeboard");
                jobNoticeboard.innerHTML = "";  // Clear existing job cards

                data.forEach(job => {
                    const jobCard = createJobCard(job);
                    jobNoticeboard.appendChild(jobCard);
                });
            })
            .catch(error => console.error("Error fetching job listings:", error));
    }

    function createJobCard(job) {
        const jobCard = document.createElement("div");
        jobCard.className = "job-card card shadow-sm";
        jobCard.setAttribute("data-aos", "fade-up");

        const jobCardBody = document.createElement("div");
        jobCardBody.className = "card-body";

        const jobTitle = document.createElement("h5");
        jobTitle.className = "card-title";
        jobTitle.textContent = job.Title;

        const employer = document.createElement("h6");
        employer.className = "card-subtitle mb-2 text-muted";
        employer.textContent = job.EmployerID; // Assuming EmployerID is used to fetch or display employer's info

        const details = document.createElement("div");
        details.className = "card-text";

        const location = document.createElement("p");
        location.className = "location";
        location.innerHTML = `<i class="fas fa-map-marker-alt"></i> Location: ${job.Location}`;

        const salary = document.createElement("p");
        salary.className = "salary";
        salary.innerHTML = `<i class="fas fa-dollar-sign"></i> Salary: ${job.Salary}`;

        details.appendChild(location);
        details.appendChild(salary);

        jobCardBody.appendChild(jobTitle);
        jobCardBody.appendChild(employer); // Re-including as it was originally fetching "employer".
        jobCardBody.appendChild(details);

        if (job.Description) {
            const description = document.createElement("p");
            description.className = "job-description";
            description.textContent = job.Description;
            jobCardBody.appendChild(description);
        }

        jobCard.appendChild(jobCardBody);

        return jobCard;
    }

    // Handle search form submission
    document.getElementById("searchForm").addEventListener("submit", function(event) {
        event.preventDefault();
        const jobTitle = document.getElementById("jobTitle").value.trim();
        const location = document.getElementById("location").value.trim();
        const query = `?title=${encodeURIComponent(jobTitle)}&location=${encodeURIComponent(location)}`;
        fetchJobs(query);
    });

    // Inject CSS styles for the sticky-search-bar
    const style = document.createElement("style");
    style.textContent = `
        .sticky-container {
            position: relative;
            z-index: 800; /* Ensure it's below the top-nav */
        }

        .sticky-search-bar {
            position: sticky;
            top: 60px; /* Adjust according to the height of your top-nav */
            background-color: #3498db;
            padding: 10px 20px;
            text-align: center;
            z-index: 1000; /* Ensure it's above other content */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-bottom: 1px solid #ddd;
        }

        .sticky-search-bar form {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
        }

        .sticky-search-bar label {
            font-size: 1rem;
            color: #ffffff;
            margin-right: 10px;
        }

        .sticky-search-bar input,
        .sticky-search-bar button {
            padding: 10px;
            margin: 5px;
            border-radius: 5px;
            border: none;
            outline: none;
        }

        .sticky-search-bar input {
            flex: 1;
            min-width: 200px;
        }

        .sticky-search-bar button {
            background-color: #27ae60;
            color: #ffffff;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .sticky-search-bar button:hover {
            background-color: #1e8449;
        }

        .job-noticeboard {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            padding-top: 20px; /* Space below the sticky bar */
        }

        .job-card {
            width: 100%;
            max-width: 400px;
            border-radius: 10px;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .job-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        }

        .job-card .card-body {
            background-color: #ffffff;
            padding: 20px;
        }

        .job-card .card-title {
            font-size: 1.25rem;
            font-weight: bold;
        }

        .job-card .card-subtitle {
            margin-bottom: 10px;
        }

        .job-card .card-text {
            margin-bottom: 15px;
        }

        .job-card .location,
        .job-card .salary {
            font-size: 0.9em;
        }

        .job-card .location i,
        .job-card .salary i {
            margin-right: 5px;
        }

        footer {
            background-color: #264653;
            color: #ffffff;
            padding: 15px 0;
            text-align: center;
            font-family: "Roboto", sans-serif;
        }

        .container p {
            margin: 0;
        }
    `;
    document.head.appendChild(style);
});
