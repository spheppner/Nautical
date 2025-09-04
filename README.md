# Nautical

---

## WORK IN PROGRESS

I am reviving this game as a hobby next to many other things.

---

A 2-4 player LAN game of turn-based naval strategy and real-time artillery skill. Hunt for your friends' fleets across a vast, procedurally-generated archipelago, and engage in explosive, physics-based combat where you can destroy the very islands you fight over.

## How to Play

1.  **Launch the Game:** Run `main.py` with Python and Pygame installed.
2.  **Host a Game:** One player selects "Host Game". They will enter the Lobby and can share their local IP address with friends.
3.  **Join a Game:** Other players select "Join Game" and enter the host's local IP address.
4.  **Start:** Once all players are visible in the lobby, the host can click "Start Game".
5.  **Strategy Phase:**
    * **Select a ship:** Left-click on one of your ships.
    * **Set a destination:** Right-click anywhere on the map to set a waypoint. The ship will travel towards this point over subsequent turns.
    * **Finalize your moves:** Click "Submit Turn" to send your commands to the server and end your turn.

## Features

* **LAN Multiplayer:** Play with up to 4 friends on the same local network.
* **Procedurally Generated Maps:** Never play on the same map twice thanks to a Perlin noise-based world generator.
* **Simultaneous Turn-Based Strategy:** Plan your moves in secret, then watch as everyone's actions unfold at once.
* **Fog of War:** Hunt for your opponents, using scout ships to reveal the map and track enemy movements.
* **Real-Time Combat (Work in Progress):** The framework is in place to engage in skill-based artillery duels.
* **Destructible Terrain (Work in Progress):** The mechanics for reshaping the battlefield with powerful cannon fire are being developed.

## Credits and Origins

This project is a revival and reimagining of the original idea from 2020.

Original Contributor: **Horst Jens** ([github.com/horstjens/](https://github.com/horstjens/)) with whom I thought out the initial concept in 2020.