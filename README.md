# asistencia
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Conectados - Control de Asistencia</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <!-- Header -->
  <header class="site-header">
    <div class="container header-inner">
      <div class="brand">
        <img src="logo.png" alt="Logo" class="logo" aria-label="Logo">
        <div class="brand-text">
          <span class="brand-title">Conectados</span>
          <span class="brand-subtitle">por Mendoza Futura</span>
        </div>
      </div>
      <div class="user-area">
        <span class="user-name" aria-label="Usuario actual">Sonia Guevara</span>
        <span class="user-avatar" aria-hidden="true">👤</span>
      </div>
    </div>
  </header>

  <!-- Nav -->
  <nav class="site-nav" aria-label="Navegación principal">
    <div class="container nav-inner">
      <a href="#" class="nav-link">Dashboard</a>
      <a href="#" class="nav-link">Asistencia</a>
      <a href="#" class="nav-link">Cursos</a>
      <a href="#" class="nav-link">Configuración</a>
    </div>
  </nav>

  <!-- Main -->
  <main class="container main-content">
    <section class="asistencia-section" aria-labelledby="asistencia-titulo">
      <!-- Logo y título de la sección (izquierda) -->
      <div class="section-header">
        <img src="logo-small.png" alt="Logo Conectados" class="section-logo" />
        <h1 id="asistencia-titulo" class="section-title">Conectados por Mendoza Futura</h1>
      </div>

      <!-- Tabla de control de asistencia -->
      <div class="attendance-panel">
        <div class="panel-header">
          <h2>Asistencias</h2>
          <div class="panel-subheader">
            <label for="fecha" class="visually-hidden">Fecha</label>
            <input type="date" id="fecha" class="date-input" aria-label="Fecha de la asistencia">
          </div>
        </div>

        <!-- Tabla de estudiantes -->
        <div class="table-wrap">
          <table class="students-table" aria-label="Tabla de estudiantes y estados de asistencia">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Estado</th>
                <th>Clase</th>
              </tr>
            </thead>
            <tbody id="students-body">
              <!-- Filas ejemplo (reemplázalas dinámicamente si conectas con backend) -->
              <tr>
                <td>Nombre Estudiante 1</td>
                <td class="state-cell">
                  <label><input type="radio" name="s1" value="presente"> Presente</label><br/>
                  <label><input type="radio" name="s1" value="ausente"> Ausente</label><br/>
                  <label><input type="radio" name="s1" value="ausente_justificado"> Ausente justificado</label>
                </td>
                <td>Curso A</td>
              </tr>
              <tr>
                <td>Nombre Estudiante 2</td>
                <td class="state-cell">
                  <label><input type="radio" name="s2" value="presente"> Presente</label><br/>
                  <label><input type="radio" name="s2" value="ausente"> Ausente</label><br/>
                  <label><input type="radio" name="s2" value="ausente_justificado"> Ausente justificado</label>
                </td>
                <td>Curso B</td>
              </tr>
              <!-- Añade más filas según necesidad -->
            </tbody>
          </table>
        </div>

        <!-- Observaciones -->
        <div class="observations">
          <label for="observaciones" class="observations-label">Observaciones</label>
          <textarea id="observaciones" class="observations-text" placeholder="Escribe observaciones generales de la sesión..."></textarea>
        </div>

        <!-- Pie de panel (opcional: botón para guardar) -->
        <div class="panel-actions">
          <button class="btn btn-primary" type="button" id="save-btn">Guardar / Actualizar</button>
        </div>
      </div>

      <!-- Nombre del facilitador (derecha) -->
      <aside class="facilitator-info" aria-label="Facilitador actual">
        <div class="facilitator-card">
          <span class="label">Facilitador</span>
          <span class="facilitator-name">Nombre del facilitador</span>
        </div>
      </aside>
    </section>
  </main>

  <!-- Footer -->
  <footer class="site-footer" role="contentinfo">
    <div class="container footer-inner">
      <span>&copy; 2026 Mendoza Futura. Todos los derechos reservados.</span>
    </div>
  </footer>

  <!-- Scripts (opcional: ajustar datos dinámicamente) -->
  <script>
    // Ejemplo: guardar estado de asistencia de forma local
    document.getElementById('save-btn').addEventListener('click', function () {
      // Lectura simple de estados
      const rows = document.querySelectorAll('#students-body tr');
      const data = [];
      rows.forEach((row, idx) => {
        const name = row.cells<a href="" class="citation-link" target="_blank" style="vertical-align: super; font-size: 0.8em; margin-left: 3px;">[0]</a>.innerText.trim();
        const radios = row.querySelectorAll('input[type="radio"]');
        let estado = '';
        radios.forEach(r => { if (r.checked) estado = r.value; });
        data.push({ id: idx+1, name, estado });
      });
      const obs = document.getElementById('observaciones').value;
      console.log({ data, observaciones: obs });
      alert('Datos de asistencia guardados (simulado).');
    });
  </script>
</body>
</html>
