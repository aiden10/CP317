

// Call populateOrders function when page loads
document.addEventListener('DOMContentLoaded', populateOrders);

async function populateOrders(){
    /*
    Called when the page loads. Retrieves the order data and populates the containers to display the retrieved data.
    */
    // Get element containers
    const orderData = await getOrderData();
    insightsPanel.innerText = orderData.data.insight;
    var incomeNotes = "";
    orderData.data.income_notes.forEach(note => {
        incomeNotes += `
        <div class="income-panel">
            <span>
                ${note}
            </span>
        </div>`
    });
    incomeContainer.innerHTML = incomeNotes;
}

async function getOrderData() {
    /*
    Retrieves the order data and redirects unauthorized users.
    */

    try {
        const response = await fetch("http://localhost:8000/order", {
            credentials: 'include'
        });
        if (!response.ok) {
            alert("Failed to retrieve order data");
            return;
        }
        const json = await response.json();
        if (json.status_code === 401){
            window.location.href = "../login/index.html"; // Redirect to login page if they don't have access to view the order. 
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
