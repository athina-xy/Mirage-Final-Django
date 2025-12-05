
// title & description limit
const TITLE_MAX = 50;
const DESC_MAX = 200;

let tasks = JSON.parse(localStorage.getItem("mirageTasks")) || [];
let filterMode = "all";


// Set the minimum selectable date to today in the date input
function setDateMinToday() {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, "0");
    const dd = String(today.getDate()).padStart(2, "0");
    const todayStr = `${yyyy}-${mm}-${dd}`;

    $("#taskDate").attr("min", todayStr);
}

// Check if a date string (yyyy-mm-dd) is today or in the future
function isTodayOrFuture(dateStr) {
    const selected = new Date(dateStr);
    const today = new Date();

    // Compare only dates (remove time part)
    selected.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    return selected >= today;
}

// Validate fields before adding a task
function validateNewTask(name, desc, date) {
    const errors = [];

    if (!name) {
        errors.push("Title is required.");
    } else if (name.length > TITLE_MAX) {
        errors.push(`Title must be at most ${TITLE_MAX} characters.`);
    }

    if (!desc) {
        errors.push("Description is required.");
    } else if (desc.length > DESC_MAX) {
        errors.push(`Description must be at most ${DESC_MAX} characters.`);
    }

    if (!date) {
        errors.push("Due date is required.");
    } else if (!isTodayOrFuture(date)) {
        errors.push("Due date cannot be in the past.");
    }

    if (errors.length > 0) {
        alert(errors.join("\n"));
        return false;
    }
    return true;
}

// Trim text to a max length, optionally warning the user
function enforceMaxLength(text, max, fieldLabel) {
    if (text.length <= max) return text;
    alert(`${fieldLabel} cannot exceed ${max} characters. Extra characters were removed.`);
    return text.slice(0, max);
}

// ---------- Add Task ----------

$("#addTaskBtn").on("click", function () {
    let name = $("#taskName").val().trim();
    let desc = $("#taskDesc").val().trim();
    let date = $("#taskDate").val();

    // Use the validation helper instead of just "all fields required"
    if (!validateNewTask(name, desc, date)) {
        return;
    }

    tasks.push({
        name,
        desc,
        date,
        status: "pending"
    });

    saveTasks();
    showTasks();
    $("#taskName, #taskDesc, #taskDate").val("");
    setDateMinToday(); // ensure min stays correct if date resets
});

// ---------- Show Tasks in Table ----------

function showTasks() {
    $("#taskTable").empty();

    let filtered = tasks.filter(t => {
        if (filterMode === "all") return true;
        return t.status === filterMode;
    });

    filtered.forEach((task, index) => {
        $("#taskTable").append(`
            <tr>
                <td contenteditable="true" class="editName">${task.name}</td>
                <td contenteditable="true" class="editDesc">${task.desc}</td>
                <td contenteditable="true" class="editDate">${task.date}</td>
                <td class="text-${task.status === "completed" ? "success" : "warning"}">
                    ${task.status}
                </td>
                <td>
                    <button class="btn btn-success completeBtn" data-i="${index}">Complete</button>
                    <button class="btn btn-danger deleteBtn" data-i="${index}">Delete</button>
                </td>
            </tr>
        `);
    });

    updateSummary();
}

// ---------- Save to localStorage ----------

function saveTasks() {
    localStorage.setItem("mirageTasks", JSON.stringify(tasks));
}

// ---------- Mark Complete ----------

$(document).on("click", ".completeBtn", function () {
    let i = $(this).data("i");
    tasks[i].status = "completed";
    saveTasks();
    showTasks();
});

// ---------- Delete Task ----------

$(document).on("click", ".deleteBtn", function () {
    let i = $(this).data("i");
    tasks.splice(i, 1);
    saveTasks();
    showTasks();
});

// ---------- Inline Editing ----------

$(document).on("blur", ".editName, .editDesc, .editDate", function () {
    const $row = $(this).closest("tr");
    const rowIndex = $row.index();

    // Read edited values from the row
    let newName = $row.find(".editName").text().trim();
    let newDesc = $row.find(".editDesc").text().trim();
    let newDate = $row.find(".editDate").text().trim();

    // Enforce max lengths on inline edit
    newName = enforceMaxLength(newName, TITLE_MAX, "Title");
    newDesc = enforceMaxLength(newDesc, DESC_MAX, "Description");

    // If date is invalid or in the past, revert to previous stored date
    if (!isTodayOrFuture(newDate)) {
        alert("Due date cannot be set to a past date. Reverting to previous value.");
        newDate = tasks[rowIndex].date;
    }

    // Update cell texts in case we trimmed or reverted
    $row.find(".editName").text(newName);
    $row.find(".editDesc").text(newDesc);
    $row.find(".editDate").text(newDate);

    // Save back into the tasks array
    tasks[rowIndex].name = newName;
    tasks[rowIndex].desc = newDesc;
    tasks[rowIndex].date = newDate;

    saveTasks();
});

// ---------- Filtering ----------

$(".filterBtn").on("click", function () {
    filterMode = $(this).data("filter");
    showTasks();
});

// ---------- Sorting ----------

$(".sortBtn").on("click", function () {
    let mode = $(this).data("sort");

    if (mode === "name") {
        tasks.sort((a, b) => a.name.localeCompare(b.name));
    } else if (mode === "date") {
        tasks.sort((a, b) => new Date(a.date) - new Date(b.date));
    }

    saveTasks();
    showTasks();
});

// ---------- Summary stats ----------

function updateSummary() {
    let total = tasks.length;
    let pending = tasks.filter(t => t.status === "pending").length;
    let completed = tasks.filter(t => t.status === "completed").length;

    $("#totalTasks").text(total);
    $("#pendingTasks").text(pending);
    $("#completedTasks").text(completed);
}



// Set min date and show existing tasks on page load
setDateMinToday();
showTasks();
