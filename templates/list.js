    // Fetch players from the server
    function fetchPlayers() {
        fetch('/players')
          .then(response => response.json())
          .then(players => {
            const playerTable = document.getElementById('player-table');
            const tbody = playerTable.getElementsByTagName('tbody')[0];
            tbody.innerHTML = ''; // Clear existing rows
  
            players.forEach(player => {
              const row = document.createElement('tr');
              row.innerHTML = `
                <td>${player.username}</td>
                <td>${player.password}</td>
                <td>
                  <button onclick="editPlayer(${player.id})">Edit</button>
                  <button onclick="deletePlayer(${player.id})">Delete</button>
                </td>
              `;
              tbody.appendChild(row);
            });
          });
      }
  
      // Edit player
      function editPlayer(playerId) {
          var username = document.getElementById("username").value;
          var password = document.getElementById("password").value;
          var data = { "username": username, "password": password };
    
          fetch(`/players/${playerId}`, {
          method: 'PUT',
          body: JSON.stringify(data),
          headers:{
              'Content-Type': 'application/json'
          }
          }).then(response => response.text())
          .then(text => {
              if (text === "SUCCESS") {
                  location.reload();
                  console.log(`Player with ID ${playerId} edited successfully`);          
              } 
          })
      }
  
      // Delete player
      function deletePlayer(playerId) {
          fetch(`/players/${playerId}`, {
          method: 'DELETE'
          })
          .then(response => response.text())
          .then(text => {
              if (text === "SUCCESS") {
                  location.reload();
                  console.log(`Player with ID ${playerId} deleted succesfully`);
              } 
          })
      }

      // Create player
      function create_player(){
        var username = document.getElementById("username").value;
        var password = document.getElementById("password").value;
        var data = { "username": username, "password": password };
  
        fetch(`/players`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers:{
            'Content-Type': 'application/json'
        }
        }).then(response => response.text())
        .then(text => {
            if (text === "SUCCESS") {
                location.reload();
                console.log(`Player ${username} added successfully`);          
            } 
        })
    }
  
      // Initial fetch of players
      fetchPlayers();