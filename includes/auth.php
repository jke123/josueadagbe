<?php
require_once 'db.php';

function login($username, $password) {
    $db = getDB();
    $stmt = $db->prepare("SELECT * FROM admins WHERE username = ?");
    $stmt->execute([$username]);
    $user = $stmt->fetch();
    
    if ($user && password_verify($password, $user['password'])) {
        $_SESSION['admin_id'] = $user['id'];
        $_SESSION['admin_username'] = $user['username'];
        return true;
    }
    return false;
}

function isLoggedIn() {
    return isset($_SESSION['admin_id']);
}

function logout() {
    session_destroy();
}

function requireLogin() {
    if (!isLoggedIn()) {
        redirect('login.php');
    }
}
?>