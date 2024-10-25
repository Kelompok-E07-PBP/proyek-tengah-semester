document.getElementById('reviewForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Mencegah reload halaman

    var formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest' // Menandai permintaan AJAX
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Ulasan berhasil ditambahkan!');
            location.reload(); // Reload halaman untuk menampilkan ulasan baru
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});