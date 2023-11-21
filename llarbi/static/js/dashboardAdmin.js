      // Script para achicar y expandir el sidebar al hacer clic en el icono de ajustes
      const settingsIcon = document.getElementById("settings-icon");
      const sidebar = document.getElementById("sidebar");
      const content = document.getElementById("content");
      const hiddenContent = document.querySelectorAll(".hidden-content");

      let isSidebarMinimized = false;

      settingsIcon.addEventListener("click", () => {
          if (isSidebarMinimized) {
              sidebar.classList.remove("sidebar-minimized");
              content.style.marginLeft = "250px";
              hiddenContent.forEach(element => element.style.display = "block");
              isSidebarMinimized = false;
          } else {
              sidebar.classList.add("sidebar-minimized");
              content.style.marginLeft = "50px";
              hiddenContent.forEach(element => element.style.display = "none");
              isSidebarMinimized = true;
          }
      });