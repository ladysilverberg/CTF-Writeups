## WEB550 - Included

By clicking the menu link, we get a route https://71fb1303c76a0ab6cc6890256c1e743e.challenge.hackazon.org/index.php?page=menu. From previous tasks, we know that there's an LFI vulnerability here, but it appends ".php".

We tried using some PHP filters and other things, but didn't find an immediate way to get the LFI to give us the source code of arbitrary routes.