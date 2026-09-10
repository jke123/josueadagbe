<?php
require_once '../includes/config.php';
require_once '../includes/functions.php';
require_once '../includes/auth.php';
requireLogin();

$db = getDB();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['action'])) {
        switch ($_POST['action']) {
            case 'add':
                $stmt = $db->prepare("INSERT INTO services (title, description, icon) VALUES (?, ?, ?)");
                $stmt->execute([
                    sanitize($_POST['title']),
                    sanitize($_POST['description']),
                    sanitize($_POST['icon'])
                ]);
                setFlash('success', 'Service ajouté');
                break;
                
            case 'edit':
                $stmt = $db->prepare("UPDATE services SET title=?, description=?, icon=? WHERE id=?");
                $stmt->execute([
                    sanitize($_POST['title']),
                    sanitize($_POST['description']),
                    sanitize($_POST['icon']),
                    $_POST['id']
                ]);
                setFlash('success', 'Service mis à jour');
                break;
                
            case 'delete':
                $stmt = $db->prepare("DELETE FROM services WHERE id=?");
                $stmt->execute([$_POST['id']]);
                setFlash('success', 'Service supprimé');
                break;
        }
        redirect('services.php');
    }
}

$services = getServices();
include 'includes/header.php';
?>

<div class="admin-content">
    <div class="admin-header">
        <h1>Gestion des Services</h1>
        <button onclick="openModal('addModal')" class="btn btn-primary">Ajouter un service</button>
    </div>
    
    <?php if ($flash = getFlash()): ?>
    <div class="alert alert-<?= $flash['type'] ?>"><?= $flash['message'] ?></div>
    <?php endif; ?>
    
    <table class="admin-table">
        <thead>
            <tr>
                <th>Icône</th>
                <th>Titre</th>
                <th>Description</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($services as $service): ?>
            <tr>
                <td><?= $service['icon'] ?></td>
                <td><?= $service['title'] ?></td>
                <td><?= substr($service['description'], 0, 50) ?>...</td>
                <td>
                    <button onclick="editService(<?= htmlspecialchars(json_encode($service)) ?>)" class="btn btn-sm btn-primary">Modifier</button>
                    <form method="POST" style="display:inline" onsubmit="return confirm('Supprimer ?')">
                        <input type="hidden" name="action" value="delete">
                        <input type="hidden" name="id" value="<?= $service['id'] ?>">
                        <button type="submit" class="btn btn-sm btn-danger">Supprimer</button>
                    </form>
                </td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</div>

<!-- Add/Edit Modals similaires à projects.php -->

<script>
function openModal(id) {
    document.getElementById(id).style.display = 'block';
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

function editService(service) {
    // Similaire à editProject
    document.getElementById('edit_id').value = service.id;
    document.getElementById('edit_title').value = service.title;
    document.getElementById('edit_description').value = service.description;
    document.getElementById('edit_icon').value = service.icon;
    openModal('editModal');
}
</script>

<?php include 'includes/footer.php'; ?>