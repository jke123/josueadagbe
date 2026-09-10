<?php
define('DB_HOST', getenv('MYSQLHOST')     ?: getenv('DB_HOST') ?: 'localhost');
define('DB_PORT', getenv('MYSQLPORT')     ?: getenv('DB_PORT') ?: '3306');
define('DB_NAME', getenv('MYSQLDATABASE') ?: getenv('DB_NAME') ?: 'portfolio_db');
define('DB_USER', getenv('MYSQLUSER')     ?: getenv('DB_USER') ?: 'root');
define('DB_PASS', getenv('MYSQLPASSWORD') ?: getenv('DB_PASS') ?: '');

$host = getenv('RENDER_EXTERNAL_HOSTNAME') ?: ($_SERVER['HTTP_HOST'] ?? 'localhost');
$protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
define('SITE_URL', $protocol . '://' . $host . '/');
define('ADMIN_URL', SITE_URL . 'admin/');
define('UPLOAD_DIR', __DIR__ . '/../public/uploads/');

session_start();
date_default_timezone_set('Europe/Paris');
error_reporting(E_ALL);
ini_set('display_errors', 1);