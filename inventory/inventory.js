

// Call populateDashboard function when page loads
document.addEventListener('DOMContentLoaded', populateDashboard);

async function populateDashboard(){
    /*
    Called when the page loads. Retrieves the dashboard data and populates the containers to display the retrieved data.
    */
    // Get element containers
    const updatesList = document.getElementById("updates-list");
    const insightsPanel = document.getElementById("insights-panel");
    const chartContainer = document.getElementById("chart-container");
    const incomeContainer = document.getElementById("income-container");
    const dashboardData = await getDashboardData();
    insightsPanel.innerText = dashboardData.data.insight;
    var incomeNotes = "";
    dashboardData.data.income_notes.forEach(note => {
        incomeNotes += `
        <div class="income-panel">
            <span>
                ${note}
            </span>
        </div>`
    });
    incomeContainer.innerHTML = incomeNotes;

    var updates = "";
    dashboardData.data.updates.forEach(update => {
        updates += `
        <li>
            ${update}
        </li>`
    });
    updatesList.innerHTML = `<ul>${updates}</ul>`;
    var chart = new Image();
    chart.setAttribute('src', `data:image/jpg;base64,${dashboardData.data.chart}`)
    chart.width = 650;
    chart.height = 325;
    chartContainer.appendChild(chart);
}

async function getDashboardData() {
    /*
    Retrieves the dashboard data and redirects unauthorized users.
    */

    try {
        const response = await fetch("http://localhost:8000/dashboard", {
            credentials: 'include'
        });
        if (!response.ok) {
            alert("Failed to retrieve dashboard data");
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