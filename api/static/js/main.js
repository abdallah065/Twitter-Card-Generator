window.onload = function () {
    document
        .getElementById("cardForm")
        .addEventListener("submit", function (event) {
            event.preventDefault();

            // Get form values
            const title = document.getElementById("title").value;
            const description = document.getElementById("description").value;
            const image_url = document.getElementById("image_url").value;
            const url = document.getElementById("url").value;

            // Create card data
            const cardData = { title, description, image_url, url };

            // preview card
            document.getElementById("previewLink").href = url;
            document.getElementById("previewImage").style.width = document.getElementById("mainContainer").style.width
            document.getElementById("previewImage").src = image_url;
            document.getElementById("previewContainer").style.display = "block";


            // Send data to the server
            fetch("/create-card", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(cardData),
            })
                .then((response) => response.json())
                .then((data) => {
                    const link = data.link;

                    // Update link input with generated link
                    const linkInput = document.getElementById("cardLink");
                    linkInput.value = link;

                    // Show the link container
                    document.getElementById("linkContainer").style.display = "block";
                });
        });

    // Copy link to clipboard
    document
        .getElementById("copyButton")
        .addEventListener("click", function () {
            const linkInput = document.getElementById("cardLink");
            linkInput.select();
            document.execCommand("copy");
            alert("Link copied to clipboard!");
        });
}