<script>
    import { onMount } from 'svelte';
    import flatpickr from 'flatpickr';
    import 'flatpickr/dist/flatpickr.min.css'; // Import flatpickr styles

    let tableData = [];
    let filteredData = [];
    let selectedUser = '';
    let selectedStartTime = '';
    let selectedEndTime = '';
    let isFilterApplied = false;
    let allUsernames = [];

    let calendarStart;
    let calendarEnd;

    function formatDate(date) {
        const year = date.getFullYear();
        const month = date.getMonth() + 1; // January is 0
        const day = date.getDate();
        return `${year}-${month}-${day}`;
    }

    async function fetchUsernames() {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/usernames');
            if (response.ok) {
                allUsernames = await response.json();
            } else {
                throw new Error('Failed to fetch usernames');
            }
        } catch (error) {
            console.error(error);
        }
    }

    async function fetchTableData(startDate, endDate, name) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/table_data?start_date=${startDate}&end_date=${endDate}&name=${name}`);
            if (response.ok) {
                tableData = await response.json();
                filteredData = tableData; // Initialize filteredData with all tableData
            } else {
                throw new Error('Failed to fetch data');
            }
        } catch (error) {
            console.error(error);
        }
    }

    onMount(async () => {
        try {
            await fetchUsernames();
            const today = formatDate(new Date()); // Get today's date formatted as YYYY-M-D
            await fetchTableData(today, today, selectedUser); // Initially fetch data with selectedName as empty
            calendarStart = flatpickr("#startTimeSelect", {
                defaultDate: 'today',
                enableTime: false,
                dateFormat: "Y-m-d"
            });
            calendarEnd = flatpickr("#endTimeSelect", {
                defaultDate: 'today',
                enableTime: false,
                dateFormat: "Y-m-d"
            });
        } catch (error) {
            console.error(error);
        }
    });

    function filterTable() {
        const startDate = calendarStart.selectedDates[0];
        const endDate = calendarEnd.selectedDates[0];
        const formattedStartDate = formatDate(startDate);
        const formattedEndDate = formatDate(endDate);
        fetchTableData(formattedStartDate, formattedEndDate, selectedUser); // Pass selectedName to fetchTableData
        isFilterApplied = true;
    }

    // Function to reset all selections and show all table data
    async function resetFilter() {
        selectedUser = '';
        selectedStartTime = '';
        selectedEndTime = '';
        calendarStart.setDate(new Date());
        calendarEnd.setDate(new Date());
        isFilterApplied = false;
        const today = formatDate(new Date());
        await fetchTableData(today, today, selectedUser); // Fetch data with today's date after resetting the filter
    }
</script>

<main class="container">
    <h1 class="mt-4">Table Data</h1>

    <div class="search-bar">
        <div class="form-group">
            <label for="userSelect">Select User:</label>
            <select class="form-control" id="userSelect" bind:value={selectedUser}>
                <option value="">Name</option>
                {#each allUsernames as user}
                    <option value={user}>{user}</option>
                {/each}
            </select>
        </div>

        <div class="form-group">
            <label for="startTimeSelect">Select Start Date:</label>
            <input type="text" class="form-control" id="startTimeSelect">
        </div>

        <div class="form-group">
            <label for="endTimeSelect">Select End Date:</label>
            <input type="text" class="form-control" id="endTimeSelect">
        </div>

        <button class="btn btn-primary" on:click={filterTable}>Apply Filter</button>
        <button class="btn btn-secondary" on:click={resetFilter} disabled={!isFilterApplied}>Reset Filters</button>
    </div>

    <div class="table-container">
        <table class="table mt-4">
            <thead>
                <tr>
                    {#if filteredData.length > 0}
                        {#each ['Task ID', 'Repetition Count Sum', 'Project Name', 'Start Time', 'End Time', 'Duration', 'User Name'] as column}
                            <th>{column}</th>
                        {/each}
                    {:else}
                        <th colspan="7">No data available</th>
                    {/if}
                </tr>
            </thead>
            <tbody>
                {#if filteredData.length > 0}
                    {#each filteredData as row}
                        <tr>
                            <td>{row.distinct_task_id_count}</td>
                            <td>{row.repetition_counts_sum}</td>
                            <td>{row.project_name}</td>
                            <td>{row.start_time}</td>
                            <td>{row.end_time}</td>
                            <td>{row.duration_hours} : {row.duration_minutes} h</td>
                            <td>{row.username}</td>
                        </tr>
                    {/each}
                {/if}
            </tbody>
        </table>
    </div>
</main>

<style>
    main {
        text-align: center;
        padding: 0 20px;
    }

    h1 {
        color: #ff3e00;
        text-transform: uppercase;
        font-size: 2.5em;
        font-weight: 100;
    }

    .search-bar {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .form-group {
        flex: 1;
        margin-right: 10px;
    }

    .table-container {
        overflow-x: auto;
    }

    @media screen and (max-width: 768px) {
        .form-group {
            flex-basis: 100%;
            margin-right: 0;
            margin-bottom: 10px;
        }

        .form-group:last-child {
            margin-bottom: 0;
        }
    }

    .table {
        width: 100%;
    }
</style>
