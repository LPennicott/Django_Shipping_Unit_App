
<script>
document.addEventListener('DOMContentLoaded', function () {
    const deleteModal = document.getElementById('deleteModal');
    const deleteForm = document.getElementById('deleteForm');
    const recordNameElem = document.getElementById('recordName');
    let deleteUrl = null;

    deleteModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const recordId = button.getAttribute('data-record-id');
        const recordName = button.getAttribute('data-record-name');
        deleteUrl = button.getAttribute('data-url');

        recordNameElem.textContent = recordName;
        deleteForm.setAttribute('data-record-id', recordId);
    });

    deleteForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch(deleteUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                const modal = bootstrap.Modal.getInstance(deleteModal);
                modal.hide();

                const card = document.getElementById(`record-card-${data.id}`);
                if (card) card.remove();

                location.reload();
            } else {
                alert("Failed to delete record.");
            }
        } catch (err) {
            console.error("AJAX delete error:", err);
        }
    });

    const editModal = document.getElementById('editModal');
    const editModalBody = document.getElementById('editModalBody');

    editModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const editUrl = button.getAttribute('data-url');

        fetch(editUrl, {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.text())
        .then(html => {
            editModalBody.innerHTML = html;

            const form = editModal.querySelector("form");
            if (form) {
                form.addEventListener("submit", function (e) {
                    e.preventDefault();
                    const formData = new FormData(form);
                    const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;

                    fetch(editUrl, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken,
                            "X-Requested-With": "XMLHttpRequest"
                        },
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            bootstrap.Modal.getInstance(editModal).hide();
                            location.reload();
                        } else {
                            editModalBody.innerHTML = data.html;
                        }
                    });
                });
            }
        });
    });

    const detailModal = document.getElementById("detailModal");
    detailModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        const url = button.getAttribute("data-url");

        fetch(url, {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("detailModalContent").innerHTML = data.html;
        });
    });
});
</script>
