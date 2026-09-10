<?php
require_once '../includes/config.php';
require_once '../includes/functions.php';
require_once '../includes/auth.php';
requireLogin();
include 'includes/header.php';
?>

<div class="dashboard">
    <h1>Tableau de bord</h1>
    
    <div class="stats-grid">
        <div class="stat-card">
            <h3>Projets</h3>
            <p class="number"><?= count(getProjects()) ?></p>
        </div>
        <div class="stat-card">
            <h3>Services</h3>
            <p class="number"><?= count(getServices()) ?></p>
        </div>
        <div class="stat-card">
            <h3>Compétences</h3>
            <p class="number"><?= count(getSkills()) ?></p>
        </div>
        <div class="stat-card">
            <h3>Messages</h3>
            <p class="number">0</p>
        </div>
    </div>
</div>

<?php include 'includes/footer.php'; ?>