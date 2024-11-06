let currentPage = { customers: 1, sales: 1, products: 1 };
const itemsPerPage = { customers: 10, sales: 10, products: 10 };
let customersData = [], salesData = [], productsData = []; // Store fetched data for filtering

// Function to fetch data from an API endpoint
async function fetchData(endpoint) {
    const response = await fetch(endpoint);

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    return await response.json();
}

async function loadAnalyticsData() {
    try {
        // Existing analytics data fetching
        const totalCustomers = await fetchData('http://localhost:5000/api/stats/total-customers');
        document.querySelector('#total-customers span').innerText = totalCustomers.total_customers;

        const totalSales = await fetchData('http://localhost:5000/api/stats/total-sales');
        document.querySelector('#total-sales span').innerText = totalSales.total_sales;

        const totalRevenue = await fetchData('http://localhost:5000/api/stats/total-revenue');
        document.querySelector('#total-revenue span').innerText = totalRevenue.total_revenue;

        const averageOrderValue = await fetchData('http://localhost:5000/api/stats/average-order-value');
        document.querySelector('#average-order-value span').innerText = averageOrderValue.average_order_value;

        const salesByCategory = await fetchData('http://localhost:5000/api/stats/sales-by-category');
        loadSalesByCategoryChart(salesByCategory);

        loadRevenueChart();

        const salesByProduct = await fetchData('http://localhost:5000/api/stats/sales-by-product');
        populateSalesByProductTable(salesByProduct);

        const salesTrend = await fetchData('http://localhost:5000/api/stats/sales-trend');
        loadSalesTrendChart(salesTrend);

        const topCustomers = await fetchData('http://localhost:5000/api/stats/top-customers');
        populateTopCustomersByRevenueTable(topCustomers);

        const topProducts = await fetchData('http://localhost:5000/api/stats/top-products');
        populateTopProductsBySalesTable(topProducts);

        // Load existing tables
        const customersData = await fetchData('http://localhost:5000/api/stats/customers');
        populateCustomersTable(customersData);

        const productsData = await fetchData('http://localhost:5000/api/stats/products');
        populateProductsTable(productsData);

        const salesData = await fetchData('http://localhost:5000/api/stats/sales');
        populateSalesTable(salesData);

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}



// Function to load the Sales by Category chart
function loadSalesByCategoryChart(data) {
    const ctx = document.getElementById('salesByCategoryChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.category),
            datasets: [{
                label: 'Sales by Category',
                data: data.map(item => item.total_quantity),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            }]
        },
        options: {}
    });
}

// Function to load a placeholder revenue chart
function loadRevenueChart() {
    const ctx = document.getElementById('revenueChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May'],
            datasets: [{
                label: 'Revenue',
                data: [12000, 19000, 30000, 50000, 40000],
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false,
            }]
        },
        options: {}
    });
}

// Function to show the appropriate section based on user interaction
function showSection(section) {
    document.querySelectorAll('.section').forEach(sec => sec.style.display = 'none');
    document.getElementById(section).style.display = 'block';
    if (section === 'analytics') loadAnalyticsData();
}

// Function to populate the sales table with the fetched sales data
function populateSalesTable(data) {
    const tableBody = document.querySelector(`#sales-table tbody`);
    tableBody.innerHTML = '';

    data.sort((a, b) => new Date(b.sale_date) - new Date(a.sale_date));

    data.slice((currentPage['sales'] - 1) * itemsPerPage['sales'], currentPage['sales'] * itemsPerPage['sales']).forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${item.sale_id}</td><td>${item.product_id}</td><td>${item.customer_id}</td><td>${item.sale_date}</td><td>${item.quantity}</td><td>${item.total_amount}</td>`;
        tableBody.appendChild(row);
    });
}

// Function to populate the products table
function populateProductsTable(data) {
    const tableBody = document.querySelector(`#products-data-table tbody`);
    tableBody.innerHTML = '';

    data.slice((currentPage['products'] -1) * itemsPerPage['products'], currentPage['products'] * itemsPerPage['products']).forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${item.product_name}</td><td>$${item.price}</td><td>${item.stock_quantity}</td>`;
        tableBody.appendChild(row);
    });
}

// Function to populate the customers table
function populateCustomersTable(data) {
    const tableBody = document.querySelector(`#customers-table tbody`);
    tableBody.innerHTML = '';

    data.slice((currentPage['customers'] - 1) * itemsPerPage['customers'], currentPage['customers'] * itemsPerPage['customers']).forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${item.customer_name}</td><td>${item.email}</td><td>${item.phone}</td><td>${item.city}</td>`;
        tableBody.appendChild(row);
    });
}

function populateTotalRevenueByCustomerTable(data) {
    const tableBody = document.querySelector(`#total-revenue-by-customer tbody`);
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${item.customer_name}</td><td>$${item.total_revenue}</td>`;
        tableBody.appendChild(row);
    });
}


function populateSalesByProductTable(data) {
    const tableBody = document.querySelector(`#sales-by-product tbody`);
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${item.product_name}</td><td>${item.total_quantity_sold}</td><td>$${item.total_revenue}</td>`;
        tableBody.appendChild(row);
    });
}

function loadSalesTrendChart(data) {
    const ctx = document.getElementById('salesTrendChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(item => item.month),
            datasets: [{
                label: 'Sales Trend',
                data: data.map(item => item.total_sales),
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false,
            }]
        },
        options: {}
    });
}

function populateTopCustomersByRevenueTable(data) {
    const tableBody = document.querySelector(`#top-customers-by-revenue tbody`);
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${item.customer_name}</td><td>$${item.total_revenue}</td>`;
        tableBody.appendChild(row);
    });
}

function populateTopProductsBySalesTable(data) {
    const tableBody = document.querySelector(`#top-products-by-sales tbody`);
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${item.product_name}</td><td>${item.total_quantity_sold}</td><td>$${item.total_revenue}</td>`;
        tableBody.appendChild(row);
    });
}


// Pagination functions for customers, sales, and products tables
function prevPage(table) {
    if (currentPage[table] > 1) {
        currentPage[table]--;
        if (table === 'customers') populateCustomersTable(customersData);
        if (table === 'sales') populateSalesTable(salesData);
        if (table === 'products') populateProductsTable(productsData);
    }
}

function nextPage(table) {
    const totalItems = table === 'customers' ? customersData.length : table === 'sales' ? salesData.length : productsData.length;
    if (currentPage[table] * itemsPerPage[table] < totalItems) {
        currentPage[table]++;
        if (table === 'customers') populateCustomersTable(customersData);
        if (table === 'sales') populateSalesTable(salesData);
        if (table === 'products') populateProductsTable(productsData);
    }
}

// Load the initial data and show the analytics section on page load
window.onload = function() {
    showSection('analytics');
};

