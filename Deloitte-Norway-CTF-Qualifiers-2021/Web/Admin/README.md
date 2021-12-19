## WEB550 - Admin

By clicking the contact link, we get access to a live chat. By playing around a bit and looking at the javascript code, this takes the input, encodes it in a parameter called msg and sends a POST request to https://71fb1303c76a0ab6cc6890256c1e743e.challenge.hackazon.org/chat/. The response is then printed back in the live chat window.

By playing a bit around with the input, we found that we could provide URLs within the domain of https://71fb1303c76a0ab6cc6890256c1e743e.challenge.hackazon.org, and the server would then visit the site and seemingly post some carefully chosen HTML from the site back. By providing https://71fb1303c76a0ab6cc6890256c1e743e.challenge.hackazon.org/admin/ as input, we would get the reply "Welcome, Admin", and visiting https://71fb1303c76a0ab6cc6890256c1e743e.challenge.hackazon.org/pma/ yielded "PhpMiniAdmin | Logout |.

If we visit https://71fb1303c76a0ab6cc6890256c1e743e.challenge.hackazon.org/admin/, we get a message telling us that we don't have the correct cookie set. In order to solve this, we would need a way to provide some carefully chosen URL or input to the live chat which would leak the cookies of the server so we could access the whole /admin route.

Some likely vectors we did not have time to fully explore here includes XSS and CSRF. There may have been some way to utilize the LFI vulnerability to leak the source code of more parts of the site as well which could have provided valuable information, or there may have been some pointers hidden in the /dav route which returned a 403 - Forbidden.