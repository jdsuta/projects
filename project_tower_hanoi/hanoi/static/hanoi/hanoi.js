// main.js

let rods = { A: [], B: [], C: [] };
let numDisks = 0;
let steps = [];
let manualMoves = [];

function setupAndSolve(mode) {
    numDisks = document.getElementById('num_disks').value;
    if (numDisks < 1) {
        alert('Number of disks must be greater than 0');
        return;
    }
    reset();
    rods = { A: [], B: [], C: [] };
    for (let i = numDisks; i >= 1; i--) {
        rods.A.push(i);
    }
    render();

    if (mode === 'auto') {
        solve();
    }
}

function reset() {
    const puzzle = document.getElementById('puzzle');
    puzzle.innerHTML = `
        <div id="rodA" class="rod"></div>
        <div id="rodB" class="rod"></div>
        <div id="rodC" class="rod"></div>
    `;
    document.getElementById('solution').innerText = '';
    rods = { A: [], B: [], C: [] };
    manualMoves = [];
}

function solve() {
    fetch('/hanoi/solve/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ num_disks: numDisks })
    })
    .then(response => response.json())
    .then(data => {
        if (data.solution) {
            document.getElementById('solution').innerText = data.solution.join('\n');
            steps = data.solution;
            animate();
        } else {
            document.getElementById('solution').innerText = 'Error solving puzzle';
        }
    });
}

function render() {
    const puzzle = document.getElementById('puzzle');
    puzzle.innerHTML = '';
    for (let rod in rods) {
        const rodDiv = document.createElement('div');
        rodDiv.className = 'rod';
        rodDiv.id = `rod${rod}`;
        rodDiv.innerHTML = `<strong>${rod}:</strong> `;
        rodDiv.ondragover = (event) => event.preventDefault();
        rodDiv.ondrop = (event) => {
            event.preventDefault();
            const diskId = event.dataTransfer.getData("text");
            const disk = document.getElementById(diskId);
            const fromRod = disk.parentNode.id.replace('rod', '');
            const toRod = rod;

            // Check if the disk being moved is the top disk on its rod
            if (rods[fromRod].length === 0 || disk.innerText != rods[fromRod][rods[fromRod].length - 1].toString()) {
                alert('Invalid move! You can only move the top disk.');
                return;
            }

            if (canMoveDisk(fromRod, toRod)) {
                moveDisk(fromRod, toRod);
                manualMoves.push(`Move disk ${disk.innerText} from ${fromRod} to ${toRod}`);
                document.getElementById('solution').innerText = manualMoves.join('\n');
                render();
                if (rods.C.length === numDisks) {
                    document.getElementById('solution').innerText += '\nYou have done it!';
                }
            } else {
                alert('Invalid move! You cannot place a larger disk on a smaller disk.');
            }
        };
        rods[rod].forEach(disk => {
            const diskDiv = document.createElement('div');
            diskDiv.className = 'disk';
            diskDiv.style.width = (disk * 12) + 'px';
            diskDiv.innerText = disk;
            diskDiv.draggable = true;
            diskDiv.id = `disk${disk}`;
            diskDiv.ondragstart = (event) => {
                event.dataTransfer.setData("text", event.target.id);
            };
            rodDiv.appendChild(diskDiv);
        });
        puzzle.appendChild(rodDiv);
    }
}

function moveDisk(from, to) {
    if (rods[from].length === 0) return;
    const disk = rods[from].pop();
    rods[to].push(disk);
}

function canMoveDisk(from, to) {
    if (rods[to].length === 0) return true;
    return rods[to][rods[to].length - 1] > rods[from][rods[from].length - 1];
}

function animate() {
    let stepIndex = 0;

    function step() {
        if (stepIndex < steps.length) {
            const [_, disk, from, to] = steps[stepIndex].match(/Move disk (\d+) from (.) to (.)/);
            moveDisk(from, to);
            render();
            stepIndex++;
            setTimeout(step, 500);
        }
    }

    step();
}
