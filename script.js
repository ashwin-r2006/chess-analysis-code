const form = document.getElementById("fenForm");
const output = document.getElementById("output");
const lichessBtn = document.getElementById("lichessBtn");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Show immediate feedback
    output.value = "Generating FEN, please wait...";
    lichessBtn.disabled = true;

    const data = {
        move: document.getElementById("move").value,
        kw: document.getElementById("kw").value.trim(),
        kb: document.getElementById("kb").value.trim(),
        qw: document.getElementById("qw").value.trim(),
        qb: document.getElementById("qb").value.trim(),
        bw: document.getElementById("bw").value.trim(),
        bb: document.getElementById("bb").value.trim(),
        nw: document.getElementById("nw").value.trim(),
        nb: document.getElementById("nb").value.trim(),
        rw: document.getElementById("rw").value.trim(),
        rb: document.getElementById("rb").value.trim(),
        pw: document.getElementById("pw").value.trim(),
        pb: document.getElementById("pb").value.trim(),
        castle: {
            K: document.getElementById("K").checked,
            Q: document.getElementById("Q").checked,
            k: document.getElementById("k").checked,
            q: document.getElementById("q").checked
        }
    };

    try {
        const response = await fetch(
            "https://chess-analysis-code.onrender.com/generate_fen",
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            }
        );

        const result = await response.json();

        // Handle backend error
        if (!response.ok || result.error) {
            output.value = "Error: " + (result.error || "Backend error");
            return;
        }

        // Success
        output.value = result.fen;

        lichessBtn.disabled = false;
        lichessBtn.onclick = () => {
            window.open(result.lichess_url, "_blank");
        };

    } catch (err) {
        output.value = "Error: Unable to reach backend server.";
    }
});
