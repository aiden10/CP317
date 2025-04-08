
// place-holder employee info
var employees = [
    { name: "Alice Smith", pay: "$22.25", hours: "35h", position: "Bakery Manager" },
    { name: "Bob Johnson", pay: "$18.50", hours: "30h", position: "Cashier" },
    { name: "Charlie Brown", pay: "$25.00", hours: "40h", position: "Head Chef" },
    { name: "Diana Prince", pay: "$20.00", hours: "28h", position: "Barista" },
    { name: "Edward Blake", pay: "$19.75", hours: "32h", position: "Stock Clerk" },
  ];

// Call populateEmployees function when page loads
document.addEventListener('DOMContentLoaded', populateEmployees);

async function populateEmployees(){
    /*
    Called when the page loads. Retrieves the employees data and populates the containers to display the retrieved data.
    */
    // Get element containers
    const employeesList = document.getElementById("employee-list");
    const employeesData = await getEmployeesData();
    employees = employeesData.data;
    var employeeButtons = "";
    var i = 0;
    employeesData.data.forEach(employee => {
        employeeButtons += `
        <button class="employee-button" onclick=\"selectEmployee(${i})\">
            ${employee.first_name + " " + employee.last_name}
        </button>
        `
        i++;
    });
    employeesList.innerHTML = employeeButtons;
}

async function getEmployeesData() {
    /*
    Retrieves the employees data and redirects unauthorized users.
    */

    try {
        const response = await fetch("http://localhost:8000/employees", {
            credentials: 'include'
        });
        if (!response.ok) {
            alert("Failed to retrieve employees data");
            return;
        }
        const json = await response.json();
        if (json.status_code === 401){
            window.location.href = "../login/index.html"; // Redirect to login page if they don't have access to view the employees. 
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

  function selectEmployee(index) {
    const emp = employees[index];

    // Hide placeholder message, show details
    document.getElementById("placeholder-message").style.display = "none";
    document.getElementById("employee-details").style.display = "flex";

    document.getElementById("employee-name").textContent = emp.first_name + " " + emp.last_name;
    document.getElementById("pay").textContent = emp.pay;
    document.getElementById("hours").textContent = emp.weekly_hours;
    document.getElementById("position").textContent = emp.position;
  }


  function changeLocation() {
    const selected = document.getElementById("location-select").value;
    console.log("Location changed to:", selected);
    // Optional: trigger employee filtering or backend call here
  }