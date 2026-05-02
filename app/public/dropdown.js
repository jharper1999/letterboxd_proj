fetch("/api/tags")
  .then((response) => response.json())
  .then((tags) => {
    const app = document.getElementById("app");
    if (!app) return;

    const select = document.createElement("select");
    select.id = "tag-select";

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Choose a tag";
    defaultOption.selected = true;
    defaultOption.disabled = true;
    select.appendChild(defaultOption);

    tags.forEach((tag) => {
      const option = document.createElement("option");
      option.value = String(tag);
      option.textContent = String(tag);
      select.appendChild(option);
    });

    const selectedTags = new Set();

    const selectedTagsDiv = document.createElement("div");
    selectedTagsDiv.id = "selected-tags";
    selectedTagsDiv.style.marginTop = "20px";

    const selectedTagsTitle = document.createElement("h3");
    selectedTagsTitle.textContent = "Selected Tags";
    selectedTagsDiv.appendChild(selectedTagsTitle);

    const selectedTagsList = document.createElement("div");
    selectedTagsList.id = "selected-tags-list";
    selectedTagsDiv.appendChild(selectedTagsList);

    const updateSelectedTagsDisplay = () => {
      selectedTagsList.innerHTML = "";
      if (selectedTags.size === 0) {
        selectedTagsList.textContent = "No tags selected.";
        return;
      }

      selectedTags.forEach((tag) => {
        const tagItem = document.createElement("div");
        tagItem.style.display = "flex";
        tagItem.style.alignItems = "center";
        tagItem.style.padding = "8px";
        tagItem.style.marginBottom = "8px";
        tagItem.style.backgroundColor = "#e9ecef";
        tagItem.style.borderRadius = "4px";

        const tagText = document.createElement("span");
        tagText.textContent = tag;
        tagText.style.marginRight = "10px";

        const removeButton = document.createElement("button");
        removeButton.textContent = "Remove";
        removeButton.style.padding = "4px 8px";
        removeButton.style.backgroundColor = "#dc3545";
        removeButton.style.color = "white";
        removeButton.style.border = "none";
        removeButton.style.borderRadius = "4px";
        removeButton.style.cursor = "pointer";

        removeButton.addEventListener("click", () => {
          selectedTags.delete(tag);
          updateSelectedTagsDisplay();
          fetchMoviesForSelectedTags();
        });

        tagItem.appendChild(tagText);
        tagItem.appendChild(removeButton);
        selectedTagsList.appendChild(tagItem);
      });
    };

    const fetchMoviesForSelectedTags = () => {
      if (selectedTags.size === 0) {
        results.textContent = "Select tags to view movies.";
        return;
      }

      const tagsParam = Array.from(selectedTags).join(':');
      fetch(`/api/tags/${encodeURIComponent(tagsParam)}`)
        .then((response) => response.json())
        .then((movies) => {
          results.textContent = "";
          if (movies.length === 0) {
            results.textContent = "No movies found for these tags.";
            return;
          }
          
          const list = document.createElement("ul");
          list.style.listStyle = "none";
          list.style.padding = "0";
          
          movies.forEach((movie) => {
            const item = document.createElement("li");
            item.style.padding = "10px";
            item.style.marginBottom = "8px";
            item.style.backgroundColor = "#f5f5f5";
            item.style.borderRadius = "4px";
            item.style.borderLeft = "4px solid #007bff";
            
            const date = new Date(movie.date);
            const formattedDate = date.toLocaleDateString("en-GB");
            
            item.innerHTML = `
              <strong>${movie.film_title}</strong>
              <span style="color: #666; margin-left: 8px;">(${movie.film_year})</span>
              <br>
              <small style="color: #999;">Watched: ${formattedDate}</small>
            `;
            
            list.appendChild(item);
          });
          
          results.appendChild(list);
        })
        .catch((error) => {
          results.textContent = "Error loading tag movies: " + error;
        });
    };

    select.addEventListener("change", () => {
      const selectedTag = select.value;
      if (!selectedTag) return;

      selectedTags.add(selectedTag);
      updateSelectedTagsDisplay();
      fetchMoviesForSelectedTags();

      // Reset dropdown to default
      select.value = "";
    });

    const results = document.createElement("div");
    results.id = "tag-results";
    results.textContent = "Select tags to view movies.";

    app.textContent = "";
    app.appendChild(select);
    app.appendChild(selectedTagsDiv);
    app.appendChild(results);
  })
  .catch((e) => {
    const app = document.getElementById("app");
    if (app) app.textContent = "Error: " + e;
  });
