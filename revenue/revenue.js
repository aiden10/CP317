

// Call populateRevenue function when page loads
document.addEventListener('DOMContentLoaded', populateRevenue);

async function populateRevenue(){
    /*
    Called when the page loads. Retrieves the revenue data and populates the containers to display the retrieved data.
    */
    // Get element containers
    const insightsPanel = document.getElementById("insights-panel");
    const chartContainer = document.getElementById("chart-container");
    const incomeContainer = document.getElementById("income-container");
    const revenueData = await getRevenueData();
    insightsPanel.innerText = revenueData.data.insight;
    var incomeNotes = "";
    revenueData.data.income_notes.forEach(note => {
        incomeNotes += `
        <div class="income-panel">
            <span>
                ${note}
            </span>
        </div>`
    });
    incomeContainer.innerHTML = incomeNotes;

    var chart = new Image();
    chart.setAttribute('src', `data:image/jpg;base64,${revenueData.data.chart}`)
    chart.width = 650;
    chart.height = 325;
    chartContainer.appendChild(chart);
}

async function getRevenueData() {
    /*
    Retrieves the revenue data and redirects unauthorized users.
    */

    try {
        const response = await fetch("http://localhost:8000/revenue", {
            credentials: 'include'
        });
        if (!response.ok) {
            alert("Failed to retrieve revenue data");
            return;
        }
        const json = await response.json();
        if (json.status_code === 401){
            window.location.href = "../login/index.html"; // Redirect to login page if they don't have access to view the dashboard. 
            return;
        } 
        return json;

    } catch (error) {
        console.error(error);
    }
}

function showLeftPanel(){
    var leftPanel = document.getElementById("left-panel");
    leftPanel.classList.toggle("open");
}

// Function to handle logout
function logout() {
    // Send GET request to the /logout endpoint
    fetch("http://localhost:8000/logout", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "include",
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status_code === 200) {
            // Clear the session_token cookie
            document.cookie = "session_token=; path=/; max-age=0";

            // Redirect to the login page
            window.location.href = "../login/index.html";
        } else {
            console.error("Logout failed", data.message);
        }
    })
    .catch((error) => {
        console.error("Error during logout:", error);
    });
}