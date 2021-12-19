## WEB550 - RCE

From previous tasks, we know that the source code of the index.php page is:

````
	dbConnect();
	$this->siteConfig();
	$this->render();
} 

function dbConnect() { 
	// connect to database $cfg = include("db.inc.php");
	$this->db = new PDO(
		$cfg['db_dsn'],
		$cfg['db_user'],
		$cfg['db_pass']
	);
	$this->db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
}

function siteConfig() { 
	// get site configuration
	$select = $this->db->query('SELECT k,v FROM config');
	foreach ($select->fetchAll() as $entry) { 
		extract($entry); 
		$GLOBALS[$k] = $$k = unserialize($v); 
	}
	
	// in maintenance? 
	if ($maintenance_mode) { 
		header("content-type: text/plain"); 
		print $maintenance_text; 
		exit; 
	} 
} 

function render() { 
	// load/parse page
	$page = (string) @$_GET['page'] ?: "home";
	include("pages/template_top.php");
	readfile("pages/${page}.php"); // <-- LFI
	readfile("pages/template_bottom.php");
}

function __destruct() {
	$this->db = null; 
	file_put_contents($this->logfile, $GLOBALS['log_visitor_entry']); 
}

} new Website;
````

From this code, we see some interesting things:
- We seem to have a Website class with a __destruct() function which has a call to file_put_contents.
- We have an LFI which can include php files in the render() function.
- In siteConfig(), some configuration entries from the database is iterated over, unserialized and put in an array called $GLOBALS.
- In siteConfig(), if $maintenance_mode is true and we can control $maintenance_text, we practically have the ability to print anything we want.

These things can be chained together into RCE. Since we already have access to the database, we can edit the config and thus unserialize whatever data we want. We want to set the entry where $k = 'log_visitor_entry' to have $v = [php command shell code]. This will make it so that if __destruct() gets called, a PHP shell will be put into a file with the filename $this->logfile contains.

Next, we want to create our own little snippet to create and serialize our own Website object:

````
class Website {
	public $db;
	public $logfile;

	function __construct() {
		$this->db = null;
		$this->logfile = 'pages/shell.php';
	}
}

echo serialize(new Website());
````

With the string this outputs, we can create a new entry in the config on the actual website. unserialize() will then unserialize a Website object where db = null and logfile = 'pages/shell.php'. The idea is then to force this object to destruct. Since $GLOBALS is a global variable and not a local variable of the class, the actual Website object will have set $GLOBALS['log_visitor_entry'] to be our PHP code. When our fake unserialized Website object is destroyed, we will therefore write this code into a file named 'pages/shell.php'.

Finally, once we have managed to do all of this we would simply include our shell.php by setting the page parameter in the URL to be shell. We now have RCE.
