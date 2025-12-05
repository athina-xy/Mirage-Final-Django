
function getStoredTasks() {
    const possibleKeys = ["mirageTasks", "tasks", "taskList"];

    for (const key of possibleKeys) {
        const raw = localStorage.getItem(key);
        if (raw) {
            try {
                const parsed = JSON.parse(raw);
                if (Array.isArray(parsed)) {
                    return parsed;
                }
            } catch (e) {
                console.error("Error parsing tasks from key:", key, e);
            }
        }
    }
    return [];
}

// Returns both the array and counts
function getTaskStats() {
    const tasks = getStoredTasks();
    const completed = tasks.filter(t => t.status === "completed" || t.completed === true).length;
    const total = tasks.length;
    const pending = total - completed;
    return { tasks, total, pending, completed };
}

function renderLatestActivity() {
    const { tasks, total, pending, completed } = getTaskStats();
    const $box = $("#latest-activity");

    if (!tasks.length) {
        $box.html(
            `<p class="mb-0 text-center">
                <em>No Tasks added yet.</em>
             </p>`
        );
        return;
    }

    // Sort by lastUpdated / dueDate / createdAt if available (newest first)
    const sorted = [...tasks].sort((a, b) => {
        const da = new Date(a.lastUpdated || a.date || a.dueDate || a.createdAt || 0);
        const db = new Date(b.lastUpdated || b.date || b.dueDate || b.createdAt || 0);
        return db - da;
    });

    const recent = sorted.slice(0, 3);

    let items = recent.map(t => {
        const name = t.name || t.title || "Unnamed task";
        const isDone = t.status === "completed" || t.completed === true;
        const statusLabel = isDone ? "Completed" : "Pending";
        const statusClass = isDone ? "text-success" : "text-warning";

        return `
            <li class="mb-1">
                <strong>${name}</strong>
                <span class="${statusClass} ms-1">(${statusLabel})</span>
            </li>
        `;
    }).join("");

    if (!items) {
        items = `<li>No recent events.</li>`;
    }

    $box.html(`
        <p class="mb-2">
            <strong>Task Summary</strong><br>
            Total: ${total} • Pending: ${pending} • Completed: ${completed}
        </p>
        <ul class="mb-0 ps-3">
            ${items}
        </ul>
    `);
}


// Pie Chart 


let tasksChart = null;

function updateTasksChart() {
    const { pending, completed } = getTaskStats();
    const canvas = document.querySelector("#tasksChart");
    if (!canvas || typeof Chart === "undefined") return;

    const data = [pending, completed];

    if (!tasksChart) {
        const ctx = canvas.getContext("2d");
        tasksChart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: ["Pending", "Completed"],
                datasets: [{
                    data: data,
                    backgroundColor: [
                        "rgba(255, 206, 86, 0.8)",   // Pending
                        "rgba(75, 192, 192, 0.8)"   // Completed
                    ],
                    borderColor: [
                        "rgba(255, 206, 86, 1)",
                        "rgba(75, 192, 192, 1)"
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            color: "#f5f5f5"
                        }
                    }
                }
            }
        });
    } else {
        tasksChart.data.datasets[0].data = data;
        tasksChart.update();
    }
}


// API
function setQuoteLoading() {
    $("#quote-text").html(
        `<em>Tuning into the Crystal Archives...</em>`
    );
}

function setQuote(text, author) {
    const safeText = text || "The realms speak in whispers only the brave can hear.";
    const safeAuthor = author ? `— ${author}` : "";

    $("#quote-text").html(`
        "${safeText}"<br><span class="d-block mt-1" style="font-size:0.85rem;">${safeAuthor}</span>
    `);
}

// Uses AdviceSlip API 
function fetchQuote() {
    setQuoteLoading();

    fetch("https://api.adviceslip.com/advice")
        .then(resp => {
            if (!resp.ok) throw new Error("Network response was not ok");
            return resp.json();
        })
        .then(data => {
            const text = data && data.slip && data.slip.advice
                ? data.slip.advice
                : "Sometimes the clearest path appears only after you take the first step.";

            const author = "Aetherstone";
            setQuote(text, author);
        })
        .catch(err => {
            console.error("Quote fetch error:", err);

            const fallbackQuotes = [
                {
                    text: "In a world of fractured mirrors, every shard hides a possible you.",
                    author: "Luminite"
                },
                {
                    text: "Not all exiles are lost; some are simply ahead of their time.",
                    author: "Prismheart"
                },
                {
                    text: "Balance is not the absence of chaos, but learning to dance with it.",
                    author: "Sylwen"
                }
            ];
            const random = fallbackQuotes[Math.floor(Math.random() * fallbackQuotes.length)];
            setQuote(random.text, random.author || "Caelcryst");
        });
}


$(function () {
    // Reveal section when button clicked
    $("#enterRealmBtn").on("click", function () {
        const $section = $("#revealContent");

        $section.slideDown(600, function () {
            // After reveal, load API + activity + chart
            fetchQuote();
            renderLatestActivity();
            updateTasksChart();

            // Smooth scroll animation 
            $("html, body").animate(
                { scrollTop: $section.offset().top - 20 },
                600
            );
        });
    });

    // Refresh quote button
    $("#new-quote").on("click", function () {
        fetchQuote();
    });
});
