<?php
// Configuration
define('DB_HOST', 'localhost');
define('DB_NAME', 'portfolio_db');
define('DB_USER', 'root');
define('DB_PASS', '');

define('SITE_URL', 'http://localhost/portfolio/');
define('ADMIN_URL', SITE_URL . 'admin/');
define('UPLOAD_DIR', __DIR__ . '/../public/uploads/');

// Session
session_start();

// Timezone
date_default_timezone_set('Europe/Paris');

// Error reporting (à désactiver en production)
error_reporting(E_ALL);
ini_set('display_errors', 1);
?>