
import './App.css';
import React, { useState, useEffect } from 'react';

function App() {

  //state for the list of characters
  const [characters, setCharacters] = useState([]);

  //state for the current pair of characters to vote on
  const [characterPair, setCharacterPair] = useState([]);


  useEffect(() => {

    fetchCharacterPair();

    // Fetch data from Flask API
    fetch('/api/characters') // Adjust the endpoint if i need to
      .then(response => response.json())
      .then(data => {
        setCharacters(data);
      })
      .catch(error => console.error('Error:', error));
  }, []);

  const fetchCharacterPair = () => {

    fetch('/api/character-pair') // Adjust the endpoint 
      .then(response => response.json())
      .then(data => { setCharacterPair(data); })
      .catch(error => console.error('Error fetching character pair:', error));
  };

  const handleVote = (winner, loser) => {
    fetch('/update_elo', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ winner, loser })
    })
      .then(response => response.json())
      .then(data => {
        // After a vote, refresh character pair and rankings
        fetchCharacterPair();
        // Fetch character rankings to update the table
        fetch('/api/characters')
          .then(response => response.json())
          .then(data => setCharacters(data));
      })
      .catch(error => console.error('Error:', error));
  };


  return (

    <div>
      <h1>Star Wars Character Competition</h1>
      <h2>Vote Your Favourite of the Two Below!</h2>


      <div>
        {characterPair.map((character, index) => (
          <button key={index} onClick={() => handleVote(character.name, characterPair[1 - index].name)}>
            {character.name}
          </button>
        ))}
      </div>

      <h2>Characters Ranked By ELO!</h2>

      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>ELO</th>
          </tr>
        </thead>
        <tbody>
          {characters.map((character, index) => {


            const isHighlighted = characterPair.some(pair => pair.name === character.name);
            return (
              <tr key={index} className={isHighlighted ? 'highlighted-row' : ''}>
                <td>{index + 1}</td>
                <td>{character.name}</td>
                <td>{character.elo}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>


  );
}

export default App;
