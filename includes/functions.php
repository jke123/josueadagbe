<?php
require_once 'db.php';

// Upload de fichier
function uploadFile($file, $targetDir) {
    if (!file_exists($targetDir)) {
        mkdir($targetDir, 0777, true);
    }
    
    $fileName = time() . '_' . basename($file['name']);
    $targetFile = $targetDir . $fileName;
    $imageFileType = strtolower(pathinfo($targetFile, PATHINFO_EXTENSION));
    
    $allowedTypes = ['jpg', 'jpeg', 'png', 'gif', 'webp'];
    if (!in_array($imageFileType, $allowedTypes)) {
        return false;
    }
    
    if ($file['size'] > 5000000) {
        return false;
    }
    
    if (move_uploaded_file($file['tmp_name'], $targetFile)) {
        return $fileName;
    }
    
    return false;
}

// Sécuriser les inputs
function sanitize($input) {
    return htmlspecialchars(strip_tags(trim($input)));
}

// Redirection
function redirect($url) {
    header("Location: $url");
    exit();
}

// Message flash
function setFlash($type, $message) {
    $_SESSION['flash'] = ['type' => $type, 'message' => $message];
}

function getFlash() {
    if (isset($_SESSION['flash'])) {
        $flash = $_SESSION['flash'];
        unset($_SESSION['flash']);
        return $flash;
    }
    return null;
}

// Récupérer les données
function getHero() {
    $db = getDB();
    $stmt = $db->query("SELECT * FROM hero LIMIT 1");
    return $stmt->fetch();
}

function getProjects($limit = null) {
    $db = getDB();
    $sql = "SELECT * FROM projects ORDER BY created_at DESC";
    if ($limit) {
        $sql .= " LIMIT $limit";
    }
    $stmt = $db->query($sql);
    return $stmt->fetchAll();
}

function getServices() {
    $db = getDB();
    $stmt = $db->query("SELECT * FROM services ORDER BY created_at");
    return $stmt->fetchAll();
}

function getSkills() {
    $db = getDB();
    $stmt = $db->query("SELECT * FROM skills ORDER BY category, level DESC");
    return $stmt->fetchAll();
}

function getExperiences() {
    $db = getDB();
    $stmt = $db->query("SELECT * FROM experiences ORDER BY start_date DESC");
    return $stmt->fetchAll();
}

function getContact() {
    $db = getDB();
    $stmt = $db->query("SELECT * FROM contact LIMIT 1");
    return $stmt->fetch();
}
?>