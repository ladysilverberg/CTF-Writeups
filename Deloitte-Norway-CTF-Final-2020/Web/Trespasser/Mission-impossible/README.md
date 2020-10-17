## WEB600 - Trespasser (Mission Impossible)
We are presented a level which is essentially impossible to solve, due to there being too many blockades.
By looking in the game.js source file of the application in the developer console in the browser, we can see the code which loads the level.

However, we can intercept the request in burp and send it to repeater. Here we can change the parameters of the level to remove the blockades and set the rings and lasers so that we get an instant victory and the flag as a response.
