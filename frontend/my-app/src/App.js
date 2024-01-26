
import './App.css';
import React, { useState, useEffect } from 'react';
import { FaArrowUp, FaArrowDown } from 'react-icons/fa';

function App() {

  //state for the list of characters
  const [characters, setCharacters] = useState([]);

  //state for the current pair of characters to vote on
  const [characterPair, setCharacterPair] = useState([]);




  useEffect(() => {



    // Fetch data from Flask API
    fetch('/api/characters')
      .then(response => response.json())
      .then(data => {
        const initialDataWithRanks = data.map((character, index) => ({
          ...character,
          previousRank: index + 1,  // Store initial rank
          rankChange: 'none'        // Initial rank change is none
        }));
        setCharacters(initialDataWithRanks);
      })
      .catch(error => console.error('Error:', error));

    fetchCharacterPair();
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
        console.log('ELO updated:', data);

        // Fetch character rankings to update the table
        fetch('/api/characters')
          .then(response => response.json())
          .then(updatedData => {

            const updatedCharactersWithRankChange = updatedData.map((character, index) => {
              const currentRank = index + 1;
              const previousCharacter = characters.find(c => c.name === character.name);

              // Determine the rank change
              let rankChange = 'none';
              if (previousCharacter) {
                if (previousCharacter.previousRank > currentRank) {
                  rankChange = 'up';
                } else if (previousCharacter.previousRank < currentRank) {
                  rankChange = 'down';
                }
              }

              return {
                ...character,
                previousRank: currentRank,  // Update previous rank
                rankChange                  // Set rank change
              };
            });

            setCharacters(updatedCharactersWithRankChange);

            // Fetch the updated character pair for voting
            fetchCharacterPair();
          })
          .catch(error => console.error('Error fetching updated character data:', error));
      })
      .catch(error => console.error('Error updating ELO:', error));
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
              <tr key={character.name} className={isHighlighted ? 'highlighted-row' : ''}>
                <td>
                  {index + 1}

                  {character.rankChange === 'up' && <FaArrowUp style={{ color: 'green' }} />}
                  {character.rankChange === 'down' && <FaArrowDown style={{ color: 'red' }} />}

                </td>
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
