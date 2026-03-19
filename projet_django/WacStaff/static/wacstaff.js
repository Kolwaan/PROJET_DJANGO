
// ─────────────────────────────────────────────
// MODALE DE CONFIRMATION DE SUPPRESSION
// ─────────────────────────────────────────────

// Crée la modale une seule fois et l'ajoute au DOM
const modal = document.createElement('div');
modal.id = 'confirm-modal';
modal.innerHTML = `
    <div class="modal-overlay">
        <div class="modal-box">
            <div class="modal-icon">⚠️</div>
            <h3 class="modal-title">Confirmer la suppression</h3>
            <p class="modal-message"></p>
            <div class="modal-actions">
                <button class="btn btn-secondary" id="modal-cancel">Annuler</button>
                <button class="btn btn-danger" id="modal-confirm">Supprimer</button>
            </div>
        </div>
    </div>
`;
document.body.appendChild(modal);

let formToSubmit = null;  // garde en mémoire le formulaire à soumettre si confirmé

// Pour chaque formulaire avec data-confirm, on intercepte la soumission
document.querySelectorAll('form[data-confirm]').forEach(function(form) {
    form.addEventListener('submit', function(e) {
        e.preventDefault();  // bloque la soumission immédiate
        formToSubmit = form;
        // Affiche le message personnalisé dans la modale
        modal.querySelector('.modal-message').textContent = form.getAttribute('data-confirm');
        modal.classList.add('active');
    });
});

// Bouton "Confirmer" → soumet le formulaire
document.getElementById('modal-confirm').addEventListener('click', function() {
    modal.classList.remove('active');
    if (formToSubmit) {
        formToSubmit.submit();
        formToSubmit = null;
    }
});

// Bouton "Annuler" → ferme la modale sans rien faire
document.getElementById('modal-cancel').addEventListener('click', function() {
    modal.classList.remove('active');
    formToSubmit = null;
});

// Clic sur l'overlay → ferme aussi la modale
modal.querySelector('.modal-overlay').addEventListener('click', function(e) {
    if (e.target === this) {
        modal.classList.remove('active');
        formToSubmit = null;
    }
});


// ─────────────────────────────────────────────
// FERMETURE AUTOMATIQUE DES MESSAGES FLASH
// ─────────────────────────────────────────────

document.querySelectorAll('.msg').forEach(function(msg) {
    setTimeout(function() {
        msg.style.transition = 'opacity 0.5s ease';
        msg.style.opacity = '0';
        setTimeout(function() { msg.remove(); }, 500);
    }, 4000);
});
