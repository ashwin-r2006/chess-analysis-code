const form = document.getElementById("fenForm");
const output = document.getElementById("output");
const lichessBtn = document.getElementById("lichessBtn");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        move: document.getElementById("move").value,
        kw: document.getElementById("kw").value,
        kb: document.getElementById("kb").value,
        qw: document.getElementById("qw").value,
        qb: document.getElementById("qb").value,
        bw: document.getElementById("bw").value,
        bb: document.getElementById("bb").value,
        nw: document.getElementById("nw").value,
        nb: document.getElementById("nb").value,
        rw: document.getElementById("rw").value,
        rb: document.getElementById("rb").value,
        pw: document.getElementById("pw").value,
        pb: document.getElementById("pb").value,
        castle: {
            K: document.getElementById("K").checked,
            Q: document.getElementById("Q").checked,
            k: document.getElementById("k").checked,
            q: document.getElementById("q").checked
        }
    };

    const response = await fetch("https://YOUR_BACKEND_URL/generate_fen", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    output.value = result.fen;

    lichessBtn.disabled = false;
    lichessBtn.onclick = () => {
        window.open(result.lichess_url, "_blank");
    };
});
