<?php
require_once '../includes/config.php';
require_once '../includes/functions.php';

$hero = getHero();
$projects = getProjects(6);
$services = getServices();
$skills = getSkills();
$experiences = getExperiences();
$contact = getContact();
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mon Portfolio</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="container">
            <a href="#" class="logo">Portfolio</a>
            <ul class="nav-links">
                <li><a href="#hero">Accueil</a></li>
                <li><a href="#projects">Projets</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#skills">Compétences</a></li>
                <li><a href="#experience">Expérience</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="hero" class="hero" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="container">
            <div class="hero-content">
                <h1><?= $hero['title'] ?? 'Bienvenue' ?></h1>
                <p class="subtitle"><?= $hero['subtitle'] ?? '' ?></p>
                <p class="description"><?= $hero['description'] ?? '' ?></p>
                <a href="#contact" class="btn btn-primary">Contactez-moi</a>
            </div>
        </div>
    </section>

    <!-- Projects -->
    <section id="projects" class="section">
        <div class="container">
            <h2>Mes Projets</h2>
            <div class="projects-grid">
                <?php foreach ($projects as $project): ?>
                <div class="project-card">
                    <?php if ($project['image']): ?>
                    <img src="uploads/<?= $project['image'] ?>" alt="<?= $project['title'] ?>">
                    <?php endif; ?>
                    <h3><?= $project['title'] ?></h3>
                    <p><?= $project['description'] ?></p>
                    <div class="project-links">
                        <?php if ($project['demo_url']): ?>
                        <a href="<?= $project['demo_url'] ?>" target="_blank">Voir le projet</a>
                        <?php endif; ?>
                        <?php if ($project['code_url']): ?>
                        <a href="<?= $project['code_url'] ?>" target="_blank">Code source</a>
                        <?php endif; ?>
                    </div>
                    <?php if ($project['technologies']): ?>
                    <div class="tech-tags">
                        <?php foreach (explode(',', $project['technologies']) as $tech): ?>
                        <span><?= trim($tech) ?></span>
                        <?php endforeach; ?>
                    </div>
                    <?php endif; ?>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </section>

    <!-- Services -->
    <section id="services" class="section bg-light">
        <div class="container">
            <h2>Mes Services</h2>
            <div class="services-grid">
                <?php foreach ($services as $service): ?>
                <div class="service-card">
                    <div class="service-icon"><?= $service['icon'] ?? '🚀' ?></div>
                    <h3><?= $service['title'] ?></h3>
                    <p><?= $service['description'] ?></p>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </section>

    <!-- Skills -->
    <section id="skills" class="section">
        <div class="container">
            <h2>Compétences</h2>
            <div class="skills-grid">
                <?php 
                $skillsByCategory = [];
                foreach ($skills as $skill) {
                    $skillsByCategory[$skill['category']][] = $skill;
                }
                foreach ($skillsByCategory as $category => $skills): 
                ?>
                <div class="skill-category">
                    <h3><?= $category ?></h3>
                    <?php foreach ($skills as $skill): ?>
                    <div class="skill-item">
                        <span><?= $skill['name'] ?></span>
                        <div class="skill-bar">
                            <div class="skill-level" style="width: <?= $skill['level'] ?>%;"></div>
                        </div>
                    </div>
                    <?php endforeach; ?>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </section>

    <!-- Experience -->
    <section id="experience" class="section bg-light">
        <div class="container">
            <h2>Expérience</h2>
            <div class="timeline">
                <?php foreach ($experiences as $exp): ?>
                <div class="timeline-item">
                    <div class="timeline-date">
                        <?= date('M Y', strtotime($exp['start_date'])) ?>
                        <?php if ($exp['current']): ?>
                        - Présent
                        <?php else: ?>
                        - <?= date('M Y', strtotime($exp['end_date'])) ?>
                        <?php endif; ?>
                    </div>
                    <div class="timeline-content">
                        <h3><?= $exp['title'] ?></h3>
                        <h4><?= $exp['company'] ?></h4>
                        <p><?= $exp['description'] ?></p>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </section>

    <!-- Contact -->
    <section id="contact" class="section">
        <div class="container">
            <h2>Contact</h2>
            <div class="contact-wrapper">
                <div class="contact-info">
                    <?php if ($contact): ?>
                    <p>Email: <?= $contact['email'] ?></p>
                    <p>Téléphone: <?= $contact['phone'] ?></p>
                    <p>Adresse: <?= $contact['address'] ?></p>
                    <div class="social-links">
                        <?php if ($contact['linkedin']): ?>
                        <a href="<?= $contact['linkedin'] ?>">LinkedIn</a>
                        <?php endif; ?>
                        <?php if ($contact['github']): ?>
                        <a href="<?= $contact['github'] ?>">GitHub</a>
                        <?php endif; ?>
                    </div>
                    <?php endif; ?>
                </div>
                <form action="send_message.php" method="POST" class="contact-form">
                    <input type="text" name="name" placeholder="Nom" required>
                    <input type="email" name="email" placeholder="Email" required>
                    <input type="text" name="subject" placeholder="Sujet">
                    <textarea name="message" placeholder="Message" required></textarea>
                    <button type="submit" class="btn btn-primary">Envoyer</button>
                </form>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; <?= date('Y') ?> Mon Portfolio. Tous droits réservés.</p>
        </div>
    </footer>

    <script src="assets/js/main.js"></script>
</body>
</html>