

// Call populateInventory function when page loads
document.addEventListener('DOMContentLoaded', populateInventory);

async function populateInventory(){
    /*
    Called when the page loads. Retrieves the inventory data and populates the containers to display the retrieved data.
    */
    // Get element containers
    const inventoryData = await getInventoryData();

    // Populate inventory table
    const tableBody = document.querySelector('#inventory-table tbody');
    let inventoryRows = '';

    inventoryData.data.forEach(item => {
        inventoryRows += `
            <tr>
                <td>${item.item_name}</td>
                <td>${item.category}</td>
                <td>${item.price}</td>
                <td>${item.quantity}</td>
            </tr>
        `;
    });

    tableBody.innerHTML = inventoryRows;
}

async function getInventoryData() {
    /*
    Retrieves the inventory data and redirects unauthorized users.
    */

    try {
        const response = await fetch("http://localhost:8000/inventory", {
            credentials: 'include'
        });
        if (!response.ok) {
            alert("Failed to retrieve inventory data");
            return;
        }
        const json = await response.json();
        if (json.status_code === 401){
            window.location.href = "../login/index.html"; // Redirect to login page if they don't have access to view the inventory. 
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
