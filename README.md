# RMT_Four_in_a_row
Console representation of known multiplayer game [Connect Four](https://en.wikipedia.org/wiki/Connect_Four), done within project at the faculty. 

## Description
<ul>
<li> This is "Connect four" game for two players. </li>
<li> Architecture is client-server. </li>
<li> Application is implemented in Python. </li>
</ul>

## How to play
In this game first player uses the mark "X", whereas second uses "O". The game is played on 7x6 field vertical grid and players take turns choosing the right column in order to connect four pieces of their mark. First player to connect them horizontally, vertically, or diagonally wins the game.

## How to run the game
You can either play version with server and two client programs or an "offline" version with one interface. 

### Client-server version
Firstly, server needs to be up and running. Within project directory type: `python GameServer.py` <br/> Secondly, for starting client process type: `python Client.py` <br/><br/> Minimum game requirements are running server and at least two connected clients. 

### Offline version
In this version both players play the game in the same console. For starting type: `python FunctionalOfflineGame.py`

### Enjoy!
