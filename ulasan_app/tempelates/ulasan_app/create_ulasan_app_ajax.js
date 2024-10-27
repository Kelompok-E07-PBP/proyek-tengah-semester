document.addEventListener("DOMContentLoaded", function () {
    const ulasanContainer = document.getElementById("ulasan-container");

    function fetchUlasan() {
        fetch("/ajax/json/")
            .then(response => response.json())
            .then(data => {
                ulasanContainer.innerHTML = "";  // Kosongkan container
                data.forEach(ulasan => {
                    const ulasanDiv = document.createElement("div");
                    ulasanDiv.className = "bg-white shadow-md rounded px-6 py-4 mb-4";
                    ulasanDiv.innerHTML = `
                        <h2 class="font-bold">${ulasan.user}</h2>
                        <p class="text-gray-600">Produk: ${ulasan.product_name}</p>
                        <p class="text-gray-600">Rating: ${ulasan.rating}</p>
                        <p class="text-gray-500 text-sm">${new Date(ulasan.date).toLocaleString()}</p>
                        <div class="flex justify-between mt-4">
                            <span>Likes: ${ulasan.likes}</span>
                            <span>Dislikes: ${ulasan.dislikes}</span>
                        </div>
                        <div class="mt-2">
                            <a href="/hapus/${ulasan.id}/" class="text-red-500 hover:underline">Hapus</a>
                        </div>
                    `;
                    ulasanContainer.appendChild(ulasanDiv);
                });
            })
            .catch(error => console.error('Error:', error));
    }

    document.querySelector(".bg-green-500").addEventListener("click", fetchUlasan);
});