// Fetch colors del servidor
// 1pt
function fetchColors() {
  fetch('/colors')
    .then((response) => response.json())
    .then((colors) => {
      const colorTable = document.getElementById('color-table');
      const tbody = colorTable.getElementsByTagName('tbody')[0];
      tbody.innerHTML = ''; // Limpia las filas existentes en la tabla

      colors.forEach((color) => {
        const row = document.createElement('tr');
        row.innerHTML = `
                <td>${color.R}</td>
                <td> #TODO </td>
                <td> #TODO </td>
                <td> #MOSTRAR COLOR </td>
                <td>
                  <button onclick="editColor(${color.id})">Edit</button>
                  <button> #TODO </button>
                </td>
              `;
        tbody.appendChild(row);
      });
    });
}

// Update color
// 1pt
function editColor(colorID) {
  var R = document.getElementById('R').value;
  // TODO

  var data = { R: R, ...'#TODO' }; // Complete data object

  fetch(`/colors/${colorID}`, {
    method: 'PUT',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.text())
    .then((text) => {
      if (text === 'SUCCESS') {
        location.reload(); // Recarga la página
        console.log(`Color with ID ${colorID} edited successfully`);
      }
    });
}

// Delete color
// 2pt
function deletePlayer(colorId) {
  //TODO
}

// Create color
// 2pt
function addColor() {
  //TODO
}

// Inicia cargando la página de colores existentes
fetchColors();
