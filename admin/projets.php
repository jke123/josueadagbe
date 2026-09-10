<?php
require_once '../includes/config.php';
require_once '../includes/functions.php';
require_once '../includes/auth.php';
requireLogin();

$db = getDB();

// Traitement CRUD
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['action'])) {
        switch ($_POST['action']) {
            case 'add':
                $image = '';
                if (isset($_FILES['image']) && $_FILES['image']['error'] === 0) {
                    $image = uploadFile($_FILES['image'], UPLOAD_DIR . 'projects/');
                }
                
                $stmt = $db->prepare("INSERT INTO projects (title, description, image, demo_url, code_url, technologies) VALUES (?, ?, ?, ?, ?, ?)");
                $stmt->execute([
                    sanitize($_POST['title']),
                    sanitize($_POST['description']),
                    $image,
                    sanitize($_POST['demo_url']),
                    sanitize($_POST['code_url']),
                    sanitize($_POST['technologies'])
                ]);
                setFlash('success', 'Projet ajouté avec succès');
                break;
                
            case 'edit':
                $id = $_POST['id'];
                $image = $_POST['current_image'];
                if (isset($_FILES['image']) && $_FILES['image']['error'] === 0) {
                    $newImage = uploadFile($_FILES['image'], UPLOAD_DIR . 'projects/');
                    if ($newImage) {
                        $image = $newImage;
                    }
                }
                
                $stmt = $db->prepare("UPDATE projects SET title=?, description=?, image=?, demo_url=?, code_url=?, technologies=? WHERE id=?");
                $stmt->execute([
                    sanitize($_POST['title']),
                    sanitize($_POST['description']),
                    $image,
                    sanitize($_POST['demo_url']),
                    sanitize($_POST['code_url']),
                    sanitize($_POST['technologies']),
                    $id
                ]);
                setFlash('success', 'Projet mis à jour');
                break;
                
            case 'delete':
                $stmt = $db->prepare("DELETE FROM projects WHERE id=?");
                $stmt->execute([$_POST['id']]);
                setFlash('success', 'Projet supprimé');
                break;
        }
        redirect('projects.php');
    }
}

$projects = getProjects();
include 'includes/header.php';
?>

<div class="admin-content">
    <div class="admin-header">
        <h1>Gestion des Projets</h1>
        <button onclick="openModal('addModal')" class="btn btn-primary">Ajouter un projet</button>
    </div>
    
    <?php if ($flash = getFlash()): ?>
    <div class="alert alert-<?= $flash['type'] ?>"><?= $flash['message'] ?></div>
    <?php endif; ?>
    
    <table class="admin-table">
        <thead>
            <tr>
                <th>Image</th>
                <th>Titre</th>
                <th>Technologies</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($projects as $project): ?>
            <tr>
                <td>
                    <?php if ($project['image']): ?>
                    <img src="../public/uploads/projects/<?= $project['image'] ?>" width="50">
                    <?php endif; ?>
                </td>
                <td><?= $project['title'] ?></td>
                <td><?= $project['technologies'] ?></td>
                <td>
                    <button onclick="editProject(<?= htmlspecialchars(json_encode($project)) ?>)" class="btn btn-sm btn-primary">Modifier</button>
                    <form method="POST" style="display:inline" onsubmit="return confirm('Supprimer ?')">
                        <input type="hidden" name="action" value="delete">
                        <input type="hidden" name="id" value="<?= $project['id'] ?>">
                        <button type="submit" class="btn btn-sm btn-danger">Supprimer</button>
                    </form>
                </td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</div>

<!-- Modals -->
<!-- Add Modal -->
<div id="addModal" class="modal">
    <div class="modal-content">
        <span class="close" onclick="closeModal('addModal')">&times;</span>
        <h2>Ajouter un projet</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="hidden" name="action" value="add">
            
            <div class="form-group">
                <label>Titre</label>
                <input type="text" name="title" required>
            </div>
            
            <div class="form-group">
                <label>Description</label>
                <textarea name="description" rows="4"></textarea>
            </div>
            
            <div class="form-group">
                <label>Image</label>
                <input type="file" name="image" accept="image/*">
            </div>
            
            <div class="form-group">
                <label>Lien Demo</label>
                <input type="url" name="demo_url">
            </div>
            
            <div class="form-group">
                <label>Lien Code</label>
                <input type="url" name="code_url">
            </div>
            
            <div class="form-group">
                <label>Technologies (séparées par des virgules)</label>
                <input type="text" name="technologies">
            </div>
            
            <button type="submit" class="btn btn-primary">Enregistrer</button>
        </form>
    </div>
</div>

<!-- Edit Modal -->
<div id="editModal" class="modal">
    <div class="modal-content">
        <span class="close" onclick="closeModal('editModal')">&times;</span>
        <h2>Modifier le projet</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="hidden" name="action" value="edit">
            <input type="hidden" name="id" id="edit_id">
            <input type="hidden" name="current_image" id="edit_current_image">
            
            <div class="form-group">
                <label>Titre</label>
                <input type="text" name="title" id="edit_title" required>
            </div>
            
            <div class="form-group">
                <label>Description</label>
                <textarea name="description" id="edit_description" rows="4"></textarea>
            </div>
            
            <div class="form-group">
                <label>Image</label>
                <input type="file" name="image" accept="image/*">
                <small>Image actuelle: <span id="edit_current_image_name"></span></small>
            </div>
            
            <div class="form-group">
                <label>Lien Demo</label>
                <input type="url" name="demo_url" id="edit_demo_url">
            </div>
            
            <div class="form-group">
                <label>Lien Code</label>
                <input type="url" name="code_url" id="edit_code_url">
            </div>
            
            <div class="form-group">
                <label>Technologies (séparées par des virgules)</label>
                <input type="text" name="technologies" id="edit_technologies">
            </div>
            
            <button type="submit" class="btn btn-primary">Mettre à jour</button>
        </form>
    </div>
</div>

<script>
function openModal(id) {
    document.getElementById(id).style.display = 'block';
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

function editProject(project) {
    document.getElementById('edit_id').value = project.id;
    document.getElementById('edit_current_image').value = project.image || '';
    document.getElementById('edit_title').value = project.title;
    document.getElementById('edit_description').value = project.description || '';
    document.getElementById('edit_demo_url').value = project.demo_url || '';
    document.getElementById('edit_code_url').value = project.code_url || '';
    document.getElementById('edit_technologies').value = project.technologies || '';
    document.getElementById('edit_current_image_name').textContent = project.image || 'Aucune image';
    openModal('editModal');
}

// Fermer modal en cliquant à l'extérieur
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}
</script>

<?php include 'includes/footer.php'; ?>