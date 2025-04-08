
var inventoryData = [];

// Call populateOrders function when page loads
document.addEventListener('DOMContentLoaded', populateOrders);

async function populateOrders(){
    /*
    Called when the page loads. Retrieves the sales data and populates the containers to display the retrieved data.
    */
    // Get element containers
    const orderTable = document.getElementById("order-table");
    inventoryData = await getInventoryData();
    inventoryData.data.forEach((item, i) => {
        var row = document.createElement("tr");
        var category = document.createElement("td");
        category.innerText = item.category;
        var price = document.createElement("td");
        price.innerText = item.price;
        var name = document.createElement("td");
        name.innerText = item.item_name;
        var quantity = document.createElement("td");
        quantity.innerText = item.quantity;
        var order = document.createElement("td");
        var orderButton = document.createElement("button");
        orderButton.addEventListener('click', function() {
            placeOrder(i);
        });
        orderButton.innerText = "Order"
        orderButton.className = "order-btn";
        order.appendChild(orderButton);
        row.appendChild(name);
        row.appendChild(category);
        row.appendChild(price);
        row.appendChild(quantity);
        row.appendChild(order);
        orderTable.appendChild(row);
    });
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
            alert("Failed to retrieve sales data");
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

function placeOrder(index){
    // index is the item's index in inventoryData
    var item = inventoryData.data[index];
    fetch("http://localhost:8000/inventory/order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "item_name": item.item_name, "category": item.category, "quantity": 1 }),
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status_code === 200) {
            alert(`Successfully placed order for 1 ${item.item_name}`);
        } else {
            alert("Failed to place order: " + data.message);
        }
    })
    .catch(error => {
        console.error(`Error: ${error}`);
        alert(`Error: ${error}`);
    });    
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

